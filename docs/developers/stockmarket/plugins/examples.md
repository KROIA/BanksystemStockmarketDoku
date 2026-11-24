---
title: "Example plugins"
description: "Three complete example plugins: price floor, trading hours and liquidity provider."
---

# Example plugins

Three plugins, each showing other parts of the API. All three keep their settings per market, so admins can set them differently for each market.

| Plugin | What it does | What it shows |
|---|---|---|
| [Price floor](#price-floor-plugin) | Keeps the price above a minimum. | Settings per market, a settings form, the target price. |
| [Trading hours](#trading-hours-plugin) | Holds the price still outside set hours. | Time-based logic, live values in the settings form. |
| [Liquidity provider](#liquidity-provider-plugin) | Places limit orders around the price. | Limit orders, reading the order book, state per market. |

The imports are the same as in [Your first plugin](getting-started.md), plus `ByteBufCodecs` from `net.minecraft.network.codec` and the `java.util` and `java.time` classes used.

## Price floor plugin

The **PriceFloorPlugin** is the plugin of the example project. [Your first plugin](getting-started.md) shows its complete code: the server plugin, the registration and the settings form.

What to take from it:

- **It only acts when needed.** Above the floor it does nothing, so the other plugins keep control of the price.
- **It sets the target, not the price.** `setTargetPrice` waits in the cache until all plugins ran. If another plugin sets the target later in the same tick, that plugin wins. Keep the price floor below the VolatilityPlugin in the list.
- **The settings need no code of their own.** `getCustomSettings(marketID)` in `update` reads the market's floor. The framework stores, sends and saves the settings.

## Trading hours plugin

The **TradingHoursPlugin** holds the price of a market still outside its hours: it sets the target price to the current price. Each market has its own hours. The settings form shows the server's hour and how many markets are held right now.

!!! note "Markets have real trading hours"
    StockMarket has [trading hours](../../../admin/stockmarket/trading-hours.md) built in. They refuse all orders while a market is closed, and plugins don't get closed markets at all. Use them for real opening times. This plugin only shows time-based plugin logic: players can still trade while it holds the price.

### Server plugin

```java title="TradingHoursPlugin.java"
public class TradingHoursPlugin extends ServerPlugin<TradingHoursPlugin.Settings, TradingHoursPlugin.Status> {

    // The hours of one market, 0 to 23. A start after the end runs over midnight, e.g. 22 to 6.
    public record Settings(int startHour, int endHour) {
        public Settings {
            if (startHour < 0 || startHour > 23) startHour = 9;
            if (endHour < 0 || endHour > 23) endHour = 17;
        }

        public static final StreamCodec<ByteBuf, Settings> CODEC = StreamCodec.composite(
                ByteBufCodecs.INT, Settings::startHour,
                ByteBufCodecs.INT, Settings::endHour,
                Settings::new
        );

        boolean isOpen(int hour) {
            if (startHour <= endHour)
                return hour >= startHour && hour < endHour;
            return hour >= startHour || hour < endHour;   // over midnight
        }
    }

    // Live values for the settings form
    public record Status(int currentHour, int heldMarkets) {
        public static final StreamCodec<ByteBuf, Status> CODEC = StreamCodec.composite(
                ByteBufCodecs.INT, Status::currentHour,
                ByteBufCodecs.INT, Status::heldMarkets,
                Status::new
        );
    }

    private int heldMarkets = 0;

    @Override
    public void update(List<MarketInterface> markets) {
        int hour = LocalTime.now().getHour();
        int held = 0;
        for (MarketInterface market : markets) {
            Settings settings = getCustomSettings(market.market.getMarketID());
            if (settings == null || settings.isOpen(hour))
                continue;
            // Outside the hours: the target stays where the price is
            market.market.setTargetPrice(market.market.getPrice());
            held++;
        }
        heldMarkets = held;
    }

    @Override public void init() {}
    @Override public void deInit() {}
    @Override public void finalize(List<MarketInterface> markets) {}
    @Override public void onMarketSubscribed(ItemID marketID) {}
    @Override public void onMarketUnsubscribed(ItemID marketID) {}
    @Override public void onEnable() {}
    @Override public void onDisable() {}

    // --- Live values ---

    @Override
    protected StreamCodec<ByteBuf, Status> runtimeDataCodec() {
        return Status.CODEC;
    }

    @Override
    protected Status provideRuntimeData() {
        return new Status(LocalTime.now().getHour(), heldMarkets);
    }

    @Override
    public long getRuntimeDataStreamInterval() {
        return 1000;   // once per second is enough for an hour display
    }

    // --- Per-market settings ---

    @Override
    protected StreamCodec<ByteBuf, Settings> customSettingsCodec() {
        return Settings.CODEC;
    }

    @Override
    protected Settings provideDefaultCustomSettings() {
        return new Settings(9, 17);
    }
}
```

### Settings form

```java title="TradingHoursGuiElement.java"
public class TradingHoursGuiElement
        extends PluginGuiElement<TradingHoursPlugin.Settings, TradingHoursPlugin.Status> {

    private final Label startLabel = new Label("Start Hour:");
    private final TextBox startTextBox = new TextBox();
    private final Label endLabel = new Label("End Hour:");
    private final TextBox endTextBox = new TextBox();
    private final Button applyButton = new Button("Apply", this::onApply);
    private final Label statusLabel = new Label("Status: --");

    private final Map<ItemID, TradingHoursPlugin.Settings> settingsMap = new HashMap<>();

    public TradingHoursGuiElement() {
        startTextBox.setMatchRegex(TextBox.createRegex_onlyNumerical(true, false, 2, 0));
        endTextBox.setMatchRegex(TextBox.createRegex_onlyNumerical(true, false, 2, 0));

        addChild(startLabel);
        addChild(startTextBox);
        addChild(endLabel);
        addChild(endTextBox);
        addChild(applyButton);
        addChild(statusLabel);

        setHeight(4 * (defaultElementHeight + spacing) + padding);   // four rows
    }

    @Override
    protected StreamCodec<ByteBuf, TradingHoursPlugin.Settings> customSettingsCodec() {
        return TradingHoursPlugin.Settings.CODEC;
    }

    @Override
    protected StreamCodec<ByteBuf, TradingHoursPlugin.Status> runtimeDataCodec() {
        return TradingHoursPlugin.Status.CODEC;
    }

    @Override
    protected void onPluginSyncDataReceived(PluginSyncData data,
                                            @Nullable Map<ItemID, TradingHoursPlugin.Settings> customSettingsMap) {
        settingsMap.clear();
        if (customSettingsMap != null)
            settingsMap.putAll(customSettingsMap);

        List<ItemID> markets = data.getSubscribedMarkets();
        if (!markets.isEmpty())
            setActiveMarket(markets.get(0));

        startDataStream();
    }

    @Override
    protected void onActiveMarketChanged(@Nullable ItemID marketID) {
        TradingHoursPlugin.Settings settings = marketID != null ? settingsMap.get(marketID) : null;
        if (settings != null) {
            startTextBox.setText(settings.startHour());
            endTextBox.setText(settings.endHour());
        }
    }

    @Override
    protected void onCustomSettingsResponse(boolean success, @Nullable ItemID marketID,
                                            @Nullable TradingHoursPlugin.Settings confirmedSettings) {
        if (success && marketID != null && confirmedSettings != null) {
            settingsMap.put(marketID, confirmedSettings);
            if (marketID.equals(getActiveMarket()))
                onActiveMarketChanged(marketID);   // show the corrected values
        }
    }

    @Override
    protected void onRuntimeDataReceived(TradingHoursPlugin.Status data) {
        statusLabel.setText("Hour " + data.currentHour() + ", held markets: " + data.heldMarkets());
    }

    private void onApply() {
        ItemID market = getActiveMarket();
        if (market != null)
            sendCustomSettings(market, new TradingHoursPlugin.Settings(
                    (int) startTextBox.getDouble(), (int) endTextBox.getDouble()));
    }

    @Override
    protected void layoutChanged() {
        int w = getWidth();
        int eh = defaultElementHeight;
        int labelW = w / 3;
        int fieldW = w - labelW - spacing - padding;

        int y = padding;
        startLabel.setBounds(padding, y, labelW, eh);
        startTextBox.setBounds(labelW + spacing, y, fieldW, eh);
        y += eh + spacing;
        endLabel.setBounds(padding, y, labelW, eh);
        endTextBox.setBounds(labelW + spacing, y, fieldW, eh);
        y += eh + spacing;
        applyButton.setBounds(padding, y, w - 2 * padding, eh);
        y += eh + spacing;
        statusLabel.setBounds(padding, y, w - 2 * padding, eh);
    }

    @Override
    protected void render() {}
}
```

### What to take from it

- **The hours check lives in the settings record.** `isOpen` handles hours over midnight. The compact constructor replaces hours outside 0 to 23, so bad input never gets stored. The form shows the corrected values from `onCustomSettingsResponse`.
- **No `save` and `load`.** The framework saves the hours of every market. The held-market count is worked out again every tick.
- **One live value for all markets.** `provideRuntimeData` sends the hour and a count. The framework only sends a packet when one of them changed, and checks once per second.
- **Position in the list.** Like the price floor, the plugin must run below the VolatilityPlugin, or the Volatility plugin moves the target again.
- **Server time.** `LocalTime.now()` is the server's clock, not the time in the game world.

## Liquidity provider plugin

The **LiquidityProviderPlugin** places limit orders a little below and above the price, so players find someone to trade with. Each market has its own spread and order size. The settings form shows the last buy and sell price of the selected market.

### Server plugin

```java title="LiquidityProviderPlugin.java"
public class LiquidityProviderPlugin
        extends ServerPlugin<LiquidityProviderPlugin.Settings, LiquidityProviderPlugin.Levels> {

    // spread: distance from the price on each side, as a share of the price (0.05 = 5 %)
    public record Settings(float spread, float orderSize) {
        public Settings {
            if (!(spread > 0 && spread <= 1)) spread = 0.05f;
            if (!(orderSize > 0)) orderSize = 1.0f;
        }

        public static final StreamCodec<ByteBuf, Settings> CODEC = StreamCodec.composite(
                ByteBufCodecs.FLOAT, Settings::spread,
                ByteBufCodecs.FLOAT, Settings::orderSize,
                Settings::new
        );
    }

    // Live values: the last order prices of every market
    public record Levels(List<Entry> entries) {
        public record Entry(short itemId, double buyPrice, double sellPrice) {}

        public static final StreamCodec<ByteBuf, Levels> CODEC = new StreamCodec<>() {
            @Override
            public Levels decode(ByteBuf buf) {
                int count = buf.readInt();
                List<Entry> entries = new ArrayList<>();
                for (int i = 0; i < count; i++)
                    entries.add(new Entry(buf.readShort(), buf.readDouble(), buf.readDouble()));
                return new Levels(entries);
            }

            @Override
            public void encode(ByteBuf buf, Levels data) {
                buf.writeInt(data.entries().size());
                for (Entry e : data.entries()) {
                    buf.writeShort(e.itemId());
                    buf.writeDouble(e.buyPrice());
                    buf.writeDouble(e.sellPrice());
                }
            }
        };
    }

    // State of one market, kept only while the server runs
    private static class MarketState {
        double lastBuyPrice = 0;
        double lastSellPrice = 0;
        int tickCounter = 0;
    }

    private final Map<ItemID, MarketState> marketStates = new HashMap<>();

    @Override
    public void update(List<MarketInterface> markets) {
        for (MarketInterface market : markets) {
            ItemID id = market.market.getMarketID();
            MarketState state = marketStates.get(id);
            Settings settings = getCustomSettings(id);
            if (state == null || settings == null)
                continue;
            updateMarket(market, state, settings);
        }
    }

    private void updateMarket(MarketInterface market, MarketState state, Settings settings) {
        // Only every 100 ticks (5 seconds)
        if (++state.tickCounter < 100) return;
        state.tickCounter = 0;

        double price = market.market.getPrice();
        if (price <= 0) return;

        double halfSpread = price * settings.spread();
        double buyPrice = price - halfSpread;
        double sellPrice = price + halfSpread;

        // Only act when the price moved by more than half the spread
        if (Math.abs(buyPrice - state.lastBuyPrice) <= halfSpread * 0.5
                && Math.abs(sellPrice - state.lastSellPrice) <= halfSpread * 0.5)
            return;

        float buyVolume = market.oderBook.getRealVolume(buyPrice, price);     // bids: positive
        float sellVolume = market.oderBook.getRealVolume(price, sellPrice);   // asks: negative

        if (buyVolume < settings.orderSize() * 2) {
            market.market.placeOrder(settings.orderSize(), buyPrice);          // limit buy
            info("Buy order: " + settings.orderSize() + " @ " + buyPrice);
        }
        if (Math.abs(sellVolume) < settings.orderSize() * 2) {
            market.market.placeOrder(-settings.orderSize(), sellPrice);        // limit sell
            info("Sell order: " + settings.orderSize() + " @ " + sellPrice);
        }

        state.lastBuyPrice = buyPrice;
        state.lastSellPrice = sellPrice;
    }

    @Override
    public void onMarketSubscribed(ItemID marketID) {
        marketStates.put(marketID, new MarketState());
    }

    @Override
    public void onMarketUnsubscribed(ItemID marketID) {
        marketStates.remove(marketID);
    }

    @Override public void init() {}
    @Override public void deInit() {}
    @Override public void finalize(List<MarketInterface> markets) {}
    @Override public void onEnable() {}
    @Override public void onDisable() {}

    // --- Live values ---

    @Override
    protected StreamCodec<ByteBuf, Levels> runtimeDataCodec() {
        return Levels.CODEC;
    }

    @Override
    protected Levels provideRuntimeData() {
        if (marketStates.isEmpty()) return null;   // nothing to send
        List<Levels.Entry> entries = new ArrayList<>();
        for (Map.Entry<ItemID, MarketState> e : marketStates.entrySet())
            entries.add(new Levels.Entry(e.getKey().getShort(),
                    e.getValue().lastBuyPrice, e.getValue().lastSellPrice));
        return new Levels(entries);
    }

    @Override
    public long getRuntimeDataStreamInterval() {
        return 1000;
    }

    // --- Per-market settings ---

    @Override
    protected StreamCodec<ByteBuf, Settings> customSettingsCodec() {
        return Settings.CODEC;
    }

    @Override
    protected Settings provideDefaultCustomSettings() {
        return new Settings(0.05f, 1.0f);
    }
}
```

### Settings form

The form works like the trading hours form, with **Spread** and **Order Size** fields. Only the parts that differ are shown here; the constructor, `onActiveMarketChanged`, `onCustomSettingsResponse` and `layoutChanged` follow the same pattern.

```java title="LiquidityProviderGuiElement.java (parts)"
public class LiquidityProviderGuiElement
        extends PluginGuiElement<LiquidityProviderPlugin.Settings, LiquidityProviderPlugin.Levels> {

    private final TextBox spreadTextBox = new TextBox();
    private final TextBox orderSizeTextBox = new TextBox();
    private final Label statusLabel = new Label("Levels: --");
    // ... labels, Apply button and settingsMap as in the trading hours form

    @Override
    protected StreamCodec<ByteBuf, LiquidityProviderPlugin.Levels> runtimeDataCodec() {
        return LiquidityProviderPlugin.Levels.CODEC;
    }

    @Override
    protected void onRuntimeDataReceived(LiquidityProviderPlugin.Levels data) {
        // The live values cover every market: show the selected one
        ItemID active = getActiveMarket();
        if (active == null) return;
        for (LiquidityProviderPlugin.Levels.Entry e : data.entries()) {
            if (e.itemId() == active.getShort()) {
                statusLabel.setText(String.format("Buy: %.2f | Sell: %.2f", e.buyPrice(), e.sellPrice()));
                return;
            }
        }
    }

    private void onApply() {
        ItemID market = getActiveMarket();
        if (market != null)
            sendCustomSettings(market, new LiquidityProviderPlugin.Settings(
                    (float) spreadTextBox.getDouble(), (float) orderSizeTextBox.getDouble()));
    }
}
```

### What to take from it

- **State per market.** `onMarketSubscribed` creates the market's state and `onMarketUnsubscribed` removes it. This is the usual pattern for anything a plugin tracks per market. The state isn't saved; after a restart the plugin starts counting again.
- **Limit orders.** `placeOrder(amount, price)` places a limit order: a positive amount buys, a negative one sells. The order waits in the cache and goes into the book after all plugins ran.
- **No cancelling.** The plugin API can't cancel a limit order. That's why the plugin checks the volume first and only adds an order when a side is thin, and only every 5 seconds.
- **Bot orders count too.** `getRealVolume` counts the bot orders as well. On a market with **Enable Virtual Orderbook** on, the book is usually deep enough, so the plugin rarely adds anything. It's most useful on players-only markets.
- **Matching live values to a market.** The live values hold the item ID as a `short` (`ItemID.getShort()`). The form compares it with the selected market.

## Registering the examples

All three are registered like the price floor plugin. The forms are set on the client only:

```java
public static final PluginRegistryObject TRADING_HOURS = PluginRegistry.registerPlugin(
        TradingHoursPlugin.class.getName(),
        "TradingHoursPlugin",
        "Holds the price still outside configurable hours.",
        TradingHoursPlugin::new
);

public static final PluginRegistryObject LIQUIDITY_PROVIDER = PluginRegistry.registerPlugin(
        LiquidityProviderPlugin.class.getName(),
        "LiquidityProviderPlugin",
        "Places limit orders at a spread around the current price.",
        LiquidityProviderPlugin::new
);

public static void clientSetup() {
    PRICE_FLOOR_PLUGIN.setGuiElementFactory(PriceFloorGuiElement::new);
    TRADING_HOURS.setGuiElementFactory(TradingHoursGuiElement::new);
    LIQUIDITY_PROVIDER.setGuiElementFactory(LiquidityProviderGuiElement::new);
}
```

## Related pages

- [Your first plugin](getting-started.md): the price floor plugin step by step.
- [Plugin API reference](api-reference.md): every method used here.
- [Trading hours](../../../admin/stockmarket/trading-hours.md): the built-in opening times of markets.
- [Choosing a market setup](../../../admin/stockmarket/setup-use-cases.md): markets with and without bot orders.
