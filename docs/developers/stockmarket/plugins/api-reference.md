---
title: "Plugin API reference"
description: "ServerPlugin, IPluginMarket, IPluginOrderBook, PluginGuiElement and the registry."
---

# Plugin API reference

Every class and method a plugin uses, grouped by class. The [Plugin system overview](index.md) explains when the framework calls what; [Your first plugin](getting-started.md) shows the classes in use.

**Units.** A "real" price or volume is what players see: a price of `0.1`, a volume of `2.5` items. A "backend" or "raw" value is the internal whole number behind it. Use the real methods unless you work level by level in the order book.

**Signs.** Order amounts are positive for buying and negative for selling. Order book volumes are positive on the buy side (bids) and negative on the sell side (asks).

## ServerPlugin

`net.kroia.stockmarket.pluginsystem.plugin.ServerPlugin<TSettings, TRuntimeData>`

The base class of every plugin. `TSettings` is the settings type of one market, `TRuntimeData` the type of the live values for the settings form. Use `Void` for a type you don't need.

### Methods you implement

| Method | When it's called |
|---|---|
| `void init()` | Once, right after the instance is created (by **Add Plugin** or when the world loads). |
| `void deInit()` | Once, when an admin deletes the instance. Not when the server stops. |
| `void update(List<MarketInterface> markets)` | Every tick while the plugin is enabled. `markets` holds the subscribed markets inside their trading hours. |
| `void finalize(List<MarketInterface> markets)` | Every tick, after every enabled plugin ran `update`, with the same markets. The caches are applied after all `finalize` calls. |
| `void onMarketSubscribed(ItemID marketID)` | A market was added to the plugin. Set up per-market state here. |
| `void onMarketUnsubscribed(ItemID marketID)` | A market was removed. Its settings are already gone. |
| `void onEnable()` | The plugin was switched on, also when an enabled plugin is loaded. |
| `void onDisable()` | The plugin was switched off. |

### Methods you can override

| Method | Default | What it's for |
|---|---|---|
| `protected @Nullable StreamCodec<ByteBuf, TSettings> customSettingsCodec()` | `null` | The codec of the settings. `null` = no settings. |
| `protected @Nullable TSettings provideDefaultCustomSettings()` | `null` | The settings a newly subscribed market gets. |
| `protected void onCustomSettingsApplied(ItemID marketID, @NotNull TSettings settings)` | nothing | Called after settings were stored for a market: defaults on subscribe, an admin's **Apply**, the saved values on load, `replaceCustomSettings`. |
| `protected @Nullable StreamCodec<ByteBuf, TRuntimeData> runtimeDataCodec()` | `null` | The codec of the live values. `null` = no live values. |
| `protected @Nullable TRuntimeData provideRuntimeData()` | `null` | The current live values. `null` = nothing to send now. |
| `public long getRuntimeDataStreamInterval()` | `500` | Milliseconds between two live updates. A packet is only sent when the encoded value changed. |
| `public boolean save(CompoundTag tag)` | `false` | Write your own extra data. The tag is only stored if it isn't empty; the return value isn't checked. |
| `public boolean load(CompoundTag tag)` | `false` | Read it back. Runs after the markets and their settings are restored, before `onEnable()`. |

### Methods you call

