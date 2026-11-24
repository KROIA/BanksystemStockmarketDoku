---
title: "Das Plugin-System im Überblick"
description: "Aufbau und Lebenszyklus eines StockMarket-Plugins und wie es registriert wird."
---

# Das Plugin-System im Überblick { #plugin-system-overview }

Ein StockMarket-Plugin ist Server-Code, der in jedem Tick auf den Märkten läuft, die es abonniert hat. Die fünf Standard-Preis-Plugins sind ebenfalls Plugins, also kann deins dasselbe wie sie: den Zielpreis setzen, Orders platzieren und das Orderbuch formen. Admins fügen dein Plugin in der Plugin-Verwaltung hinzu und richten es pro Markt ein, genau wie die eingebauten Plugins.

Dieser Abschnitt hat vier Seiten:

- dieser Überblick: wie ein Plugin abläuft;
- [Dein erstes Plugin](getting-started.md): das Beispiel-Plugin Schritt für Schritt;
- [Plugin-API-Referenz](api-reference.md): jede Klasse und jede Methode;
- [Beispiel-Plugins](examples.md): drei vollständige Plugins als Vorlage.

## Die Teile eines Plugins { #the-parts-of-a-plugin }

| Teil | Seite | Was er tut |
|---|---|---|
| Eine Unterklasse von `ServerPlugin<TSettings, TRuntimeData>` | Server | Deine Logik. Sie bekommt in jedem Tick die abonnierten Märkte. |
| Ein Aufruf von `PluginRegistry.registerPlugin(...)` | Server und Client | Gibt dem Plugin-Typ eine ID, einen Namen und eine Beschreibung. Danach erscheint der Typ in der Liste **Plugin hinzufügen**. |
| Ein `TSettings`-Record mit einem `StreamCodec` (optional) | beide | Die Einstellungen eines Markts. Das Framework hält sie pro Markt vor, schickt sie an das Einstellungsformular und speichert sie. |
| Ein `TRuntimeData`-Record mit einem `StreamCodec` (optional) | beide | Live-Werte, die der Server an das offene Einstellungsformular streamt, zum Beispiel eine Statuszeile. |
| Eine Unterklasse von `PluginGuiElement<TSettings, TRuntimeData>` (optional) | Client | Das Einstellungsformular im Eintrag des Plugins oder ein eigener Bildschirm. |

Verwende `Void` für einen Typparameter, den du nicht brauchst: `ServerPlugin<MySettings, Void>` hat Einstellungen, aber keine Live-Daten.

## Wie ein Plugin einen Markt erreicht { #how-a-plugin-reaches-a-market }

Ein Plugin greift nie direkt auf einen Markt zu. Für jeden abonnierten Markt bekommt es ein `MarketInterface` mit zwei Teilen:

```text
your ServerPlugin
   │  update(markets), finalize(markets)
   ▼
MarketInterface              one per subscribed market
   ├── market    (IPluginMarket)     prices, target price, orders, player flow
   └── oderBook  (IPluginOrderBook)  orders in the book, volume, bot orders
   │  every change goes into a per-market cache
   ▼
market                       gets all cached changes after every plugin is done
```

Das Feld heißt wirklich `oderBook`, ohne das erste „r“.

## Ein Tick { #one-tick }

Der Plugin-Manager läuft auf dem Master-Server, im Server-Thread, einmal pro Server-Tick:

1. **Aktualisieren.** Von jedem aktivierten Plugin läuft `update(markets)`, von oben nach unten durch die Plugin-Liste.
2. **Abschließen.** Von jedem aktivierten Plugin läuft `finalize(markets)`, in derselben Reihenfolge.
3. **Anwenden.** Die Caches aller Märkte werden angewendet: Zielpreise, Orders und Änderungen am Orderbuch.

Daraus folgt:

