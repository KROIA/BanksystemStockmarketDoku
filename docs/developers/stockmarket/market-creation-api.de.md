---
title: "Marktintegrations-API"
description: "Märkte aus einer anderen Mod öffnen, schließen und pausieren und auf dem Client das Handelsfenster oder ein Preischart öffnen."
---

# Marktintegrations-API { #market-integration-api }

Mit dieser API kann eine andere Mod auf dem Server StockMarket-Märkte erstellen, löschen und pausieren und auf dem Client das Handelsfenster oder ein Live-Preischart zeigen. Sie liegt in `net.kroia.stockmarket.api.integration`.

| Klasse | Seite | Was sie macht |
|---|---|---|
| `IStockMarketIntegration` | Server-Thread, nur Master | Märkte erstellen, löschen und pausieren |
| `MarketConfig` | Server | Die Starteinstellungen eines neuen Markts |
| `MarketOpenResult` | Server | Das Ergebnis, wenn ein Markt erstellt wird |
| `StockMarketClientIntegration` | Client-Thread | Das Handelsfenster öffnen, ein Preischart einbetten |

Märkte werden über die `ItemID` von BankSystem (`net.kroia.banksystem.util.ItemID`) zugeordnet. Eine bekommst du mit `ItemID.of(itemStack)`.

## Die Integration holen { #getting-the-integration }

```java
IStockMarketIntegration markets = StockMarketMod.getAPI().getIntegration();
if (markets == null) {
    return;   // no server in this JVM, or it hasn't started yet
}
```

- `getIntegration()` gibt auf einem reinen Client und vor dem Serverstart `null` zurück. Du kannst sie bei jeder Nutzung gefahrlos neu holen.
- **Jede Methode darf nur auf dem Server-Thread laufen.** Von einem anderen Thread aus wechselst du zuerst auf den Server-Thread.
- **Sie funktioniert nur auf dem Master** (oder einem einzelnen Server), wo die Märkte liegen. Auf einem Slave leitet sie nichts an den Master weiter. Dort gibt `openMarket` `FAILED` zurück, `marketExistsFor` und `isMarketOpen` geben `false` zurück, und die anderen Methoden tun nichts.

## Einen Markt erstellen { #creating-a-market }

```java
MarketOpenResult.Result openMarket(ItemID subject, MarketConfig cfg);
```

Der Markt bekommt seine Einstellungen nur aus `cfg`. [Markt-Voreinstellungen](../../admin/stockmarket/presets.md) werden nicht verwendet, daher ist das Ergebnis auf jedem Server gleich.

`MarketConfig` ist ein Record:

| Feld | Typ | Standard | Bedeutung |
|---|---|---|---|
| `virtualOrderbookEnabled` | `boolean` | `true` | Bot-Orders im Orderbuch. `false` = nur Spieler-Orders. |
| `defaultPrice` | `float` | `1.0` | Startpreis, in dem Geld, das Spieler sehen (nicht roh). |
| `naturalAbundance` | `float` | `100.0` | Wie häufig das Item ist: bestimmt die Tiefe des Orderbuchs und die max. Ordergröße. |
| `ignorePluginAutosubscribe` | `boolean` | `false` | `true` = kein Plugin wird dem neuen Markt automatisch hinzugefügt. |

`MarketConfig.defaults()` liefert diese Standardwerte. Baue Configs mit dem Konstruktor oder mit `defaults()`; später können neue Felder dazukommen.

**Max. Ordergröße.** Die größte Spieler-Order eines neuen Markts ist `max(f, round(f × naturalAbundance))` Items. Dabei ist `f` der **Faktor max. Ordergröße** aus den [Mod-Einstellungen](../../admin/stockmarket/mod-settings.md) (standardmäßig 64). `defaults()` erlaubt also 6'400 Items pro Order, und Häufigkeit `0` erlaubt 64. Bot-Orders haben kein Limit.

### Ein normaler Markt { #a-normal-market }

Bot-Orders und die Standard-Plugins, wie bei einem Markt, den ein Admin erstellt:

```java
MarketOpenResult.Result result = markets.openMarket(subject, MarketConfig.defaults());
```

### Ein reiner Spielermarkt { #a-players-only-market }

Zum Beispiel für Unternehmensaktien, deren Preis nur Spieler bestimmen sollen. Setze **beide** Flags:

```java
MarketConfig shares = new MarketConfig(
        false,    // virtualOrderbookEnabled: no bot orders
        100.0f,   // defaultPrice
        0.0f,     // naturalAbundance: max order size 64
        true      // ignorePluginAutosubscribe: no plugins
);
MarketOpenResult.Result result = markets.openMarket(subject, shares);
```

Die beiden Flags sind unabhängig voneinander. Setzt du nur das erste, kommen trotzdem Plugins zum Markt und handeln darauf. Setzt du nur das zweite, geben die Bot-Orders dem Markt weiterhin Tiefe. `ignorePluginAutosubscribe` gilt nur beim Erstellen: Ein Admin kann dem Markt später trotzdem Plugins hinzufügen.

### Das Ergebnis { #the-result }

`openMarket` gibt nie `null` zurück. Das Ergebnis ist ein Record `Result(Status status, String reason)` mit `isSuccess()`:

| `Status` | Bedeutung |
|---|---|
| `SUCCESS` | Der Markt existiert jetzt. Verbundene Spieler sehen ihn sofort. `reason` ist `null`. |
| `ALREADY_EXISTS` | Für dieses Item gibt es schon einen Markt. Es hat sich nichts geändert, daher kannst du `openMarket` gefahrlos bei jedem Start aufrufen. |
| `ITEM_BLACKLISTED` | BankSystem lässt das Item nicht zu. |
| `FAILED` | Alles andere. `reason` sagt, warum, zum Beispiel auf einem Slave. |

