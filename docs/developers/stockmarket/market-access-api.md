---
title: "Market access API"
description: "Reading markets and placing orders from another mod: sync, async and client APIs, and request failures."
---

# Market access API

This page covers reading markets, prices and orders, and placing orders for the player, from another mod. The interfaces live in `net.kroia.stockmarket.api` (`market`, `marketmanager`, `preset`, `pluginmanager`).

## What your mod can reach

| You want to | Use | Where |
|---|---|---|
| Read markets and prices, or place orders for the local player (a HUD, your own screen) | The client managers | Client |
| Create, delete or pause a market | `IStockMarketIntegration`, see [Market integration API](market-creation-api.md) | Master server |
| Change prices or place bot orders | A plugin, see [Plugin system overview](plugins/index.md) | Master server |

On the server, StockMarket doesn't hand its market manager to other mods: `StockMarketMod.getAPI()` only has `getModID()`, `getModVersion()` and `getIntegration()`. The sync and async interfaces further down describe how StockMarket's own parts talk to each other. You meet them through the client managers and in plugins.

## On the client

```java
StockMarketModBackend.ClientInstances client = StockMarketModBackend.getClientInstances();
if (client == null) return;   // not in a world
```

The holder is created when the player joins a world and set to `null` when they leave. Fetch it each time instead of keeping it. It has three managers:

| Field | Type | Who may use it |
|---|---|---|
| `MARKET_MANAGER` | `IClientMarketManager` | Every player |
| `PLUGIN_MANAGER` | `IClientPluginManager` | Admins only; the server refuses other players |
| `PRESET_MANAGER` | `IAsyncPresetManager` | Admins only |

### Reading markets

`IClientMarketManager`:

| Method | What it does |
|---|---|
| `requestMarkets()` | Asks the server for all markets and refreshes the local list. `CompletableFuture<List<ItemID>>`. |
| `getAvailableMarkets()` | The list from the last `requestMarkets()`. |
| `getMarket(ItemID)` | The `ClientMarket` from the local list, or `null`. |
| `requestPendingOrders(itemFilter, bankAccountNr, playerFilter, timeBegin, timeEnd)` | Open orders, filtered. |
| `getTradingCurrencyIDAsync()` | The money item the markets trade against. |
| `getCrossRateMarket(have, want)` | Price data for a pair of two markets (want price ÷ have price), for a chart. |
| `requestCreateMarket(ItemID)`, `requestDeleteMarket(ItemID)` | Admins only. |

New and deleted markets reach the local list by themselves; you don't need to call `requestMarkets()` again.

`ClientMarket` gives you `getItemID()`, `getCurrentMarketPrice()` (raw), `getCurrentMarketRealPrice()` and `getTradingState()`: `OPEN`, `CLOSED` (outside trading hours) or `MAINTENANCE`. If the state isn't known yet, it says `OPEN`; the server still refuses orders on a closed market. `ClientMarket` also implements `IPriceDataProvider` with the candles for a chart.

### Placing an order

The order is placed for the local player, from a bank account they may use. Volumes and prices are real values: positive volume buys, negative volume sells.

```java
ClientMarket market = client.MARKET_MANAGER.getMarket(itemID);
if (market == null) return;

market.createMarketBuyOrder(accountNr, 16).whenComplete((answer, error) -> {
    if (error != null) {
        // no answer: the order may have been placed. Don't send it again;
        // ask the player to check their open orders.
        return;
    }
    if (answer == null) return;   // couldn't be sent (not in a world)
    switch (answer.status) {
        case CREATED          -> { }
        case ORDER_TOO_LARGE  -> showMessage("Max order size: " + answer.detail);
        case TRADING_TOO_FAST -> showMessage("Wait " + answer.detail + " ms");
        case MARKET_CLOSED    -> showMessage("Market closed");
        default               -> showMessage("Rejected: " + answer.status);
    }
});
```

| Method | Order |
|---|---|
| `createMarketBuyOrder(accountNr, volume)`, `createMarketSellOrder(accountNr, volume)` | Market order at the best price |
| `createLimitBuyOrder(accountNr, volume, price)`, `createLimitSellOrder(accountNr, volume, price)` | Limit order at a price |
| `createMarketOrder(accountNr, volume)`, `createLimitOrder(accountNr, volume, price)` | The sign of `volume` decides buy or sell |
| `createOrder(accountNr, Order.Type, volume, price)` | The general form |

The sell methods expect a negative volume and the buy methods a positive one; the wrong sign becomes 0 and is refused. The two-argument `createLimitBuyOrder(accountNr, volume)` and `createLimitSellOrder(accountNr, volume)` are deprecated: they place **market** orders. Use `createMarketBuyOrder` and `createMarketSellOrder`.

### Why an order was refused

The answer's `status` (`CreateOrderRequest.Status`) says what happened. `detail` carries a number for two of them.