| Method | What it does |
|---|---|
| `final @Nullable TSettings getCustomSettings(ItemID marketID)` | The settings of one market, or `null`. |
| `final void replaceCustomSettings(ItemID marketID, @NotNull TSettings settings)` | Stores new settings for a market from inside the plugin, for example a value the plugin worked out. They are saved and shown in the settings form. Calls `onCustomSettingsApplied`. |
| `final List<MarketInterface> getMarketInterfaces()` | All subscribed markets, also the closed ones. |
| `final @Nullable MarketInterface getMarketInterface(ItemID marketID)` | One subscribed market, or `null`. |
| `List<ItemID> getSubscribedMarkets()` | The IDs of the subscribed markets. |
| `void subscribeToMarket(ItemID itemID)` | Adds a market. Calls `onMarketSubscribed` and stores the default settings. Ignored with an error inside `init`, `update` and `finalize`. |
| `void unsubscribeFromMarket(ItemID itemID)` | Removes a market. Same limits. |
| `final boolean isEnabled()`, `void setEnabled(boolean)` | The **Enabled** switch. `setEnabled` calls `onEnable` or `onDisable` when the state changes. |
| `String getName()`, `void setName(String)` | The instance's name in the plugin list. It starts as the registered name. |
| `String getDescription()`, `void setDescription(String)` | The instance's description. |
| `final UUID getInstanceID()` | The ID of this instance. Several instances of one type can exist. |
| `final @Nullable String getPluginTypeID()` | The registered type ID. |
| `boolean getAutoSubscribeNewMarkets()`, `void setAutoSubscribeNewMarkets(boolean)` | The **Auto-subscribe** switch. Default `true`. |
| `boolean isLoggerEnabled()`, `void setLoggerEnabled(boolean)` | The **Logger** switch. |
| `protected final void info(String)`, `warn(String)`, `error(String)`, `error(String, Throwable)`, `debug(String)` | Write to the server log, with the prefix `[Plugin: <name>]`. Only when the **Logger** switch is on. |

### Framework methods

The framework calls these. Don't call or rely on them: `encodeRuntimeData()`, `encodeCustomSettings(ItemID)`, `encodeAllCustomSettings()`, `decodeAndApplyCustomSettings(ItemID, byte[])`, `decodeAndApplyCustomSettingsLegacy(byte[])`, `setInstanceID(UUID)`, `setRegistrar(PluginRegistryObject)`, `getGenericPluginData()`, `getNetworkStreamPacketTickInterval()` and the methods ending in `_internal`.

## MarketInterface

`net.kroia.stockmarket.pluginsystem.interaction.MarketInterface`

One subscribed market, as `update` and `finalize` get it.

| Field | Type | What it gives |
|---|---|---|
| `market` | `IPluginMarket` | Prices, target price, orders, player flow. |
| `oderBook` | `IPluginOrderBook` | Orders in the book, volume, bot orders. The name is spelled without the first "r". |

## IPluginMarket

`net.kroia.stockmarket.api.plugin.interaction.IPluginMarket`

Changes go into the market's cache and are applied after all plugins ran, unless the table says otherwise.

### Prices

| Method | What it does |
|---|---|
| `@NotNull ItemID getMarketID()` | The market's item ID. |
| `double getPrice()` | The current price. |
| `double getDefaultRealPrice()` | The market's default price. |
| `void setDefaultRealPrice(double defaultRealPrice)` | Changes the default price, at once and for good: it's saved with the market. Must be above 0. For rare, lasting shifts; the News plugin uses it for permanent events. |
| `double convertBackendPriceToRealPrice(long backendPrice)` | Backend price → real price. |
| `long convertRealPriceToBackendPrice(double realPrice)` | Real price → backend price. |
| `default double getMaxRealOrderVolume()` | The market's **Max order size** for players, in items. `0` = no limit; treat it as "no limit", never divide by it. Bot orders aren't limited by it. Default `0`. |
| `float getNaturalAbundance()` | The market's abundance. The default order book uses it for its depth. |

### Target price

The target price is the price the Target Price Bot trades towards.

| Method | What it does |
|---|---|
| `double getPreviousTargetPrice()` | The target that was applied last tick. |
| `double getTargetPrice()` | The target set in this tick so far, else last tick's. |
| `void setTargetPrice(double targetPrice)` | Sets the target. The last plugin that sets it in a tick wins. |
| `void addToTargetPrice(double delta)` | Shifts the target up (positive) or down (negative). |
| `default boolean isTargetPriceSetThisTick()` | Whether a plugin already set the target in this tick. Use it to set a target only when nobody else did. Default `false`. |

### Fair price

A channel between plugins for the price a market settles at without the random swing. The Net Flow plugin publishes it; the Volatility plugin adds its swing on top, and the default order book is centred on it.

| Method | What it does |
|---|---|
| `default void setEquilibriumPrice(double equilibriumPrice)` | Publishes this tick's fair price (real price). Default: does nothing. |
| `default double getEquilibriumPrice()` | This tick's fair price, else last tick's, else the default price, for example on a market without the Net Flow plugin. Default: `getDefaultRealPrice()`. |