```java
switch (result.status()) {
    case SUCCESS, ALREADY_EXISTS -> { }
    case ITEM_BLACKLISTED -> LOGGER.warn("Item not allowed: {}", result.reason());
    case FAILED -> LOGGER.error("Could not create market: {}", result.reason());
}
```

## Einen Markt prüfen und löschen { #checking-and-deleting-a-market }

```java
boolean marketExistsFor(ItemID subject);
void closeMarket(ItemID subject);
```

`closeMarket` **löscht** den Markt: Es storniert jede offene Spieler-Order und erstattet sie, entfernt den Markt aus allen Plugins und aus dem Fenster jedes Spielers. Gibt es keinen Markt, passiert nichts. Um ihn zurückzubekommen, rufst du `openMarket` erneut auf; der Preisverlauf ist dann weg.

## Einen Markt pausieren (Wartung) { #pausing-a-market-maintenance }

```java
void setMarketOpen(ItemID subject, boolean open);
void setMarketOpen(ItemID subject, boolean open, String reasonKey);
String getMarketCloseReason(ItemID subject);
boolean isMarketOpen(ItemID subject);
```

`setMarketOpen(subject, false)` versetzt den Markt in den [Wartungsmodus](../../admin/stockmarket/markets.md#maintenance-mode), `true` beendet ihn. Anders als bei `closeMarket` bleiben der Markt und sein Preisverlauf erhalten. Der Zustand wird mit der Welt gespeichert.

!!! warning "Wartung storniert Spieler-Orders"
    Das Pausieren storniert jede offene Spieler-Order auf dem Markt und erstattet sie. Spieler können keine neuen Orders platzieren, bis du die Wartung beendest, und die stornierten Orders kommen nicht zurück. Bot-Orders bleiben, und Bots handeln weiter.

- **Grund.** Mit `reasonKey` sehen Spieler deinen Text im Wartungsbanner des Markts statt des normalen Wartungstexts. Übergib einen Übersetzungsschlüssel aus deiner eigenen Sprachdatei. Wenn die Wartung endet, wird er gelöscht, auch wenn ein Admin oder ein Befehl sie beendet. `getMarketCloseReason` gibt den Schlüssel zurück, oder `null`.
- **`isMarketOpen`** ist nur `true`, wenn der Markt existiert und nicht in Wartung ist. Es beachtet die [Handelszeiten](../../admin/stockmarket/trading-hours.md) nicht: Ein Markt außerhalb seiner Zeiten gilt hier trotzdem als offen.
- Gibt es keinen Markt, tut `setMarketOpen` nichts.

## Wenn StockMarket nicht installiert ist { #when-stockmarket-isnt-installed }

Wenn deine Mod auch ohne StockMarket laufen soll, halte jeden StockMarket-Aufruf in einer eigenen Klasse. Greif auf diese Klasse erst zu, nachdem du geprüft hast, dass die Mod geladen ist. Sonst versucht Java, die StockMarket-Klassen zu laden, und deine Mod stürzt ab.

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

## Auf dem Client { #on-the-client }

`StockMarketClientIntegration` hat zwei statische Methoden für deinen Client-Code, zum Beispiel für ein Fenster über ein Unternehmen. Sie funktionieren auf jedem Server, auch auf einem Slave. Ruf sie auf dem Client-Thread auf (in einem Button-Handler oder in `init()`).

### Das Handelsfenster öffnen { #opening-the-trade-screen }

```java
static boolean openTradeScreen(ItemID market);
```

Öffnet das Handelsfenster von StockMarket mit diesem Markt ausgewählt, ohne Aktienmarkt-Block. Der Server prüft trotzdem jede Order.

- Gibt `false` zurück und tut nichts, wenn der Client den Markt nicht kennt: Er existiert nicht, oder der Spieler ist in keiner Welt.
- Sonst gibt sie `true` zurück, und das Fenster öffnet sich, wenn der Server antwortet. Ein Slave ohne Verbindung zu seinem Master lehnt ab, und der Spieler bekommt eine Chatnachricht. Ein geschlossener oder pausierter Markt öffnet sich und zeigt sein Banner.

### Ein Preischart einbetten { #embedding-a-price-chart }

```java
static GuiElement createPriceChart(ItemID market);
```

Erstellt ein Live-Kerzenchart des Markts als `GuiElement` von ModUtilities für dein eigenes Fenster. Ist der Markt noch nicht bekannt, bleibt das Chart leer und füllt sich, sobald er erscheint. Zoom und Position des Charts werden getrennt von denen des Handelsfensters gespeichert.

**Schließe es** in `removed()` deines Fensters, sonst laufen seine Preis-Updates für den Rest der Sitzung weiter:

```java
GuiElement chart = StockMarketClientIntegration.createPriceChart(shareItem);
addElement(chart);

@Override
public void removed() {
    try { ((AutoCloseable) chart).close(); } catch (Exception ignored) {}
    super.removed();
}
```

## Verwandte Seiten { #related-pages }

- [Marktzugriffs-API](market-access-api.md): Märkte und Preise lesen.
- [Märkte erstellen und verwalten](../../admin/stockmarket/markets.md): dieselben Aktionen im Admin-Fenster.
- [Dein Projekt einrichten](../setup.md): StockMarket zu deinem Build hinzufügen.
