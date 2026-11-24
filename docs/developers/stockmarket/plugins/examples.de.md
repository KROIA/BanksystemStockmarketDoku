---
title: "Beispiel-Plugins"
description: "Drei vollständige Beispiel-Plugins: Preisuntergrenze, Handelszeiten und Liquiditätsanbieter."
---

# Beispiel-Plugins { #example-plugins }

Drei Plugins, jedes zeigt andere Teile der API. Alle drei halten ihre Einstellungen pro Markt, so können Admins sie für jeden Markt anders festlegen.

| Plugin | Was es tut | Was es zeigt |
|---|---|---|
| [Preisuntergrenze](#price-floor-plugin) | Hält den Preis über einem Minimum. | Einstellungen pro Markt, ein Einstellungsformular, den Zielpreis. |
| [Handelszeiten](#trading-hours-plugin) | Hält den Preis außerhalb festgelegter Zeiten still. | Zeitabhängige Logik, Live-Werte im Einstellungsformular. |
| [Liquiditätsanbieter](#liquidity-provider-plugin) | Platziert Limit-Orders rund um den Preis. | Limit-Orders, Lesen des Orderbuchs, Zustand pro Markt. |

Die Imports sind dieselben wie in [Dein erstes Plugin](getting-started.md), dazu `ByteBufCodecs` aus `net.minecraft.network.codec` und die verwendeten Klassen aus `java.util` und `java.time`.

## Preisuntergrenzen-Plugin { #price-floor-plugin }

Das **PriceFloorPlugin** ist das Plugin des Beispielprojekts. [Dein erstes Plugin](getting-started.md) zeigt seinen vollständigen Code: das Server-Plugin, die Registrierung und das Einstellungsformular.

Was du daraus mitnehmen kannst:

- **Es greift nur ein, wenn es nötig ist.** Über der Untergrenze tut es nichts, so behalten die anderen Plugins die Kontrolle über den Preis.
- **Es setzt das Ziel, nicht den Preis.** `setTargetPrice` wartet im Cache, bis alle Plugins gelaufen sind. Setzt ein anderes Plugin das Ziel später im selben Tick, gewinnt dieses Plugin. Lass die Preisuntergrenze in der Liste unter dem VolatilityPlugin.
- **Die Einstellungen brauchen keinen eigenen Code.** `getCustomSettings(marketID)` in `update` liest die Untergrenze des Markts. Das Framework hält die Einstellungen vor, schickt sie und speichert sie.

## Handelszeiten-Plugin { #trading-hours-plugin }

Das **TradingHoursPlugin** hält den Preis eines Markts außerhalb seiner Zeiten still: Es setzt den Zielpreis auf den aktuellen Preis. Jeder Markt hat eigene Zeiten. Das Einstellungsformular zeigt die Stunde des Servers und wie viele Märkte gerade festgehalten werden.

!!! note "Märkte haben echte Handelszeiten"
    StockMarket hat [Handelszeiten](../../../admin/stockmarket/trading-hours.md) eingebaut. Sie lehnen alle Orders ab, solange ein Markt geschlossen ist, und Plugins bekommen geschlossene Märkte gar nicht erst. Nutze sie für echte Öffnungszeiten. Dieses Plugin zeigt nur zeitabhängige Plugin-Logik: Spieler können weiter handeln, während es den Preis festhält.

### Server-Plugin { #server-plugin }

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

### Einstellungsformular { #settings-form }

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

### Was du daraus mitnehmen kannst { #what-to-take-from-it }

- **Die Stundenprüfung steckt im Settings-Record.** `isOpen` behandelt Zeiten über Mitternacht. Der kompakte Konstruktor ersetzt Stunden außerhalb von 0 bis 23, so wird eine ungültige Eingabe nie gespeichert. Das Formular zeigt die korrigierten Werte aus `onCustomSettingsResponse`.
- **Kein `save` und `load`.** Das Framework speichert die Zeiten jedes Markts. Die Zahl der festgehaltenen Märkte wird in jedem Tick neu ermittelt.
- **Ein Live-Wert für alle Märkte.** `provideRuntimeData` schickt die Stunde und eine Anzahl. Das Framework schickt nur dann ein Paket, wenn sich einer der beiden Werte geändert hat, und prüft einmal pro Sekunde.
- **Position in der Liste.** Wie die Preisuntergrenze muss das Plugin unter dem VolatilityPlugin laufen, sonst verschiebt das Volatilitäts-Plugin das Ziel wieder.
- **Serverzeit.** `LocalTime.now()` ist die Uhr des Servers, nicht die Zeit in der Spielwelt.

## Liquiditätsanbieter-Plugin { #liquidity-provider-plugin }

Das **LiquidityProviderPlugin** platziert Limit-Orders etwas unter und über dem Preis, damit Spieler einen Handelspartner finden. Jeder Markt hat seinen eigenen Spread und seine eigene Ordergröße. Das Einstellungsformular zeigt den letzten Kauf- und Verkaufspreis des ausgewählten Markts.

### Server-Plugin { #server-plugin_1 }

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

### Einstellungsformular { #settings-form_1 }

Das Formular funktioniert wie das Handelszeiten-Formular, mit den Feldern **Spread** und **Order Size**. Hier stehen nur die Teile, die sich unterscheiden. Der Konstruktor, `onActiveMarketChanged`, `onCustomSettingsResponse` und `layoutChanged` folgen demselben Muster.

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

### Was du daraus mitnehmen kannst { #what-to-take-from-it_1 }

- **Zustand pro Markt.** `onMarketSubscribed` legt den Zustand des Markts an, `onMarketUnsubscribed` entfernt ihn. Das ist das übliche Muster für alles, was ein Plugin pro Markt verfolgt. Der Zustand wird nicht gespeichert. Nach einem Neustart fängt das Plugin wieder von vorn an zu zählen.
- **Limit-Orders.** `placeOrder(amount, price)` platziert eine Limit-Order: Eine positive Menge kauft, eine negative verkauft. Die Order wartet im Cache und kommt ins Buch, nachdem alle Plugins gelaufen sind.
- **Kein Stornieren.** Die Plugin-API kann keine Limit-Order stornieren. Deshalb prüft das Plugin zuerst das Volumen und fügt nur dann eine Order hinzu, wenn eine Seite dünn ist, und das nur alle 5 Sekunden.
- **Bot-Orders zählen mit.** `getRealVolume` zählt auch die Bot-Orders. Auf einem Markt, bei dem **Virtuelles Orderbuch aktiv** eingeschaltet ist, ist das Buch meist tief genug, sodass das Plugin selten etwas hinzufügt. Am nützlichsten ist es auf Märkten, auf denen nur Spieler handeln.
- **Live-Werte einem Markt zuordnen.** Die Live-Werte enthalten die Item-ID als `short` (`ItemID.getShort()`). Das Formular vergleicht sie mit dem ausgewählten Markt.

## Die Beispiele registrieren { #registering-the-examples }

Alle drei werden wie das Preisuntergrenzen-Plugin registriert. Die Formulare werden nur auf dem Client gesetzt:

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

## Verwandte Seiten { #related-pages }

- [Dein erstes Plugin](getting-started.md): das Preisuntergrenzen-Plugin Schritt für Schritt.
- [Plugin-API-Referenz](api-reference.md): alle Methoden, die hier vorkommen.
- [Handelszeiten](../../../admin/stockmarket/trading-hours.md): die eingebauten Öffnungszeiten der Märkte.
- [Ein Markt-Setup wählen](../../../admin/stockmarket/setup-use-cases.md): Märkte mit und ohne Bot-Orders.
