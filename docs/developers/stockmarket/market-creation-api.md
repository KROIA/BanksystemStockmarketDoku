---
title: "Market integration API"
description: "Opening, closing and pausing markets from another mod, and opening the trade screen or a price chart on the client."
---

# Market integration API

This API lets another mod create, delete and pause StockMarket markets on the server, and show the trade screen or a live price chart on the client. It lives in `net.kroia.stockmarket.api.integration`.

| Class | Side | What it does |
|---|---|---|
| `IStockMarketIntegration` | Server thread, master only | Create, delete and pause markets |
| `MarketConfig` | Server | The starting settings of a new market |
| `MarketOpenResult` | Server | The result of creating a market |
| `StockMarketClientIntegration` | Client thread | Open the trade screen, embed a price chart |

Markets are keyed by BankSystem's `ItemID` (`net.kroia.banksystem.util.ItemID`). Get one with `ItemID.of(itemStack)`.

## Getting the integration

```java
IStockMarketIntegration markets = StockMarketMod.getAPI().getIntegration();
if (markets == null) {
    return;   // no server in this JVM, or it hasn't started yet
}
```

- `getIntegration()` returns `null` on a pure client and before the server has started. It's safe to fetch it again on every use.
- **Every method is server-thread only.** From another thread, move to the server thread first.
- **It works on the master only** (or a single server), where the markets live. It doesn't forward to the master on a slave. There, `openMarket` returns `FAILED`, `marketExistsFor` and `isMarketOpen` return `false`, and the other methods do nothing.

## Creating a market

```java
MarketOpenResult.Result openMarket(ItemID subject, MarketConfig cfg);
```

The market gets its settings from `cfg` only. [Market presets](../../admin/stockmarket/presets.md) are not used, so the result is the same on every server.

`MarketConfig` is a record:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `virtualOrderbookEnabled` | `boolean` | `true` | Bot orders in the order book. `false` = only player orders. |
| `defaultPrice` | `float` | `1.0` | Starting price, in the money players see (not raw). |
| `naturalAbundance` | `float` | `100.0` | How common the item is: sets the order book depth and the max order size. |
| `ignorePluginAutosubscribe` | `boolean` | `false` | `true` = no plugin is added to the new market automatically. |

`MarketConfig.defaults()` returns these defaults. Build configs with the constructor or `defaults()`; new fields may be added later.

**Max order size.** A new market's largest player order is `max(f, round(f × naturalAbundance))` items, where `f` is the **Max order size factor** from the [Mod Settings](../../admin/stockmarket/mod-settings.md) (64 by default). So `defaults()` allows 6,400 items per order, and abundance `0` allows 64. Bot orders have no limit.

### A normal market

Bot orders and the default plugins, like a market an admin creates:

```java
MarketOpenResult.Result result = markets.openMarket(subject, MarketConfig.defaults());
```

### A players-only market

For example for company shares, where only players should set the price. Set **both** flags:

```java
MarketConfig shares = new MarketConfig(
        false,    // virtualOrderbookEnabled: no bot orders
        100.0f,   // defaultPrice
        0.0f,     // naturalAbundance: max order size 64
        true      // ignorePluginAutosubscribe: no plugins
);
MarketOpenResult.Result result = markets.openMarket(subject, shares);
```

The two flags are independent. With only the first, plugins still join the market and trade on it. With only the second, the bot orders still give the market depth. `ignorePluginAutosubscribe` only applies at creation: an admin can still add plugins to the market later.

### The result

`openMarket` never returns `null`. The result is a record `Result(Status status, String reason)` with `isSuccess()`:

| `Status` | Meaning |
|---|---|
| `SUCCESS` | The market exists now. Connected players see it at once. `reason` is `null`. |
| `ALREADY_EXISTS` | There's already a market for this item. Nothing changed, so calling `openMarket` again at every start is safe. |
| `ITEM_BLACKLISTED` | BankSystem doesn't allow the item. |
| `FAILED` | Anything else. `reason` says why, for example on a slave. |

