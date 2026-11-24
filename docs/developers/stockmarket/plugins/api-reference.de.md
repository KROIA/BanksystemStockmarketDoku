---
title: "Plugin-API-Referenz"
description: "ServerPlugin, IPluginMarket, IPluginOrderBook, PluginGuiElement und die Registry."
---

# Plugin-API-Referenz { #plugin-api-reference }

Alle Klassen und Methoden, die ein Plugin verwendet, nach Klassen gruppiert. [Das Plugin-System im Überblick](index.md) erklärt, wann das Framework was aufruft; [Dein erstes Plugin](getting-started.md) zeigt die Klassen im Einsatz.

**Einheiten.** Ein „realer“ Preis oder ein „reales“ Volumen ist das, was Spieler sehen: ein Preis von `0.1`, ein Volumen von `2.5` Items. Ein „Backend“- oder „Roh“-Wert ist die interne ganze Zahl dahinter. Verwende die realen Methoden, außer du arbeitest dich Stufe für Stufe durch das Orderbuch.

**Vorzeichen.** Order-Mengen sind beim Kaufen positiv und beim Verkaufen negativ. Volumen im Orderbuch sind auf der Kaufseite (Bids) positiv und auf der Verkaufsseite (Asks) negativ.

## ServerPlugin { #serverplugin }

`net.kroia.stockmarket.pluginsystem.plugin.ServerPlugin<TSettings, TRuntimeData>`

Die Basisklasse jedes Plugins. `TSettings` ist der Einstellungstyp eines Markts, `TRuntimeData` der Typ der Live-Werte für das Einstellungsformular. Verwende `Void` für einen Typ, den du nicht brauchst.

### Methoden, die du implementierst { #methods-you-implement }

| Methode | Wann sie aufgerufen wird |
|---|---|
| `void init()` | Einmal, direkt nachdem die Instanz erstellt wurde (durch **Plugin hinzufügen** oder beim Laden der Welt). |
| `void deInit()` | Einmal, wenn ein Admin die Instanz löscht. Nicht, wenn der Server stoppt. |
| `void update(List<MarketInterface> markets)` | In jedem Tick, solange das Plugin aktiviert ist. `markets` enthält die abonnierten Märkte, die innerhalb ihrer Handelszeiten liegen. |
| `void finalize(List<MarketInterface> markets)` | In jedem Tick, nachdem jedes aktivierte Plugin `update` ausgeführt hat, mit denselben Märkten. Die Caches werden nach allen `finalize`-Aufrufen angewendet. |
| `void onMarketSubscribed(ItemID marketID)` | Dem Plugin wurde ein Markt hinzugefügt. Richte hier den Zustand pro Markt ein. |
| `void onMarketUnsubscribed(ItemID marketID)` | Ein Markt wurde entfernt. Seine Einstellungen sind schon weg. |
| `void onEnable()` | Das Plugin wurde eingeschaltet, auch wenn ein aktiviertes Plugin geladen wird. |
| `void onDisable()` | Das Plugin wurde ausgeschaltet. |

### Methoden, die du überschreiben kannst { #methods-you-can-override }

| Methode | Standard | Wofür sie da ist |
|---|---|---|
| `protected @Nullable StreamCodec<ByteBuf, TSettings> customSettingsCodec()` | `null` | Der Codec der Einstellungen. `null` = keine Einstellungen. |
| `protected @Nullable TSettings provideDefaultCustomSettings()` | `null` | Die Einstellungen, die ein neu abonnierter Markt bekommt. |
| `protected void onCustomSettingsApplied(ItemID marketID, @NotNull TSettings settings)` | nichts | Wird aufgerufen, nachdem Einstellungen für einen Markt gespeichert wurden: Standardwerte beim Abonnieren, ein **Anwenden** eines Admins, die gespeicherten Werte beim Laden, `replaceCustomSettings`. |
| `protected @Nullable StreamCodec<ByteBuf, TRuntimeData> runtimeDataCodec()` | `null` | Der Codec der Live-Werte. `null` = keine Live-Werte. |
| `protected @Nullable TRuntimeData provideRuntimeData()` | `null` | Die aktuellen Live-Werte. `null` = gerade nichts zu senden. |
| `public long getRuntimeDataStreamInterval()` | `500` | Millisekunden zwischen zwei Live-Updates. Ein Paket wird nur geschickt, wenn sich der kodierte Wert geändert hat. |
| `public boolean save(CompoundTag tag)` | `false` | Schreib deine eigenen zusätzlichen Daten. Der Tag wird nur gespeichert, wenn er nicht leer ist; der Rückgabewert wird nicht geprüft. |
| `public boolean load(CompoundTag tag)` | `false` | Lies sie wieder ein. Läuft, nachdem die Märkte und ihre Einstellungen wiederhergestellt sind, vor `onEnable()`. |

### Methoden, die du aufrufst { #methods-you-call }

