---
title: "Marktzugriffs-API"
description: "Märkte lesen und Orders platzieren aus einer anderen Mod: Sync-, Async- und Client-APIs und fehlgeschlagene Anfragen."
---

# Marktzugriffs-API { #market-access-api }

Diese Seite zeigt, wie du aus einer anderen Mod Märkte, Preise und Orders liest und Orders für den Spieler platzierst. Die Interfaces liegen in `net.kroia.stockmarket.api` (`market`, `marketmanager`, `preset`, `pluginmanager`).

## Was deine Mod erreichen kann { #what-your-mod-can-reach }

| Du willst | Nutze | Wo |
|---|---|---|
| Märkte und Preise lesen oder Orders für den lokalen Spieler platzieren (ein HUD, dein eigenes Fenster) | Die Client-Manager | Client |
| Einen Markt erstellen, löschen oder pausieren | `IStockMarketIntegration`, siehe [Marktintegrations-API](market-creation-api.md) | Master-Server |
| Preise ändern oder Bot-Orders platzieren | Ein Plugin, siehe [Überblick über das Plugin-System](plugins/index.md) | Master-Server |

Auf dem Server gibt StockMarket seinen Markt-Manager nicht an andere Mods heraus: `StockMarketMod.getAPI()` hat nur `getModID()`, `getModVersion()` und `getIntegration()`. Die Sync- und Async-Interfaces weiter unten beschreiben, wie die Teile von StockMarket miteinander sprechen. Du begegnest ihnen über die Client-Manager und in Plugins.

## Auf dem Client { #on-the-client }

```java
StockMarketModBackend.ClientInstances client = StockMarketModBackend.getClientInstances();
if (client == null) return;   // not in a world
```

Der Halter wird erstellt, wenn der Spieler einer Welt beitritt, und auf `null` gesetzt, wenn er sie verlässt. Hol ihn jedes Mal neu, statt ihn aufzubewahren. Er hat drei Manager:

| Feld | Typ | Wer ihn nutzen darf |
|---|---|---|
| `MARKET_MANAGER` | `IClientMarketManager` | Jeder Spieler |
| `PLUGIN_MANAGER` | `IClientPluginManager` | Nur Admins; der Server weist andere Spieler ab |
| `PRESET_MANAGER` | `IAsyncPresetManager` | Nur Admins |

### Märkte lesen { #reading-markets }

`IClientMarketManager`:

| Methode | Was sie macht |
|---|---|
| `requestMarkets()` | Fragt den Server nach allen Märkten und aktualisiert die lokale Liste. `CompletableFuture<List<ItemID>>`. |
| `getAvailableMarkets()` | Die Liste aus dem letzten `requestMarkets()`. |
| `getMarket(ItemID)` | Der `ClientMarket` aus der lokalen Liste, oder `null`. |
| `requestPendingOrders(itemFilter, bankAccountNr, playerFilter, timeBegin, timeEnd)` | Offene Orders, gefiltert. |
| `getTradingCurrencyIDAsync()` | Das Geld-Item, gegen das die Märkte handeln. |
| `getCrossRateMarket(have, want)` | Preisdaten für ein Paar aus zwei Märkten (Preis von want ÷ Preis von have), für ein Chart. |
| `requestCreateMarket(ItemID)`, `requestDeleteMarket(ItemID)` | Nur Admins. |

Neue und gelöschte Märkte kommen von selbst in die lokale Liste; du musst `requestMarkets()` nicht erneut aufrufen.

`ClientMarket` liefert dir `getItemID()`, `getCurrentMarketPrice()` (roh), `getCurrentMarketRealPrice()` und `getTradingState()`: `OPEN`, `CLOSED` (außerhalb der Handelszeiten) oder `MAINTENANCE`. Ist der Zustand noch nicht bekannt, steht er auf `OPEN`; der Server lehnt Orders auf einem geschlossenen Markt trotzdem ab. `ClientMarket` implementiert außerdem `IPriceDataProvider` mit den Kerzen für ein Chart.

### Eine Order platzieren { #placing-an-order }

Die Order wird für den lokalen Spieler platziert, von einem Bankkonto, das er nutzen darf. Mengen und Preise sind reale Werte: Eine positive Menge kauft, eine negative Menge verkauft.

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

| Methode | Order |
|---|---|
| `createMarketBuyOrder(accountNr, volume)`, `createMarketSellOrder(accountNr, volume)` | Market-Order zum besten Preis |
| `createLimitBuyOrder(accountNr, volume, price)`, `createLimitSellOrder(accountNr, volume, price)` | Limit-Order zu einem Preis |
| `createMarketOrder(accountNr, volume)`, `createLimitOrder(accountNr, volume, price)` | Das Vorzeichen von `volume` entscheidet über Kauf oder Verkauf |
| `createOrder(accountNr, Order.Type, volume, price)` | Die allgemeine Form |

Die Verkaufsmethoden erwarten eine negative Menge, die Kaufmethoden eine positive; das falsche Vorzeichen wird zu 0 und abgelehnt. Die Varianten mit zwei Argumenten, `createLimitBuyOrder(accountNr, volume)` und `createLimitSellOrder(accountNr, volume)`, sind veraltet: Sie platzieren **Market**-Orders. Nutze `createMarketBuyOrder` und `createMarketSellOrder`.

### Warum eine Order abgelehnt wurde { #why-an-order-was-refused }

Der `status` der Antwort (`CreateOrderRequest.Status`) sagt, was passiert ist. Bei zwei davon enthält `detail` eine Zahl.