```java
switch (result.status()) {
    case SUCCESS, ALREADY_EXISTS -> { }
    case ITEM_BLACKLISTED -> LOGGER.warn("Item not allowed: {}", result.reason());
    case FAILED -> LOGGER.error("Could not create market: {}", result.reason());
}
```

## Checking and deleting a market

```java
boolean marketExistsFor(ItemID subject);
void closeMarket(ItemID subject);
```

`closeMarket` **deletes** the market: it cancels every open player order and refunds it, removes the market from all plugins and from every player's screen. If there is no market, nothing happens. To get it back, call `openMarket` again; the price history is gone.

## Pausing a market (maintenance)

```java
void setMarketOpen(ItemID subject, boolean open);
void setMarketOpen(ItemID subject, boolean open, String reasonKey);
String getMarketCloseReason(ItemID subject);
boolean isMarketOpen(ItemID subject);
```

`setMarketOpen(subject, false)` puts the market into [maintenance mode](../../admin/stockmarket/markets.md#maintenance-mode), `true` ends it. Unlike `closeMarket`, the market and its price history stay. The state is saved with the world.

!!! warning "Maintenance cancels player orders"
    Pausing cancels every open player order on the market and refunds it. Players can't place new orders until you end maintenance, and the cancelled orders don't come back. Bot orders stay, and bots keep trading.

- **Reason.** With `reasonKey`, players see your text in the market's maintenance banner instead of the plain maintenance text. Pass a translation key from your own lang file. Ending maintenance clears it, also when an admin or a command ends it. `getMarketCloseReason` returns the key, or `null`.
- **`isMarketOpen`** is `true` only if the market exists and isn't in maintenance. It doesn't look at [trading hours](../../admin/stockmarket/trading-hours.md): a market outside its hours still counts as open here.
- If there is no market, `setMarketOpen` does nothing.

## When StockMarket isn't installed

If your mod should also run without StockMarket, keep every StockMarket call in its own class and only touch that class after checking that the mod is loaded. Otherwise Java tries to load the StockMarket classes and your mod crashes.

```java
if (Platform.isModLoaded("stockmarket")) {     // Architectury
    StockMarketBridge.openMarket(subject);
}
```

```java
final class StockMarketBridge {   // only used when StockMarket is loaded
    static void openMarket(ItemID subject) {
        IStockMarketIntegration markets = StockMarketMod.getAPI().getIntegration();
        if (markets != null) markets.openMarket(subject, MarketConfig.defaults());
    }
}
```

## On the client

`StockMarketClientIntegration` has two static methods for your client code, for example a screen about a company. They work on every server, also on a slave. Call them on the client thread (a button handler or `init()`).

### Opening the trade screen

```java
static boolean openTradeScreen(ItemID market);
```

Opens the StockMarket trade screen with this market selected, without a StockMarket block. The server still checks every order.

- Returns `false` and does nothing if the client doesn't know the market: it doesn't exist, or the player isn't in a world.
- Otherwise it returns `true`, and the screen opens when the server answers. A slave without a connection to its master refuses, and the player gets a chat message. A closed or paused market opens and shows its banner.

### Embedding a price chart

```java
static GuiElement createPriceChart(ItemID market);
```

Creates a live candle chart of the market, as a ModUtilities `GuiElement` for your own screen. If the market isn't known yet, the chart stays empty and fills in once it appears. Its zoom and position are kept apart from the trade screen's.

**Close it** in your screen's `removed()`, or its price updates keep running for the rest of the session:

```java
GuiElement chart = StockMarketClientIntegration.createPriceChart(shareItem);
addElement(chart);

@Override
public void removed() {
    try { ((AutoCloseable) chart).close(); } catch (Exception ignored) {}
    super.removed();
}
```

## Related pages

- [Market access API](market-access-api.md): reading markets and prices.
- [Creating and managing markets](../../admin/stockmarket/markets.md): the same actions in the admin screen.
- [Setting up your project](../setup.md): adding StockMarket to your build.