### Orders

| Method | What it does |
|---|---|
| `long placeOrder(double amount, double price)` | Places a limit order at a real price. The return value can't be used to cancel it: the plugin API has no cancel method. |
| `void placeOrder(double amount)` | Places a market order at the best price in the book. All market orders of one market in one tick are added up into one order. |

Orders that are still in the cache when a market closes are dropped.

### Market state

| Method | What it does |
|---|---|
| `boolean isMarketOpen()` | `true` when the market is inside its trading hours and not in maintenance mode. In maintenance mode player orders are refused, but plugin orders still trade. Markets outside their trading hours don't reach `update` and `finalize` at all. |
| `boolean isVirtualOrderbookEnabled()` | Whether the market has bot orders (**Enable Virtual Orderbook**). Skip markets without them if your plugin reads or changes bot orders. |
| `void clearVirtualOrderbook()` | Removes all bot orders and keeps the book empty through later price moves, until `resetVirtualOrderbook()`. |
| `void resetVirtualOrderbook()` | Refills the bot orders from the default distribution and ends a clear. |
| `float getCurrentCandleTradedVolume()` | The volume traded in the current candle. Starts at 0 with every new candle. |

### Player flow

The net flow is the items players sold into the market minus the items they bought. Positive means players sold more than they bought.

| Method | What it does |
|---|---|
| `double getNetPlayerItemFlow()` | The flow since the last reset. |
| `default double getFadedNetPlayerItemFlow()` | The same flow, fading towards 0 with the **Net flow half-life (min)** of the [Mod Settings](../../../admin/stockmarket/mod-settings.md). Old trades lose their effect, steady trading keeps it up. Use this one for prices. Default: `getNetPlayerItemFlow()`. |
| `default void setNetPlayerItemFlow(double)`, `default void setFadedNetPlayerItemFlow(double)` | Overwrite the counters, at once. Default: do nothing. |

## IPluginOrderBook

`net.kroia.stockmarket.api.plugin.interaction.IPluginOrderBook`

The order book holds two kinds of volume: **limit orders** (from players and plugins) and **virtual volume**, the bot orders that make sure players can always trade. "Virtual" methods only count the bot orders.

The `Order` class is `net.kroia.stockmarket.stockmarket.market.core.order.Order`; `Tuple` is `net.kroia.modutilities.Tuple`.

### Orders

| Method | What it does |
|---|---|
| `@NotNull List<Order> getBuyOrders()`, `getSellOrders()` | All limit orders on one side. |
| `@NotNull List<Order> getBuyOrders(long startPrice, long endPrice)`, `getSellOrders(long, long)` | The limit orders in a backend price range, both ends included. |
| `@NotNull List<Order> getNewOrders()` | The orders created since the last update. |

### Volume

| Method | What it does |
|---|---|
| `float getRealVolume(double minPrice, double maxPrice)` | All volume between two real prices. |
| `float getRealVolume(long backendPrice)` | All volume at one backend price. |
| `float getRealVirtualVolume(long backendPrice)` | Bot volume at one backend price. |
| `default float getRealVirtualVolume(double minPrice, double maxPrice)` | Bot volume between two real prices. Limit orders aren't counted. Default `0`. |
| `long getRawVolume(long backendPrice)`, `float getRawVirtualVolume(long backendPrice)` | The same in raw units. |
| `float getCapital(long startPrice, long endPrice)` | Volume × price in a backend price range: how much money sits there. |

### Sizing an order

Both methods walk the book level by level, the way a market order eats it, including the bot volume outside the visible range. They only count bot orders on the side the order eats, so an order of the returned size never passes the target. The result is signed: negative = asks a buy eats (target above the price), positive = bids a sell eats (target below). Both default to `0`.