| Status | Meaning |
|---|---|
| `CREATED` | The order was placed. |
| `NO_SUCH_MARKET` | There is no market for the item. |
| `INVALID_VOLUME`, `INVALID_PRICE` | Volume 0, or a negative price. |
| `MARKET_CLOSED` | The market is in maintenance or outside its trading hours. Nothing was locked. |
| `ORDER_TOO_LARGE` | Above the market's max order size. `detail` = the limit in items. |
| `TRADING_TOO_FAST` | The player's trade cooldown hasn't run out. `detail` = the remaining milliseconds. |
| `ACCOUNT_FROZEN` | A BankSystem admin froze the bank account. |
| `NO_BANK_ACCOUNT`, `NO_BANK_USER`, `NO_PERMISSION_TO_DEPOSIT`, `NO_PERMISSION_TO_WITHDRAW` | The player may not trade from this account. |
| `NOT_ENOUGH_MONEY`, `NOT_ENOUGH_ITEM` | The account doesn't have enough. |
| Others (`NO_ITEM_BANK`, `UNABLE_TO_LOCK_MONEY`, …) | The bank couldn't reserve the money or items. |

## When a request fails

Every request that goes over the network can fail: the client managers' requests, order methods, and every async call from a slave to its master. The future then completes **exceptionally** with one of two exceptions from ModUtilities (`net.kroia.modutilities.networking.client_server.arrs`):

| Exception | What happened | What you may do |
|---|---|---|
| `RequestNotSentException` | The request was never sent, for example because the slave isn't connected to its master. Nothing happened. | Report a plain failure. Undoing something you reserved yourself is safe. |
| `RequestOutcomeUnknownException` | It was sent, but no answer came in time or the connection dropped. The other side may have done it. | **Never undo, refund or resend automatically.** Tell the user it may have worked and read the state again. |

Treat any other exception like an unknown outcome. Requests from a client are never checked before sending, so they only fail with `RequestOutcomeUnknownException`.

Callbacks may get the cause wrapped in a `CompletionException`; unwrap it:

```java
CompletableFuture<Boolean> request = ...;   // any write, for example setMaintenanceAsync(true)
request.whenComplete((ok, error) -> {
    if (error == null) {
        if (!ok) showMessage("Refused by the server");
        return;
    }
    Throwable cause = error instanceof CompletionException && error.getCause() != null
            ? error.getCause() : error;
    if (cause instanceof RequestNotSentException) {
        showMessage("Not sent. Nothing changed.");
    } else {
        showMessage("No answer from the server - the change may have been applied.");
        reloadFromServer();   // read again; never undo or resend
    }
});
```

- **Reads:** on failure, keep the old value or show "unavailable". Retrying later is fine.
- **Writes and orders:** never retry automatically.
- **Timeouts:** 30 seconds; 120 seconds for price, order and transaction history.
- **Threads:** the future completes on the game thread of the side that sent the request, so callbacks may touch the game.

A **refusal** is not an exception: the future completes normally with `false` or `null`. Treat `null` like `false`. Examples: a player without admin rights, or a write from a slave that the master doesn't trust.

## Sync and async interfaces

Every StockMarket manager has a sync side and an async side, picked through a facade:

```java
public interface IMarketManager {
    boolean hasSyncAccess();                  // true on the master
    boolean hasAsyncAccess();                 // master, or a slave connected to it
    @Nullable IServerMarketManager getSync(); // null on a slave
    IAsyncMarketManager getAsync();
    boolean isSlave();
    boolean isMaster();
}
```

| Side | `getSync()` | `getAsync()` |
|---|---|---|
| Master or single server | the real manager | the same object; futures complete at once |
| Slave, connected | `null` | sends every call to the master |
| Slave, not connected | `null` | sends nothing; the future completes at once with a fallback value |

The fallback values of an unconnected slave are `false`, `0`, an empty list, `null` or a new default object. `isUnderMaintenanceAsync()` returns `true`, so the market counts as closed. Check `hasAsyncAccess()` first if you need to tell "no master" from "no data".

The async market (`IAsyncMarket`) reads the default and current price, order book volume, limit orders, maintenance state, settings and the current candle, and can place orders, pause the market and set trading hours. Sync calls (`ISyncServerMarket`, `ISyncServerMarketManager`) exist only on the master and must run on the server thread.

## Raw and real values

StockMarket stores prices and volumes as whole numbers (**raw**). The **real** value is the raw value divided by the item's scale factor from BankSystem: money and items can have decimals. Methods without `Real` in their name use raw values. In plugins, `IPluginMarket` converts between them.

## Related pages

- [Market integration API](market-creation-api.md): create, delete and pause markets, trade screen and chart.
- [Developers](../index.md): which API for which job.
- [Plugin API reference](plugins/api-reference.md): the market as plugins see it.