| Status | Bedeutung |
|---|---|
| `CREATED` | Die Order wurde platziert. |
| `NO_SUCH_MARKET` | Für das Item gibt es keinen Markt. |
| `INVALID_VOLUME`, `INVALID_PRICE` | Menge 0 oder ein negativer Preis. |
| `MARKET_CLOSED` | Der Markt ist in Wartung oder außerhalb seiner Handelszeiten. Es wurde nichts reserviert. |
| `ORDER_TOO_LARGE` | Über der max. Ordergröße des Markts. `detail` = das Limit in Items. |
| `TRADING_TOO_FAST` | Der Handels-Cooldown des Spielers ist noch nicht abgelaufen. `detail` = die verbleibenden Millisekunden. |
| `ACCOUNT_FROZEN` | Ein BankSystem-Admin hat das Bankkonto eingefroren. |
| `NO_BANK_ACCOUNT`, `NO_BANK_USER`, `NO_PERMISSION_TO_DEPOSIT`, `NO_PERMISSION_TO_WITHDRAW` | Der Spieler darf nicht von diesem Konto aus handeln. |
| `NOT_ENOUGH_MONEY`, `NOT_ENOUGH_ITEM` | Das Konto hat nicht genug. |
| Andere (`NO_ITEM_BANK`, `UNABLE_TO_LOCK_MONEY`, …) | Die Bank konnte das Geld oder die Items nicht reservieren. |

## Wenn eine Anfrage fehlschlägt { #when-a-request-fails }

Jede Anfrage, die über das Netzwerk geht, kann fehlschlagen: die Anfragen der Client-Manager, die Order-Methoden und jeder Async-Aufruf von einem Slave an seinen Master. Die Future endet dann **mit einer Exception**, und zwar mit einer von zwei Exceptions aus ModUtilities (`net.kroia.modutilities.networking.client_server.arrs`):

| Exception | Was passiert ist | Was du tun darfst |
|---|---|---|
| `RequestNotSentException` | Die Anfrage wurde nie gesendet, zum Beispiel weil der Slave nicht mit seinem Master verbunden ist. Es ist nichts passiert. | Melde einen einfachen Fehlschlag. Etwas rückgängig zu machen, das du selbst reserviert hast, ist sicher. |
| `RequestOutcomeUnknownException` | Sie wurde gesendet, aber es kam nicht rechtzeitig eine Antwort, oder die Verbindung brach ab. Die andere Seite hat sie vielleicht ausgeführt. | **Nie automatisch rückgängig machen, erstatten oder erneut senden.** Sag dem Nutzer, dass es vielleicht geklappt hat, und lies den Zustand neu. |

Behandle jede andere Exception wie ein unbekanntes Ergebnis. Anfragen von einem Client werden vor dem Senden nie geprüft, daher schlagen sie nur mit `RequestOutcomeUnknownException` fehl.

Callbacks bekommen die Ursache eventuell in einer `CompletionException` verpackt; pack sie aus:

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

- **Lesen:** Behalte bei einem Fehler den alten Wert oder zeige „nicht verfügbar“. Ein neuer Versuch später ist in Ordnung.
- **Schreiben und Orders:** Nie automatisch wiederholen.
- **Timeouts:** 30 Sekunden; 120 Sekunden für Preis-, Order- und Transaktionsverlauf.
- **Threads:** Die Future endet auf dem Spiel-Thread der Seite, die die Anfrage gesendet hat. Callbacks dürfen also auf das Spiel zugreifen.

Eine **Ablehnung** ist keine Exception: Die Future endet normal mit `false` oder `null`. Behandle `null` wie `false`. Beispiele: ein Spieler ohne Admin-Rechte oder ein Schreibzugriff von einem Slave, dem der Master nicht vertraut.

## Sync- und Async-Interfaces { #sync-and-async-interfaces }

Jeder StockMarket-Manager hat eine Sync-Seite und eine Async-Seite. Du wählst sie über eine Fassade:

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

| Seite | `getSync()` | `getAsync()` |
|---|---|---|
| Master oder einzelner Server | der echte Manager | dasselbe Objekt; Futures enden sofort |
| Slave, verbunden | `null` | schickt jeden Aufruf an den Master |
| Slave, nicht verbunden | `null` | schickt nichts; die Future endet sofort mit einem Ersatzwert |

Die Ersatzwerte eines nicht verbundenen Slaves sind `false`, `0`, eine leere Liste, `null` oder ein neues Standardobjekt. `isUnderMaintenanceAsync()` gibt `true` zurück, der Markt gilt also als geschlossen. Prüfe zuerst `hasAsyncAccess()`, wenn du „kein Master“ von „keine Daten“ unterscheiden musst.

Der Async-Markt (`IAsyncMarket`) liest den Standardpreis und den aktuellen Preis, das Volumen im Orderbuch, Limit-Orders, den Wartungszustand, die Einstellungen und die aktuelle Kerze. Er kann außerdem Orders platzieren, den Markt pausieren und Handelszeiten setzen. Sync-Aufrufe (`ISyncServerMarket`, `ISyncServerMarketManager`) gibt es nur auf dem Master, und sie müssen auf dem Server-Thread laufen.

## Rohe und reale Werte { #raw-and-real-values }

StockMarket speichert Preise und Mengen als ganze Zahlen (**roh**). Der **reale** Wert ist der Rohwert geteilt durch den Skalierungsfaktor des Items aus BankSystem: Geld und Items können Nachkommastellen haben. Methoden ohne `Real` im Namen verwenden Rohwerte. In Plugins rechnet `IPluginMarket` zwischen beiden um.

## Verwandte Seiten { #related-pages }

- [Marktintegrations-API](market-creation-api.md): Märkte erstellen, löschen und pausieren, Handelsfenster und Chart.
- [Entwickler](../index.md): welche API für welche Aufgabe.
- [Plugin-API-Referenz](plugins/api-reference.md): der Markt aus Sicht der Plugins.