| Method | What it does |
|---|---|
| `default float getRealVirtualVolumeToPrice(double targetRealPrice, double capReal)` | The bot volume between the current price and `targetRealPrice`. Stops counting at `capReal` items; `Double.POSITIVE_INFINITY` = no cap. |
| `default float getRealVirtualAvailableVolume(double targetRealPrice, int levels, double capReal)` | The bot volume "within reach": skips empty levels up to the first level with volume, then adds that level and the next `levels − 1`. Stops at the target and at `capReal`. The Target Price Bot sizes its orders with it. |

### Changing the bot orders

| Method | What it does |
|---|---|
| `@NotNull Tuple<Double, Double> getEditablePriceRange()` | The real price range where you can set bot volume. |
| `@NotNull Tuple<Long, Long> getEditableBackendPriceRange()` | The same range as backend prices. |
| `void setRawVolume(double minPrice, double maxPrice, float volume)` | Sets the same volume on every level of a real price range. Give a positive volume; the side sets the sign. |
| `void setRawVolume(long backendStartPrice, float[] volume)` | Sets one value per level, starting at a backend price. |
| `void addRawVolume(double minPrice, double maxPrice, float volume)`, `addRawVolume(long, float[])` | Adds instead of sets. |
| `void resetVirtualVolume()` | Sets all bot volume to 0. |
| `default void setVirtualDepthSideFactors(float bidFactor, float askFactor)` | How fast the remembered bot volume outside the editable range recovers, per side. `1` = the speed from the Mod Settings; `2` refills twice as fast and removes extra volume half as fast. The values stay until set again. Default: does nothing. |

### The default distribution

The default distribution is the normal shape of the bot orders. Plugins add to it with an `IVolumeDistributionCalculator`; the Order book volume plugin registers one.

| Method | What it does |
|---|---|
| `void registerDefaultVolumeDistributionCalculator(IVolumeDistributionCalculator)` | Adds a calculator. |
| `void unregisterDefaultVolumeDistributionCalculator(IVolumeDistributionCalculator)` | Removes it again. |
| `float getDefaultRealVolume(double pickPrice)` | The sum of all calculators at a real price. Centred on the fair price (`getEquilibriumPrice()`), split into bids and asks at the current price. |
| `default float getDefaultRealVolumeAround(double centerPrice, double pickPrice)` | The same, centred and split at `centerPrice`. Uses only the calculators' static shape. Default: `getDefaultRealVolume(pickPrice)`. |
| `float getDefaultRawVolume(double pickPrice)` | The sum in raw units. |
| `float[] getDefaultRawVolume(long backendStartPrice, int count)` | Raw values for `count` levels in a row, starting at a backend price. Much faster than one call per level. |

## IVolumeDistributionCalculator

`net.kroia.stockmarket.api.plugin.interaction.IVolumeDistributionCalculator`

| Method | What it does |
|---|---|
| `float getVolume(double marketPrice, double volumePickPrice)` | The bot volume at `volumePickPrice` when the distribution is centred on `marketPrice`. The order book sets the sign: below the price counts as bids, above as asks. |
| `default float getStaticVolume(double marketPrice, double volumePickPrice)` | Only the normal shape, without parts that react to recent trading. Used where the book's normal depth is measured, such as `getDefaultRealVolumeAround`. Default: `getVolume(...)`. |

## PluginGuiElement

`net.kroia.stockmarket.pluginsystem.screen.PluginGuiElement<TSettings, TRuntimeData>`

The client-side settings form of a plugin. The type parameters must match the server plugin's. It extends `StockMarketGuiElement` and uses the ModUtilities GUI elements (`Label`, `TextBox`, `Button` in `net.kroia.modutilities.gui.elements`).

### Setup

| Method | Default | What it does |
|---|---|---|
| `public boolean needsCustomScreen()` | `false` | `true` = the plugin's entry shows **Open Plugin Settings**, which opens a full screen with your element. `false` = the element sits inside the entry. |
| `protected @Nullable StreamCodec<ByteBuf, TSettings> customSettingsCodec()` | `null` | The same settings codec as on the server. |
| `protected @Nullable StreamCodec<ByteBuf, TRuntimeData> runtimeDataCodec()` | `null` | The same live value codec as on the server. |

An element shown inside the entry must call `setHeight(...)` in its constructor: the entry reserves exactly that height.

### Data from the server