- **Änderungen warten im Cache.** `getTargetPrice()` gibt das Ziel zurück, das ein Plugin über deinem in diesem Tick gesetzt hat. So bauen spätere Plugins auf früheren auf. Der Preis selbst bewegt sich erst, wenn die Orders in Schritt 3 angewendet werden.
- **Wer zuletzt schreibt, gewinnt.** Rufen zwei Plugins im selben Tick `setTargetPrice` auf, gewinnt das untere in der Liste. Verwende `isTargetPriceSetThisTick()`, wenn dein Plugin nur dann ein Ziel setzen soll, wenn es sonst keines getan hat. Admins sehen die Reihenfolge auf der [Seite Plugins](../../../admin/stockmarket/plugins/index.md#the-order-matters).
- **`finalize` sieht das Ergebnis aller.** Nutze es für Änderungen, die auf dem gemeinsamen Ergebnis aufsetzen, zum Beispiel einen Faktor auf den Zielpreis. Das News-Plugin arbeitet so. Rufe in `finalize` kein `setTargetPrice` auf: Das würde solche Faktoren überschreiben.
- **Geschlossene Märkte fehlen.** `update` und `finalize` bekommen nur die abonnierten Märkte, die gerade innerhalb ihrer Handelszeiten liegen. Märkte im Wartungsmodus sind dabei. `getMarketInterfaces()` gibt weiterhin alle abonnierten Märkte zurück.
- **Market-Orders werden zusammengezählt.** Alle Market-Orders, die Plugins in einem Tick auf einem Markt platzieren, werden addiert und als eine Order platziert.
- **Plugins teilen sich ein Zeitbudget.** Der Manager misst die Zeit jedes Plugins. Admins sehen sie im [Leistungsbalken](../../../admin/stockmarket/plugins/index.md#the-performance-bar). Halte `update` billig: Ein Plugin, das nur alle paar Sekunden etwas tut, kann pro Markt Ticks zählen und vorher zurückkehren.

## Lebenszyklus { #life-cycle }

<figure markdown="span">
  ![Die Aufrufe, die ein Plugin bekommt. Wenn es erstellt oder geladen wird: init, dann beim Laden der Welt onMarketSubscribed, onCustomSettingsApplied, load und onEnable. In jedem Tick, solange es aktiviert ist: update für jedes Plugin, finalize für jedes Plugin, danach werden die Änderungen angewendet. Zu anderen Zeiten: onMarketSubscribed, onCustomSettingsApplied, onEnable oder onDisable, save, onMarketUnsubscribed, und deInit nur, wenn ein Admin das Plugin löscht.](../../../assets/images/stockmarket/dev/plugin-lifecycle.svg){ width="600" }
</figure>

| Aufruf | Wann |
|---|---|
| Konstruktor | Die Registry erstellt eine Instanz: wenn ein Admin auf **Plugin hinzufügen** klickt, und für jede gespeicherte Instanz beim Laden der Welt. |
| `init()` | Direkt nachdem die Instanz erstellt wurde. Das Plugin hat noch keine Märkte. |
| `onMarketSubscribed(marketID)` | Dem Plugin wird ein Markt hinzugefügt: von einem Admin, durch Auto-Abo beim Erstellen eines neuen Markts oder beim Laden. Danach speichert das Framework `provideDefaultCustomSettings()` für diesen Markt. |
| `onCustomSettingsApplied(marketID, settings)` | Für einen Markt wurden Einstellungen gespeichert: die Standardwerte beim Abonnieren, ein **Anwenden** eines Admins, die gespeicherten Werte beim Laden oder dein eigener Aufruf von `replaceCustomSettings`. |
| `onEnable()` / `onDisable()` | Der Schalter **Aktiviert** ändert sich. |
| `update(markets)` / `finalize(markets)` | In jedem Tick, solange das Plugin aktiviert ist. |
| `save(tag)` / `load(tag)` | Wenn die Welt gespeichert und geladen wird. |
| `onMarketUnsubscribed(marketID)` | Ein Markt wird aus dem Plugin entfernt. Seine Einstellungen werden verworfen. |
| `deInit()` | Nur wenn ein Admin die Plugin-Instanz löscht. |

Eine neue Instanz startet **deaktiviert** und ohne Märkte. Name und Beschreibung kommen aus der Registry. Der Admin schaltet sie ein und fügt Märkte hinzu.

Beim Laden der Welt durchläuft jede gespeicherte Instanz diese Schritte:

1. Der Konstruktor und `init()` laufen.
2. Name, Beschreibung, **Logger** und **Auto-Abo** werden wiederhergestellt.
3. Die gespeicherten Märkte werden abonniert: `onMarketSubscribed` und die Standardeinstellungen für jeden Markt.
4. Die gespeicherten Einstellungen ersetzen die Standardwerte: `onCustomSettingsApplied` für jeden Markt.
5. `load(tag)` bekommt deine eigenen gespeicherten Daten.
6. Zuletzt wird das Plugin aktiviert, falls es aktiviert gespeichert wurde. `onEnable()` läuft.

!!! warning "deInit() läuft nicht, wenn der Server stoppt"
    Es läuft nur, wenn ein Admin das Plugin löscht. Verlass dich beim Speichern nicht darauf. Verwende `save(tag)` für Daten, die einen Neustart überstehen müssen.

## Speichern { #saving }

Das Framework speichert für jede Instanz: die Instanz-ID, den Namen, die Beschreibung, die Schalter, die abonnierten Märkte und die Einstellungen jedes Markts (geschrieben mit deinem Settings-Codec). Deine Methoden `save(tag)` und `load(tag)` sind nur für zusätzliche Daten da, etwa Werte, die das Plugin mit der Zeit ermittelt hat.

Hat beim Laden der Welt eine gespeicherte Instanz einen Plugin-Typ, der nicht registriert ist, überspringt der Manager sie. Das Log meldet das nur, wenn in der Plugin-Verwaltung der **Plugin-Manager-Logger** eingeschaltet ist. Beim nächsten Speichern sind diese Instanz und ihre Daten weg. Das passiert, wenn die Plugin-Mod fehlt, und auch, wenn du die Typ-ID änderst. Die übliche Typ-ID ist der Klassenname. Verschiebst du die Plugin-Klasse oder benennst sie um, gehen deshalb alle gespeicherten Instanzen verloren.

## Registrieren { #registering }

Registriere den Plugin-Typ einmal, in gemeinsamem Code, der auf dem Server und auf dem Client läuft:

```java
public static final PluginRegistryObject MY_PLUGIN = PluginRegistry.registerPlugin(
        MyPlugin.class.getName(),   // type ID: unique, never change it
        "MyPlugin",                 // name in the plugin list
        "What the plugin does.",    // description in the Add Plugin list
        MyPlugin::new               // creates a new instance
);
```

Setze das Einstellungsformular nur auf dem Client, damit dedizierte Server nie Client-Klassen laden:

```java
public static void clientSetup() {
    MY_PLUGIN.setGuiElementFactory(MyPluginGuiElement::new);
}
```

Wo das Plugin installiert sein muss:

- **Server.** Plugins laufen nur auf dem Master-Server. Bei einem einzelnen Server ist das der Server selbst.
- **Client.** Die Liste **Plugin hinzufügen** kommt aus der Registry des Clients, und der Client baut das Einstellungsformular. Ein Admin ohne deine Mod sieht im Eintrag des Plugins *Plugin-Mod nicht installiert — eigene Oberfläche nicht verfügbar*.

## Was ein Plugin kann { #what-a-plugin-can-do }

| Aufgabe | Verwende |
|---|---|
| Den Zielpreis setzen oder verschieben | `setTargetPrice`, `addToTargetPrice`, `isTargetPriceSetThisTick` in [IPluginMarket](api-reference.md#ipluginmarket) |
| Einen fairen Preis mit anderen Plugins teilen | `setEquilibriumPrice`, `getEquilibriumPrice` |
| Den Standardpreis dauerhaft ändern | `setDefaultRealPrice` |
| Market- oder Limit-Orders platzieren | `placeOrder(amount)`, `placeOrder(amount, price)` |
| Angebot und Nachfrage der Spieler lesen | `getFadedNetPlayerItemFlow`, `getNetPlayerItemFlow` |
| Das Orderbuch lesen | `getRealVolume`, `getRealVirtualVolume`, `getCapital`, `getBuyOrders`, `getSellOrders` in [IPluginOrderBook](api-reference.md#ipluginorderbook) |
| Eine Order so bemessen, dass sie einen Preis nicht überschreitet | `getRealVirtualVolumeToPrice`, `getRealVirtualAvailableVolume` |
| Die Bot-Orders im Buch ändern | `setRawVolume`, `addRawVolume`, `resetVirtualVolume`, `registerDefaultVolumeDistributionCalculator` |
| Einstellungen pro Markt behalten | `customSettingsCodec`, `provideDefaultCustomSettings`, `getCustomSettings` in [ServerPlugin](api-reference.md#serverplugin) |
| Live-Werte an das Einstellungsformular streamen | `runtimeDataCodec`, `provideRuntimeData` |
| Ein Einstellungsformular oder einen Bildschirm zeigen | eine Unterklasse von [PluginGuiElement](api-reference.md#pluginguielement) |
| Auf den Chart der Plugin-Verwaltung zeichnen | [Chart-Overlays](api-reference.md#chart-overlays) |

## Verwandte Seiten { #related-pages }

- [Dein erstes Plugin](getting-started.md): das Beispiel-Plugin Schritt für Schritt bauen.
- [Plugin-API-Referenz](api-reference.md): jede Methode im Detail.
- [Plugins](../../../admin/stockmarket/plugins/index.md): wie Admins Plugins hinzufügen, anordnen und einrichten.
- [Marktzugriffs-API](../market-access-api.md): Märkte von außerhalb eines Plugins lesen und ändern.