| Methode | Was sie tut |
|---|---|
| `final @Nullable TSettings getCustomSettings(ItemID marketID)` | Die Einstellungen eines Markts oder `null`. |
| `final void replaceCustomSettings(ItemID marketID, @NotNull TSettings settings)` | Legt aus dem Plugin heraus neue Einstellungen für einen Markt ab, zum Beispiel einen Wert, den das Plugin ermittelt hat. Sie werden gespeichert und im Einstellungsformular angezeigt. Ruft `onCustomSettingsApplied` auf. |
| `final List<MarketInterface> getMarketInterfaces()` | Alle abonnierten Märkte, auch die geschlossenen. |
| `final @Nullable MarketInterface getMarketInterface(ItemID marketID)` | Ein abonnierter Markt oder `null`. |
| `List<ItemID> getSubscribedMarkets()` | Die IDs der abonnierten Märkte. |
| `void subscribeToMarket(ItemID itemID)` | Fügt einen Markt hinzu. Ruft `onMarketSubscribed` auf und speichert die Standardeinstellungen. Wird innerhalb von `init`, `update` und `finalize` mit einem Fehler ignoriert. |
| `void unsubscribeFromMarket(ItemID itemID)` | Entfernt einen Markt. Dieselben Einschränkungen. |
| `final boolean isEnabled()`, `void setEnabled(boolean)` | Der Schalter **Aktiviert**. `setEnabled` ruft `onEnable` oder `onDisable` auf, wenn sich der Zustand ändert. |
| `String getName()`, `void setName(String)` | Der Name der Instanz in der Plugin-Liste. Am Anfang ist es der registrierte Name. |
| `String getDescription()`, `void setDescription(String)` | Die Beschreibung der Instanz. |
| `final UUID getInstanceID()` | Die ID dieser Instanz. Von einem Typ kann es mehrere Instanzen geben. |
| `final @Nullable String getPluginTypeID()` | Die registrierte Typ-ID. |
| `boolean getAutoSubscribeNewMarkets()`, `void setAutoSubscribeNewMarkets(boolean)` | Der Schalter **Auto-Abo**. Standard `true`. |
| `boolean isLoggerEnabled()`, `void setLoggerEnabled(boolean)` | Der Schalter **Logger**. |
| `protected final void info(String)`, `warn(String)`, `error(String)`, `error(String, Throwable)`, `debug(String)` | Schreiben ins Server-Log, mit dem Präfix `[Plugin: <name>]`. Nur wenn der Schalter **Logger** an ist. |

### Framework-Methoden { #framework-methods }

Diese Methoden ruft das Framework auf. Ruf sie nicht selbst auf und verlass dich nicht auf sie: `encodeRuntimeData()`, `encodeCustomSettings(ItemID)`, `encodeAllCustomSettings()`, `decodeAndApplyCustomSettings(ItemID, byte[])`, `decodeAndApplyCustomSettingsLegacy(byte[])`, `setInstanceID(UUID)`, `setRegistrar(PluginRegistryObject)`, `getGenericPluginData()`, `getNetworkStreamPacketTickInterval()` und die Methoden, die auf `_internal` enden.

## MarketInterface { #marketinterface }

`net.kroia.stockmarket.pluginsystem.interaction.MarketInterface`

Ein abonnierter Markt, so wie `update` und `finalize` ihn bekommen.

| Feld | Typ | Was es liefert |
|---|---|---|
| `market` | `IPluginMarket` | Preise, Zielpreis, Orders, Spielerfluss. |
| `oderBook` | `IPluginOrderBook` | Orders im Buch, Volumen, Bot-Orders. Der Name wird ohne das erste „r“ geschrieben. |

## IPluginMarket { #ipluginmarket }

`net.kroia.stockmarket.api.plugin.interaction.IPluginMarket`

Änderungen gehen in den Cache des Markts und werden angewendet, nachdem alle Plugins gelaufen sind, sofern die Tabelle nichts anderes sagt.

### Preise { #prices }

| Methode | Was sie tut |
|---|---|
| `@NotNull ItemID getMarketID()` | Die Item-ID des Markts. |
| `double getPrice()` | Der aktuelle Preis. |
| `double getDefaultRealPrice()` | Der Standardpreis des Markts. |
| `void setDefaultRealPrice(double defaultRealPrice)` | Ändert den Standardpreis, sofort und dauerhaft: Er wird mit dem Markt gespeichert. Muss über 0 liegen. Für seltene, bleibende Verschiebungen; das News-Plugin nutzt die Methode für dauerhafte Ereignisse. |
| `double convertBackendPriceToRealPrice(long backendPrice)` | Backend-Preis → realer Preis. |
| `long convertRealPriceToBackendPrice(double realPrice)` | Realer Preis → Backend-Preis. |
| `default double getMaxRealOrderVolume()` | Die **Max. Ordergröße** des Markts für Spieler, in Items. `0` = kein Limit; behandle den Wert als „kein Limit“ und teile nie durch ihn. Bot-Orders begrenzt er nicht. Standard `0`. |
| `float getNaturalAbundance()` | Die Häufigkeit des Markts. Das Standard-Orderbuch nutzt sie für seine Tiefe. |

### Zielpreis { #target-price }

Der Zielpreis ist der Preis, auf den der Zielpreis-Bot hinhandelt.

| Methode | Was sie tut |
|---|---|
| `double getPreviousTargetPrice()` | Das Ziel, das im letzten Tick angewendet wurde. |
| `double getTargetPrice()` | Das Ziel, das bisher in diesem Tick gesetzt wurde, sonst das des letzten Ticks. |
| `void setTargetPrice(double targetPrice)` | Setzt das Ziel. Das letzte Plugin, das es in einem Tick setzt, gewinnt. |
| `void addToTargetPrice(double delta)` | Verschiebt das Ziel nach oben (positiv) oder nach unten (negativ). |
| `default boolean isTargetPriceSetThisTick()` | Ob ein Plugin das Ziel in diesem Tick schon gesetzt hat. Damit setzt du ein Ziel nur, wenn es sonst keines getan hat. Standard `false`. |