| Method | What it does |
|---|---|
| `protected void onPluginSyncDataReceived(PluginSyncData data, @Nullable Map<ItemID, TSettings> customSettingsMap)` | The plugin's data arrived, with the settings of every market already decoded. The map is `null` when there are none. |
| `PluginSyncData getPluginSyncData()` | The last data, or `null`. |
| `UUID getPluginInstanceID()` | The plugin instance's ID, or `null` before the data arrived. |

### The selected market

| Method | What it does |
|---|---|
| `final void setActiveMarket(@Nullable ItemID marketID)` | Selects the market the form edits and calls `onActiveMarketChanged`. The Plugin Management screen calls it when the admin selects a market. |
| `@Nullable ItemID getActiveMarket()` | The selected market. |
| `protected void onActiveMarketChanged(@Nullable ItemID marketID)` | Override it to show that market's settings. |

### Sending settings

| Method | What it does |
|---|---|
| `protected final void sendCustomSettings(ItemID marketID, TSettings settings)` | Sends the settings of one market to the server. Does nothing, with a warning in the client log, without a codec, sync data or market. |
| `protected void onCustomSettingsResponse(boolean success, @Nullable ItemID marketID, @Nullable TSettings confirmedSettings)` | The server's answer, with the settings it stored. Update your copy of the market's settings here. |
| `protected final void sendCustomSettingsToAllMarkets(TSettings settings)` | Sends the settings to every subscribed market, one request each. |
| `protected final void confirmApplyToAllMarkets(TSettings settings)` | Asks the admin to confirm first, then calls `sendCustomSettingsToAllMarkets`. This is the **Apply to all** button of the built-in plugins. |
| `protected @Nullable TSettings defaultSettings()` | Override it to return the settings a new market gets. `null` = no **Defaults** button. |
| `protected void showSettings(TSettings settings)` | Override it to fill the form without sending anything. The **Defaults** button calls it. |
| `protected final @Nullable Button createDefaultsButton()` | Creates the **Defaults** button, or `null` when `defaultSettings()` is `null`. Add it to your layout yourself. |
| `public static void setSettingTooltip(Component tooltip, GuiElement... elements)` | Gives setting controls a hover tooltip that opens to the left. |

`PluginGuiElement.ApplyAllTexts` holds the translated texts of the built-in forms: `APPLY_ALL`, `APPLY_ALL_TOOLTIP`, `CONFIRM_TITLE`, `DEFAULTS`, `DEFAULTS_TOOLTIP`. An **Apply to all** button like the built-in one:

```java
Button applyAll = new Button(ApplyAllTexts.APPLY_ALL.getString(),
        () -> confirmApplyToAllMarkets(readSettingsFromForm()));
setSettingTooltip(ApplyAllTexts.APPLY_ALL_TOOLTIP, applyAll);
addChild(applyAll);

Button defaults = createDefaultsButton();   // null if defaultSettings() returns null
if (defaults != null) addChild(defaults);
```

### Live values

| Method | What it does |
|---|---|
| `void startDataStream()` | Starts the stream of live values. Does nothing before the sync data arrived or while a stream runs. |
| `void stopDataStream()` | Stops it. |
| `protected void onRuntimeDataReceived(TRuntimeData data)` | A new value arrived, already decoded. |

Call `startDataStream()` in `onPluginSyncDataReceived`, like the built-in plugins. The Plugin Management screen stops the stream when it closes or rebuilds its list, and the full plugin screen stops it when it closes.

### Drawing and helpers