### Fairer Preis { #fair-price }

Ein Kanal zwischen Plugins für den Preis, bei dem sich ein Markt ohne die zufällige Schwankung einpendelt. Das Nettofluss-Plugin veröffentlicht ihn; das Volatilitäts-Plugin legt seine Schwankung obendrauf, und das Standard-Orderbuch ist um ihn zentriert.

| Methode | Was sie tut |
|---|---|
| `default void setEquilibriumPrice(double equilibriumPrice)` | Veröffentlicht den fairen Preis dieses Ticks (realer Preis). Standard: tut nichts. |
| `default double getEquilibriumPrice()` | Der faire Preis dieses Ticks, sonst der des letzten Ticks, sonst der Standardpreis, zum Beispiel auf einem Markt ohne das Nettofluss-Plugin. Standard: `getDefaultRealPrice()`. |

### Orders { #orders }

| Methode | Was sie tut |
|---|---|
| `long placeOrder(double amount, double price)` | Platziert eine Limit-Order zu einem realen Preis. Mit dem Rückgabewert kannst du sie nicht stornieren: Die Plugin-API hat keine Methode zum Stornieren. |
| `void placeOrder(double amount)` | Platziert eine Market-Order zum besten Preis im Buch. Alle Market-Orders eines Markts in einem Tick werden zu einer Order addiert. |

Orders, die noch im Cache liegen, wenn ein Markt schließt, werden verworfen.

### Marktzustand { #market-state }

| Methode | Was sie tut |
|---|---|
| `boolean isMarketOpen()` | `true`, wenn der Markt innerhalb seiner Handelszeiten und nicht im Wartungsmodus ist. Im Wartungsmodus werden Spieler-Orders abgelehnt, Plugin-Orders handeln aber weiter. Märkte außerhalb ihrer Handelszeiten erreichen `update` und `finalize` gar nicht. |
| `boolean isVirtualOrderbookEnabled()` | Ob der Markt Bot-Orders hat (**Virtuelles Orderbuch aktiv**). Überspringe Märkte ohne Bot-Orders, wenn dein Plugin Bot-Orders liest oder ändert. |
| `void clearVirtualOrderbook()` | Entfernt alle Bot-Orders und hält das Buch auch bei späteren Preisbewegungen leer, bis `resetVirtualOrderbook()` kommt. |
| `void resetVirtualOrderbook()` | Füllt die Bot-Orders aus der Standardverteilung neu auf und beendet ein Leeren. |
| `float getCurrentCandleTradedVolume()` | Das in der aktuellen Kerze gehandelte Volumen. Beginnt mit jeder neuen Kerze bei 0. |

### Spielerfluss { #player-flow }

Der Nettofluss ist die Zahl der Items, die Spieler in den Markt verkauft haben, minus die Items, die sie gekauft haben. Positiv heißt: Spieler haben mehr verkauft als gekauft.

| Methode | Was sie tut |
|---|---|
| `double getNetPlayerItemFlow()` | Der Fluss seit dem letzten Zurücksetzen. |
| `default double getFadedNetPlayerItemFlow()` | Derselbe Fluss, der mit der **Halbwertszeit Nettofluss (min)** aus den [Mod-Einstellungen](../../../admin/stockmarket/mod-settings.md) gegen 0 abklingt. Alte Käufe und Verkäufe verlieren ihre Wirkung, stetiger Handel hält sie aufrecht. Nimm diesen Wert für Preise. Standard: `getNetPlayerItemFlow()`. |
| `default void setNetPlayerItemFlow(double)`, `default void setFadedNetPlayerItemFlow(double)` | Überschreiben die Zähler, sofort. Standard: tun nichts. |

## IPluginOrderBook { #ipluginorderbook }

`net.kroia.stockmarket.api.plugin.interaction.IPluginOrderBook`

Das Orderbuch enthält zwei Arten von Volumen: **Limit-Orders** (von Spielern und Plugins) und **virtuelles Volumen**, also die Bot-Orders, die dafür sorgen, dass Spieler immer handeln können. Methoden mit „Virtual“ im Namen zählen nur die Bot-Orders.

Die Klasse `Order` ist `net.kroia.stockmarket.stockmarket.market.core.order.Order`; `Tuple` ist `net.kroia.modutilities.Tuple`.

### Orders { #orders_1 }

| Methode | Was sie tut |
|---|---|
| `@NotNull List<Order> getBuyOrders()`, `getSellOrders()` | Alle Limit-Orders einer Seite. |
| `@NotNull List<Order> getBuyOrders(long startPrice, long endPrice)`, `getSellOrders(long, long)` | Die Limit-Orders in einem Backend-Preisbereich, beide Enden eingeschlossen. |
| `@NotNull List<Order> getNewOrders()` | Die Orders, die seit dem letzten Update erstellt wurden. |

### Volumen { #volume }

| Methode | Was sie tut |
|---|---|
| `float getRealVolume(double minPrice, double maxPrice)` | Das gesamte Volumen zwischen zwei realen Preisen. |
| `float getRealVolume(long backendPrice)` | Das gesamte Volumen bei einem Backend-Preis. |
| `float getRealVirtualVolume(long backendPrice)` | Bot-Volumen bei einem Backend-Preis. |
| `default float getRealVirtualVolume(double minPrice, double maxPrice)` | Bot-Volumen zwischen zwei realen Preisen. Limit-Orders werden nicht mitgezählt. Standard `0`. |
| `long getRawVolume(long backendPrice)`, `float getRawVirtualVolume(long backendPrice)` | Dasselbe in Roh-Einheiten. |
| `float getCapital(long startPrice, long endPrice)` | Volumen × Preis in einem Backend-Preisbereich: wie viel Geld dort steckt. |

### Eine Order bemessen { #sizing-an-order }

Beide Methoden gehen das Buch Stufe für Stufe durch, so wie eine Market-Order es aufzehrt, einschließlich des Bot-Volumens außerhalb des sichtbaren Bereichs. Sie zählen Bot-Orders nur auf der Seite, die die Order aufzehrt. So überschreitet eine Order mit der zurückgegebenen Größe das Ziel nie. Das Ergebnis hat ein Vorzeichen: negativ = Asks, die ein Kauf aufzehrt (Ziel über dem Preis), positiv = Bids, die ein Verkauf aufzehrt (Ziel unter dem Preis). Beide haben den Standard `0`.

| Methode | Was sie tut |
|---|---|
| `default float getRealVirtualVolumeToPrice(double targetRealPrice, double capReal)` | Das Bot-Volumen zwischen dem aktuellen Preis und `targetRealPrice`. Hört bei `capReal` Items auf zu zählen; `Double.POSITIVE_INFINITY` = keine Obergrenze. |
| `default float getRealVirtualAvailableVolume(double targetRealPrice, int levels, double capReal)` | Das Bot-Volumen „in Reichweite“: überspringt leere Stufen bis zur ersten Stufe mit Volumen und addiert dann diese Stufe und die nächsten `levels − 1`. Hört beim Ziel und bei `capReal` auf. Der Zielpreis-Bot bemisst seine Orders damit. |

### Die Bot-Orders ändern { #changing-the-bot-orders }

| Methode | Was sie tut |
|---|---|
| `@NotNull Tuple<Double, Double> getEditablePriceRange()` | Der reale Preisbereich, in dem du Bot-Volumen setzen kannst. |
| `@NotNull Tuple<Long, Long> getEditableBackendPriceRange()` | Derselbe Bereich als Backend-Preise. |
| `void setRawVolume(double minPrice, double maxPrice, float volume)` | Setzt dasselbe Volumen auf jede Stufe eines realen Preisbereichs. Gib ein positives Volumen an; die Seite bestimmt das Vorzeichen. |
| `void setRawVolume(long backendStartPrice, float[] volume)` | Setzt einen Wert pro Stufe, ab einem Backend-Preis. |
| `void addRawVolume(double minPrice, double maxPrice, float volume)`, `addRawVolume(long, float[])` | Addiert, statt zu setzen. |
| `void resetVirtualVolume()` | Setzt das gesamte Bot-Volumen auf 0. |
| `default void setVirtualDepthSideFactors(float bidFactor, float askFactor)` | Wie schnell sich das gemerkte Bot-Volumen außerhalb des bearbeitbaren Bereichs erholt, pro Seite. `1` = die Geschwindigkeit aus den Mod-Einstellungen; `2` füllt doppelt so schnell auf und baut zusätzliches Volumen halb so schnell ab. Die Werte bleiben, bis sie neu gesetzt werden. Standard: tut nichts. |

### Die Standardverteilung { #the-default-distribution }

Die Standardverteilung ist die normale Form der Bot-Orders. Plugins ergänzen sie mit einem `IVolumeDistributionCalculator`; das Orderbuch-Volumen-Plugin registriert einen.

| Methode | Was sie tut |
|---|---|
| `void registerDefaultVolumeDistributionCalculator(IVolumeDistributionCalculator)` | Fügt einen Rechner hinzu. |
| `void unregisterDefaultVolumeDistributionCalculator(IVolumeDistributionCalculator)` | Entfernt ihn wieder. |
| `float getDefaultRealVolume(double pickPrice)` | Die Summe aller Rechner bei einem realen Preis. Zentriert auf den fairen Preis (`getEquilibriumPrice()`), beim aktuellen Preis in Bids und Asks geteilt. |
| `default float getDefaultRealVolumeAround(double centerPrice, double pickPrice)` | Dasselbe, aber bei `centerPrice` zentriert und geteilt. Nutzt nur die statische Form der Rechner. Standard: `getDefaultRealVolume(pickPrice)`. |
| `float getDefaultRawVolume(double pickPrice)` | Die Summe in Roh-Einheiten. |
| `float[] getDefaultRawVolume(long backendStartPrice, int count)` | Rohwerte für `count` aufeinanderfolgende Stufen, ab einem Backend-Preis. Viel schneller als ein Aufruf pro Stufe. |

## IVolumeDistributionCalculator { #ivolumedistributioncalculator }

`net.kroia.stockmarket.api.plugin.interaction.IVolumeDistributionCalculator`

| Methode | Was sie tut |
|---|---|
| `float getVolume(double marketPrice, double volumePickPrice)` | Das Bot-Volumen bei `volumePickPrice`, wenn die Verteilung auf `marketPrice` zentriert ist. Das Orderbuch setzt das Vorzeichen: Unter dem Preis zählt es als Bids, darüber als Asks. |
| `default float getStaticVolume(double marketPrice, double volumePickPrice)` | Nur die normale Form, ohne die Teile, die auf den jüngsten Handel reagieren. Wird dort verwendet, wo die normale Tiefe des Buchs gemessen wird, etwa in `getDefaultRealVolumeAround`. Standard: `getVolume(...)`. |