| Method | What it does |
|---|---|
| `protected void layoutChanged()` | Position the child elements. Called when the element's size changes. |
| `protected void render()` | Draw extra things. Called every frame. |
| `public void setCandlestickChart(@Nullable CandlestickChart chart)` | The screen passes its chart. Override it to add an overlay, see [Chart overlays](#chart-overlays). |
| `public void setOrderbookVolumeHistogram(@Nullable OrderbookVolumeHistogram histogram)` | The same for the order book view. |
| `protected @Nullable ClientMarket getMarket(ItemID marketID)` | The client-side market. |
| `protected IClientPluginManager getPluginManager()` | The client-side plugin manager. |
| `public static boolean isMarketVisible(@Nullable ItemID marketID)` | Whether this client may show the market. On a slave server, markets whose item the slave doesn't know are hidden. Filter your market lists with it. |
| `protected void info(String)`, `warn(String)`, `error(String)`, `debug(String)` | Write to the client log. |

Layout constants of the base class: `padding` = 4, `spacing` = 4, `defaultElementHeight` = 20, `hoverToolTipFontSize` = 0.8.

## PluginSyncData

`net.kroia.stockmarket.pluginsystem.plugin.core.PluginSyncData`

The plugin's data as the settings form gets it.

| Method | What it returns |
|---|---|
| `UUID getInstanceID()` | The instance ID. |
| `String getName()`, `String getDescription()` | Name and description. |
| `String getPluginTypeID()` | The type ID. |
| `boolean isEnabled()`, `boolean isLoggerEnabled()` | The switches. |
| `List<ItemID> getSubscribedMarkets()` | The subscribed markets. |
| `Map<ItemID, byte[]> getCustomSettings()` | The encoded settings per market. You rarely need it: `onPluginSyncDataReceived` gets them decoded. |
| `GenericPluginData getGenericData()` | The raw metadata. |

## PluginRegistry and PluginRegistryObject

`net.kroia.stockmarket.pluginsystem.registry.PluginRegistry` (static methods) and `net.kroia.stockmarket.pluginsystem.registry.PluginRegistryObject`.

| Method | What it does |
|---|---|
| `PluginRegistry.registerPlugin(String pluginTypeID, String pluginName, String pluginDescription, Supplier<ServerPlugin> serverPluginFactory)` | Registers a plugin type and returns its `PluginRegistryObject`. If the type ID is taken, it returns the existing object and registers nothing. |
| `PluginRegistry.findPlugin(String pluginTypeID)` | The registered type, or `null`. |
| `PluginRegistry.getRegistryObjects()` | All registered types. The **Add Plugin** list shows them. |
| `PluginRegistry.instantiateServerPlugin(...)`, `PluginRegistry.createGuiElement(String)` | Used by the framework. |
| `getPluginTypeID()`, `getPluginName()`, `getPluginDescription()` | The registered values. A new instance takes its name and description from here. |
| `setGuiElementFactory(@Nullable Supplier<PluginGuiElement> factory)` | Sets the settings form. Call it on the client only. |
| `getGuiElementFactory()` | The factory, or `null`. Without a factory the entry gets an empty element. |

## Chart overlays

The Plugin Management screen shows a candlestick chart and an order book view (`net.kroia.stockmarket.screen.widgets.CandlestickChart` and `OrderbookVolumeHistogram`). It passes both to every settings form. An overlay is a function that draws on one of them after it drew itself, clipped to its drawing area. When the screen rebuilds its list, it first passes `null`, so remove your overlay from the old widget.

| `CandlestickChart` method | What it does |
|---|---|
| `addOverlay(Overlay)`, `removeOverlay(Overlay)` | Adds or removes a `CandlestickChart.Overlay`: `void render(CandlestickChart chart)`. |
| `Rectangle getCanvasBounds()` | The drawing area (`net.kroia.modutilities.gui.geometry.Rectangle`, fields `x`, `y`, `width`, `height`). |
| `int toCanvasSpaceX(long time)` | A time on the chart's time axis → x coordinate. |
| `int toCanvasSpaceY(double price)` | A price → y coordinate. |
| `@Nullable ClientMarket getMarket()` | The market the chart shows. |

| `OrderbookVolumeHistogram` method | What it does |
|---|---|
| `addOverlay(Overlay)`, `removeOverlay(Overlay)` | Adds or removes an `OrderbookVolumeHistogram.Overlay`: `void render(OrderbookVolumeHistogram histogram)`. |
| `Rectangle getCanvasBounds()` | The drawing area. |
| `int toCanvasSpaceX(float absVolume)` | A volume → x coordinate. The bars grow from the right. |
| `int toCanvasSpaceY(double price)` | A price → y coordinate, the same as in the chart. |
| `float getMaxAbsVolume()` | The largest volume shown, to scale your values. |
| `double getStartPrice()`, `double getEndPrice()` | The price range shown. |
| `@Nullable ClientMarket getMarket()` | The market shown. |

Draw with the widget's own methods: `drawRect(x, y, width, height, color)`, `drawLine(x1, y1, x2, y2, thickness, color)`, `drawText(text, x, y)` and `getTextHeight()`. Colours are ARGB, for example `0xFFFF6600`.

```java
private void drawTargetLine(CandlestickChart chart) {
    ClientMarket market = chart.getMarket();
    if (market == null) return;
    double target = targetFor(market.getItemID());   // your own value
    Rectangle bounds = chart.getCanvasBounds();
    int y = chart.toCanvasSpaceY(target);
    if (y >= bounds.y && y <= bounds.y + bounds.height) {
        chart.drawRect(bounds.x, y - 1, bounds.width, 2, 0xFFFF6600);
        chart.drawText("Target", bounds.x + 4, y - chart.getTextHeight() - 2);
    }
}
```

## Built-in plugins

`net.kroia.stockmarket.pluginsystem.Plugins` registers the five built-in plugins. Their type ID is the class name; the classes are in `net.kroia.stockmarket.pluginsystem.plugins`. Their `Settings` records and `DEFAULT_*` constants are public, so you can read the defaults or build settings, for example for `replaceCustomSettings`. What each setting does in game is on the admin page of the plugin.

| Registry object | Class | Admin page |
|---|---|---|
| `NET_FLOW_PLUGIN` | `NetFlowPlugin` | [Net Flow plugin](../../../admin/stockmarket/plugins/net-flow.md) |
| `VOLATILITY_PLUGIN` | `VolatilityPlugin` | [Volatility plugin](../../../admin/stockmarket/plugins/volatility.md) |
| `DEFAULT_ORDERBOOK_VOLUME_DISTRIBUTION_PLUGIN` | `DefaultOrderbookVolumeDistributionPlugin` | [Order book volume plugin](../../../admin/stockmarket/plugins/order-book-volume.md) |
| `TARGET_PRICE_BOT_PLUGIN` | `TargetPriceBot` | [Target Price Bot](../../../admin/stockmarket/plugins/target-price-bot.md) |
| `NEWS_PLUGIN` | `NewsPlugin` | [News plugin](../../../admin/stockmarket/plugins/news.md) |

A new world creates them in the order of this table, all enabled. Together they form the price:

1. **NetFlowPlugin** works out the fair price from the faded player flow and publishes it with `setEquilibriumPrice`. It also sets the target to the fair price, but only if no plugin did in this tick.
2. **VolatilityPlugin** sets the target to fair price × (1 + random swing).
3. **DefaultOrderbookVolumeDistributionPlugin** shapes the bot orders around the fair price.
4. **TargetPriceBot** reads `getPreviousTargetPrice()` and places market orders towards it, every 5th tick, on markets with bot orders.
5. **NewsPlugin** multiplies the target in `finalize` while news events run.

### Settings records

| Class | `Settings` fields | Defaults and helpers |
|---|---|---|
| `NetFlowPlugin` | `flowEnabled`, `flowSensitivity`, `minPriceMult`, `maxPriceMult`, `permanentImpact`, `capacityVolatilityScale`, `thetaCapEnabled`, `saturationEnabled`, `anchorEnabled`, `anchorTimeDays`, `anchorMaxMovePerDay`, `anchorMinMult`, `anchorMaxMult` | `true`, `2000`, `0.05`, `3`, `0.5`, `0.3`, `true`, `true`, `true`, `2`, `0.1`, `0.25`, `4`. `Settings.createDefault()` and the copy methods `withPermanentImpact`, `withCapacityVolatilityScale`, `withToggles`, `withAnchor`, `withAnchorEnabled`. Invalid `permanentImpact` and anchor values become the defaults. |
| `VolatilityPlugin` | `volatilityScale` | `0.3` (`DEFAULT_VOLATILITY_SCALE`). `Settings.createDefault()`. |
| `DefaultOrderbookVolumeDistributionPlugin` | `volumeScale`, `speed`, `accumulationRate`, `decumulationRate`, `resetVolume`, `trendPeriodMinutes`, `trendGain`, `trendMaxFactor`, `roundLevelScale`, `roundLevelWidth`, `roundLevelRange`, `wallPeriodMinutes`, `wallDeadZone`, `wallStrength`, `wallCap` | `1`, `0.05`, `0.1`, `0.01`, then trend `10`, `10`, `4`, round levels `1`, `0.03`, `1.1`, wall `2880`, `0.15`, `200`, `40`. `Settings.createDefault()`, `withTrend`, `withRoundLevels`, `withWall`. |
| `TargetPriceBot` | `pidP`, `pidI`, `pidD`, `pidRate`, `maxOrderVolumeFactor`, `maxTargetMovePerSecond`, `reversionTimeSeconds`, `oscillationPeriodSeconds`, `oscillationDamping`, `oscillationAmplitude`, `availableVolumeLevels`, `maxRampFraction` | `0.5`, `0.1`, `0`, `0.1`, `10`, `0.005`, `600`, `60`, `0.3`, `0.15`, `50`, `2`. `Settings.createDefault()`, `withReference`, `withAvailableVolumeLevels`, `withMaxRampFraction`. |
| `NewsPlugin` | `newsEnabled`, `sensitivity` | `true`, `1.0`. All running events together are kept between `MIN_COMBINED_FACTOR` (0.1) and `MAX_COMBINED_FACTOR` (10). |

### Helpers

- **NetFlowPlugin** has static helpers for its formulas: `computeEquilibriumPrice`, `flowExponent`, `flowBand`, `capacity`, `stepAnchor`, `bookEFoldDepth`. A running instance reports per market: `getEquilibrium(ItemID)` (`NaN` before the first update), `getAnchorMultiplier`, `getSaturatedFlow`, `getMarketSettings`, `getBookEFold`.
- **TargetPriceBot** has static helpers for its steps: `anchorReference`, `stepReference`, `referenceAnchorPrice`, `limitTargetMove`, `botOrderVolumeLimit`, `rampFraction`, `crossesEmptyGap`. Its band and pause constants are public too: `BOT_MIN_PRICE_MULT` (0.25), `GAP_WINDOW_FRACTION` (0.01), `GAP_GUARD_MIN_BLOCK_SECONDS` and `GAP_GUARD_MAX_BLOCK_SECONDS` (a random pause of 45 to 75 seconds after each player fill), `RAMP_START_FRACTION` (0.02) and `RAMP_SECONDS` (180).

## Writing a StreamCodec

Settings and live values are records with a `public static final StreamCodec<ByteBuf, T> CODEC`. The server and the client use the same codec, and the framework does all encoding and decoding. `StreamCodec` and `ByteBufCodecs` are in `net.minecraft.network.codec`, `ByteBuf` in `io.netty.buffer`.

For a few simple fields, `StreamCodec.composite` is shortest:

```java
public record Settings(float spread, float orderSize) {
    public static final StreamCodec<ByteBuf, Settings> CODEC = StreamCodec.composite(
            ByteBufCodecs.FLOAT, Settings::spread,
            ByteBufCodecs.FLOAT, Settings::orderSize,
            Settings::new
    );
}
```

For more fields or lists, write the codec yourself. Write a list's length first, then each element:

```java
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
```

- **Check values in the record.** The server stores the decoded settings before it calls `onCustomSettingsApplied`. Fix bad values in a compact constructor, so they never get stored.
- **Keep old saves readable.** The settings are saved with the codec. If you add a field later, read it only when bytes are left (`buf.isReadable()`) and use a default otherwise.

!!! warning "Same codec on both sides"
    The client and the server must use the same codec, field for field and in the same order. Otherwise the settings arrive garbled or fail to decode.

## Related pages

- [Plugin system overview](index.md): when each method is called.
- [Your first plugin](getting-started.md): these classes in a working plugin.
- [Example plugins](examples.md): live values, limit orders and per-market state.
- [Market access API](../market-access-api.md): read and change markets from outside a plugin.