## PluginGuiElement { #pluginguielement }

`net.kroia.stockmarket.pluginsystem.screen.PluginGuiElement<TSettings, TRuntimeData>`

Das clientseitige Einstellungsformular eines Plugins. Die Typparameter müssen zu denen des Server-Plugins passen. Die Klasse erweitert `StockMarketGuiElement` und nutzt die GUI-Elemente von ModUtilities (`Label`, `TextBox`, `Button` in `net.kroia.modutilities.gui.elements`).

### Einrichtung { #setup }

| Methode | Standard | Was sie tut |
|---|---|---|
| `public boolean needsCustomScreen()` | `false` | `true` = Der Eintrag des Plugins zeigt **Plugin-Einstellungen öffnen**, das einen ganzen Bildschirm mit deinem Element öffnet. `false` = Das Element sitzt im Eintrag. |
| `protected @Nullable StreamCodec<ByteBuf, TSettings> customSettingsCodec()` | `null` | Derselbe Settings-Codec wie auf dem Server. |
| `protected @Nullable StreamCodec<ByteBuf, TRuntimeData> runtimeDataCodec()` | `null` | Derselbe Codec für Live-Werte wie auf dem Server. |

Ein Element, das im Eintrag angezeigt wird, muss in seinem Konstruktor `setHeight(...)` aufrufen: Der Eintrag reserviert genau diese Höhe.

### Daten vom Server { #data-from-the-server }

| Methode | Was sie tut |
|---|---|
| `protected void onPluginSyncDataReceived(PluginSyncData data, @Nullable Map<ItemID, TSettings> customSettingsMap)` | Die Daten des Plugins sind angekommen, mit den Einstellungen jedes Markts schon dekodiert. Die Map ist `null`, wenn es keine gibt. |
| `PluginSyncData getPluginSyncData()` | Die letzten Daten oder `null`. |
| `UUID getPluginInstanceID()` | Die ID der Plugin-Instanz, oder `null`, bevor die Daten angekommen sind. |

### Der ausgewählte Markt { #the-selected-market }

| Methode | Was sie tut |
|---|---|
| `final void setActiveMarket(@Nullable ItemID marketID)` | Wählt den Markt, den das Formular bearbeitet, und ruft `onActiveMarketChanged` auf. Die Plugin-Verwaltung ruft die Methode auf, wenn der Admin einen Markt auswählt. |
| `@Nullable ItemID getActiveMarket()` | Der ausgewählte Markt. |
| `protected void onActiveMarketChanged(@Nullable ItemID marketID)` | Überschreibe sie, um die Einstellungen dieses Markts anzuzeigen. |

### Einstellungen senden { #sending-settings }

| Methode | Was sie tut |
|---|---|
| `protected final void sendCustomSettings(ItemID marketID, TSettings settings)` | Schickt die Einstellungen eines Markts an den Server. Tut nichts und schreibt eine Warnung ins Client-Log, wenn Codec, Sync-Daten oder Markt fehlen. |
| `protected void onCustomSettingsResponse(boolean success, @Nullable ItemID marketID, @Nullable TSettings confirmedSettings)` | Die Antwort des Servers, mit den Einstellungen, die er gespeichert hat. Aktualisiere hier deine Kopie der Einstellungen des Markts. |
| `protected final void sendCustomSettingsToAllMarkets(TSettings settings)` | Schickt die Einstellungen an jeden abonnierten Markt, eine Anfrage pro Markt. |
| `protected final void confirmApplyToAllMarkets(TSettings settings)` | Lässt den Admin zuerst bestätigen und ruft dann `sendCustomSettingsToAllMarkets` auf. Das ist der Button **Auf alle anwenden** der eingebauten Plugins. |
| `protected @Nullable TSettings defaultSettings()` | Überschreibe sie, damit sie die Einstellungen zurückgibt, die ein neuer Markt bekommt. `null` = kein Button **Standard**. |
| `protected void showSettings(TSettings settings)` | Überschreibe sie, um das Formular zu füllen, ohne etwas zu senden. Der Button **Standard** ruft sie auf. |
| `protected final @Nullable Button createDefaultsButton()` | Erstellt den Button **Standard**, oder gibt `null` zurück, wenn `defaultSettings()` `null` ist. Füg ihn selbst in dein Layout ein. |
| `public static void setSettingTooltip(Component tooltip, GuiElement... elements)` | Gibt Bedienelementen von Einstellungen einen Hover-Tooltip, der sich nach links öffnet. |

`PluginGuiElement.ApplyAllTexts` enthält die übersetzten Texte der eingebauten Formulare: `APPLY_ALL`, `APPLY_ALL_TOOLTIP`, `CONFIRM_TITLE`, `DEFAULTS`, `DEFAULTS_TOOLTIP`. Ein Button **Auf alle anwenden** wie der eingebaute:

```java
Button applyAll = new Button(ApplyAllTexts.APPLY_ALL.getString(),
        () -> confirmApplyToAllMarkets(readSettingsFromForm()));
setSettingTooltip(ApplyAllTexts.APPLY_ALL_TOOLTIP, applyAll);
addChild(applyAll);

Button defaults = createDefaultsButton();   // null if defaultSettings() returns null
if (defaults != null) addChild(defaults);
```

### Live-Werte { #live-values }

| Methode | Was sie tut |
|---|---|
| `void startDataStream()` | Startet den Stream der Live-Werte. Tut nichts, bevor die Sync-Daten angekommen sind oder solange ein Stream läuft. |
| `void stopDataStream()` | Stoppt ihn. |
| `protected void onRuntimeDataReceived(TRuntimeData data)` | Ein neuer Wert ist angekommen, schon dekodiert. |

Rufe `startDataStream()` in `onPluginSyncDataReceived` auf, wie die eingebauten Plugins. Die Plugin-Verwaltung stoppt den Stream, wenn sie geschlossen wird oder ihre Liste neu aufbaut, und der volle Plugin-Bildschirm stoppt ihn beim Schließen.

### Zeichnen und Hilfsmethoden { #drawing-and-helpers }

| Methode | Was sie tut |
|---|---|
| `protected void layoutChanged()` | Positioniere hier die Kind-Elemente. Wird aufgerufen, wenn sich die Größe des Elements ändert. |
| `protected void render()` | Zeichne hier zusätzliche Dinge. Wird in jedem Frame aufgerufen. |
| `public void setCandlestickChart(@Nullable CandlestickChart chart)` | Der Bildschirm übergibt seinen Chart. Überschreibe die Methode, um ein Overlay hinzuzufügen, siehe [Chart-Overlays](#chart-overlays). |
| `public void setOrderbookVolumeHistogram(@Nullable OrderbookVolumeHistogram histogram)` | Dasselbe für die Orderbuch-Ansicht. |
| `protected @Nullable ClientMarket getMarket(ItemID marketID)` | Der clientseitige Markt. |
| `protected IClientPluginManager getPluginManager()` | Der clientseitige Plugin-Manager. |
| `public static boolean isMarketVisible(@Nullable ItemID marketID)` | Ob dieser Client den Markt anzeigen darf. Auf einem Slave-Server sind Märkte ausgeblendet, deren Item der Slave nicht kennt. Filtere deine Marktlisten damit. |
| `protected void info(String)`, `warn(String)`, `error(String)`, `debug(String)` | Schreiben ins Client-Log. |

Layout-Konstanten der Basisklasse: `padding` = 4, `spacing` = 4, `defaultElementHeight` = 20, `hoverToolTipFontSize` = 0.8.

## PluginSyncData { #pluginsyncdata }

`net.kroia.stockmarket.pluginsystem.plugin.core.PluginSyncData`

Die Daten des Plugins, so wie das Einstellungsformular sie bekommt.

| Methode | Was sie zurückgibt |
|---|---|
| `UUID getInstanceID()` | Die Instanz-ID. |
| `String getName()`, `String getDescription()` | Name und Beschreibung. |
| `String getPluginTypeID()` | Die Typ-ID. |
| `boolean isEnabled()`, `boolean isLoggerEnabled()` | Die Schalter. |
| `List<ItemID> getSubscribedMarkets()` | Die abonnierten Märkte. |
| `Map<ItemID, byte[]> getCustomSettings()` | Die kodierten Einstellungen pro Markt. Du brauchst sie selten: `onPluginSyncDataReceived` bekommt sie dekodiert. |
| `GenericPluginData getGenericData()` | Die rohen Metadaten. |

## PluginRegistry und PluginRegistryObject { #pluginregistry-and-pluginregistryobject }

`net.kroia.stockmarket.pluginsystem.registry.PluginRegistry` (statische Methoden) und `net.kroia.stockmarket.pluginsystem.registry.PluginRegistryObject`.

| Methode | Was sie tut |
|---|---|
| `PluginRegistry.registerPlugin(String pluginTypeID, String pluginName, String pluginDescription, Supplier<ServerPlugin> serverPluginFactory)` | Registriert einen Plugin-Typ und gibt sein `PluginRegistryObject` zurück. Ist die Typ-ID schon vergeben, gibt die Methode das vorhandene Objekt zurück und registriert nichts. |
| `PluginRegistry.findPlugin(String pluginTypeID)` | Der registrierte Typ oder `null`. |
| `PluginRegistry.getRegistryObjects()` | Alle registrierten Typen. Die Liste **Plugin hinzufügen** zeigt sie. |
| `PluginRegistry.instantiateServerPlugin(...)`, `PluginRegistry.createGuiElement(String)` | Werden vom Framework benutzt. |
| `getPluginTypeID()`, `getPluginName()`, `getPluginDescription()` | Die registrierten Werte. Eine neue Instanz übernimmt Name und Beschreibung von hier. |
| `setGuiElementFactory(@Nullable Supplier<PluginGuiElement> factory)` | Setzt das Einstellungsformular. Ruf die Methode nur auf dem Client auf. |
| `getGuiElementFactory()` | Die Factory oder `null`. Ohne Factory bekommt der Eintrag ein leeres Element. |

## Chart-Overlays { #chart-overlays }

Die Plugin-Verwaltung zeigt einen Kerzenchart und eine Orderbuch-Ansicht (`net.kroia.stockmarket.screen.widgets.CandlestickChart` und `OrderbookVolumeHistogram`). Sie übergibt beide an jedes Einstellungsformular. Ein Overlay ist eine Funktion, die auf eines der beiden Widgets zeichnet, nachdem es sich selbst gezeichnet hat, beschnitten auf seinen Zeichenbereich. Wenn der Bildschirm seine Liste neu aufbaut, übergibt er zuerst `null`. Entferne dann dein Overlay vom alten Widget.

| `CandlestickChart`-Methode | Was sie tut |
|---|---|
| `addOverlay(Overlay)`, `removeOverlay(Overlay)` | Fügt ein `CandlestickChart.Overlay` hinzu oder entfernt es: `void render(CandlestickChart chart)`. |
| `Rectangle getCanvasBounds()` | Der Zeichenbereich (`net.kroia.modutilities.gui.geometry.Rectangle`, Felder `x`, `y`, `width`, `height`). |
| `int toCanvasSpaceX(long time)` | Eine Zeit auf der Zeitachse des Charts → x-Koordinate. |
| `int toCanvasSpaceY(double price)` | Ein Preis → y-Koordinate. |
| `@Nullable ClientMarket getMarket()` | Der Markt, den der Chart zeigt. |

| `OrderbookVolumeHistogram`-Methode | Was sie tut |
|---|---|
| `addOverlay(Overlay)`, `removeOverlay(Overlay)` | Fügt ein `OrderbookVolumeHistogram.Overlay` hinzu oder entfernt es: `void render(OrderbookVolumeHistogram histogram)`. |
| `Rectangle getCanvasBounds()` | Der Zeichenbereich. |
| `int toCanvasSpaceX(float absVolume)` | Ein Volumen → x-Koordinate. Die Balken wachsen von rechts. |
| `int toCanvasSpaceY(double price)` | Ein Preis → y-Koordinate, genau wie im Chart. |
| `float getMaxAbsVolume()` | Das größte angezeigte Volumen, um deine Werte zu skalieren. |
| `double getStartPrice()`, `double getEndPrice()` | Der angezeigte Preisbereich. |
| `@Nullable ClientMarket getMarket()` | Der angezeigte Markt. |

Zeichne mit den eigenen Methoden des Widgets: `drawRect(x, y, width, height, color)`, `drawLine(x1, y1, x2, y2, thickness, color)`, `drawText(text, x, y)` und `getTextHeight()`. Farben sind ARGB, zum Beispiel `0xFFFF6600`.

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

## Eingebaute Plugins { #built-in-plugins }

`net.kroia.stockmarket.pluginsystem.Plugins` registriert die fünf eingebauten Plugins. Ihre Typ-ID ist der Klassenname; die Klassen liegen in `net.kroia.stockmarket.pluginsystem.plugins`. Ihre `Settings`-Records und `DEFAULT_*`-Konstanten sind public. So kannst du die Standardwerte lesen oder Einstellungen bauen, zum Beispiel für `replaceCustomSettings`. Was jede Einstellung im Spiel bewirkt, steht auf der Admin-Seite des Plugins.

| Registry-Objekt | Klasse | Admin-Seite |
|---|---|---|
| `NET_FLOW_PLUGIN` | `NetFlowPlugin` | [Nettofluss-Plugin](../../../admin/stockmarket/plugins/net-flow.md) |
| `VOLATILITY_PLUGIN` | `VolatilityPlugin` | [Volatilitäts-Plugin](../../../admin/stockmarket/plugins/volatility.md) |
| `DEFAULT_ORDERBOOK_VOLUME_DISTRIBUTION_PLUGIN` | `DefaultOrderbookVolumeDistributionPlugin` | [Orderbuch-Volumen-Plugin](../../../admin/stockmarket/plugins/order-book-volume.md) |
| `TARGET_PRICE_BOT_PLUGIN` | `TargetPriceBot` | [Zielpreis-Bot](../../../admin/stockmarket/plugins/target-price-bot.md) |
| `NEWS_PLUGIN` | `NewsPlugin` | [News-Plugin](../../../admin/stockmarket/plugins/news.md) |

Eine neue Welt erstellt sie in der Reihenfolge dieser Tabelle, alle aktiviert. Zusammen bilden sie den Preis:

1. **NetFlowPlugin** ermittelt den fairen Preis aus dem abklingenden Spielerfluss und veröffentlicht ihn mit `setEquilibriumPrice`. Es setzt auch das Ziel auf den fairen Preis, aber nur, wenn in diesem Tick noch kein Plugin das getan hat.
2. **VolatilityPlugin** setzt das Ziel auf fairer Preis × (1 + zufällige Schwankung).
3. **DefaultOrderbookVolumeDistributionPlugin** formt die Bot-Orders um den fairen Preis.
4. **TargetPriceBot** liest `getPreviousTargetPrice()` und platziert Market-Orders in Richtung dieses Ziels, jeden 5. Tick, auf Märkten mit Bot-Orders.
5. **NewsPlugin** multipliziert das Ziel in `finalize`, solange News-Ereignisse laufen.

### Settings-Records { #settings-records }

| Klasse | `Settings`-Felder | Standardwerte und Hilfsmethoden |
|---|---|---|
| `NetFlowPlugin` | `flowEnabled`, `flowSensitivity`, `minPriceMult`, `maxPriceMult`, `permanentImpact`, `capacityVolatilityScale`, `thetaCapEnabled`, `saturationEnabled`, `anchorEnabled`, `anchorTimeDays`, `anchorMaxMovePerDay`, `anchorMinMult`, `anchorMaxMult` | `true`, `2000`, `0.05`, `3`, `0.5`, `0.3`, `true`, `true`, `true`, `2`, `0.1`, `0.25`, `4`. `Settings.createDefault()` und die Kopiermethoden `withPermanentImpact`, `withCapacityVolatilityScale`, `withToggles`, `withAnchor`, `withAnchorEnabled`. Ungültige Werte für `permanentImpact` und den Anker werden durch die Standardwerte ersetzt. |
| `VolatilityPlugin` | `volatilityScale` | `0.3` (`DEFAULT_VOLATILITY_SCALE`). `Settings.createDefault()`. |
| `DefaultOrderbookVolumeDistributionPlugin` | `volumeScale`, `speed`, `accumulationRate`, `decumulationRate`, `resetVolume`, `trendPeriodMinutes`, `trendGain`, `trendMaxFactor`, `roundLevelScale`, `roundLevelWidth`, `roundLevelRange`, `wallPeriodMinutes`, `wallDeadZone`, `wallStrength`, `wallCap` | `1`, `0.05`, `0.1`, `0.01`, dann Trend `10`, `10`, `4`, runde Preise `1`, `0.03`, `1.1`, Wand `2880`, `0.15`, `200`, `40`. `Settings.createDefault()`, `withTrend`, `withRoundLevels`, `withWall`. |
| `TargetPriceBot` | `pidP`, `pidI`, `pidD`, `pidRate`, `maxOrderVolumeFactor`, `maxTargetMovePerSecond`, `reversionTimeSeconds`, `oscillationPeriodSeconds`, `oscillationDamping`, `oscillationAmplitude`, `availableVolumeLevels`, `maxRampFraction` | `0.5`, `0.1`, `0`, `0.1`, `10`, `0.005`, `600`, `60`, `0.3`, `0.15`, `50`, `2`. `Settings.createDefault()`, `withReference`, `withAvailableVolumeLevels`, `withMaxRampFraction`. |
| `NewsPlugin` | `newsEnabled`, `sensitivity` | `true`, `1.0`. Alle laufenden Ereignisse zusammen werden zwischen `MIN_COMBINED_FACTOR` (0.1) und `MAX_COMBINED_FACTOR` (10) gehalten. |

### Hilfsmethoden { #helpers }

- **NetFlowPlugin** hat statische Hilfsmethoden für seine Formeln: `computeEquilibriumPrice`, `flowExponent`, `flowBand`, `capacity`, `stepAnchor`, `bookEFoldDepth`. Eine laufende Instanz liefert pro Markt: `getEquilibrium(ItemID)` (`NaN` vor dem ersten Update), `getAnchorMultiplier`, `getSaturatedFlow`, `getMarketSettings`, `getBookEFold`.
- **TargetPriceBot** hat statische Hilfsmethoden für seine Schritte: `anchorReference`, `stepReference`, `referenceAnchorPrice`, `limitTargetMove`, `botOrderVolumeLimit`, `rampFraction`, `crossesEmptyGap`. Auch seine Konstanten für das Preisband und die Pausen sind public: `BOT_MIN_PRICE_MULT` (0.25), `GAP_WINDOW_FRACTION` (0.01), `GAP_GUARD_MIN_BLOCK_SECONDS` und `GAP_GUARD_MAX_BLOCK_SECONDS` (eine zufällige Pause von 45 bis 75 Sekunden nach jeder ausgeführten Spieler-Order), `RAMP_START_FRACTION` (0.02) und `RAMP_SECONDS` (180).

## Einen StreamCodec schreiben { #writing-a-streamcodec }

Einstellungen und Live-Werte sind Records mit einem `public static final StreamCodec<ByteBuf, T> CODEC`. Server und Client verwenden denselben Codec, und das Framework übernimmt das gesamte Kodieren und Dekodieren. `StreamCodec` und `ByteBufCodecs` liegen in `net.minecraft.network.codec`, `ByteBuf` in `io.netty.buffer`.

Für ein paar einfache Felder ist `StreamCodec.composite` am kürzesten:

```java
public record Settings(float spread, float orderSize) {
    public static final StreamCodec<ByteBuf, Settings> CODEC = StreamCodec.composite(
            ByteBufCodecs.FLOAT, Settings::spread,
            ByteBufCodecs.FLOAT, Settings::orderSize,
            Settings::new
    );
}
```

Für mehr Felder oder Listen schreibst du den Codec selbst. Schreib zuerst die Länge einer Liste, dann jedes Element:

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

- **Prüfe die Werte im Record.** Der Server speichert die dekodierten Einstellungen, bevor er `onCustomSettingsApplied` aufruft. Korrigiere ungültige Werte in einem kompakten Konstruktor, damit sie nie gespeichert werden.
- **Halte alte Speicherstände lesbar.** Die Einstellungen werden mit dem Codec gespeichert. Fügst du später ein Feld hinzu, lies es nur, wenn noch Bytes übrig sind (`buf.isReadable()`), und nimm sonst einen Standardwert.

!!! warning "Derselbe Codec auf beiden Seiten"
    Client und Server müssen denselben Codec verwenden, Feld für Feld und in derselben Reihenfolge. Sonst kommen die Einstellungen verfälscht an oder lassen sich nicht dekodieren.

## Verwandte Seiten { #related-pages }

- [Das Plugin-System im Überblick](index.md): wann welche Methode aufgerufen wird.
- [Dein erstes Plugin](getting-started.md): diese Klassen in einem funktionierenden Plugin.
- [Beispiel-Plugins](examples.md): Live-Werte, Limit-Orders und Zustand pro Markt.
- [Marktzugriffs-API](../market-access-api.md): Märkte von außerhalb eines Plugins lesen und ändern.
