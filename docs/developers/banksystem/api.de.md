---
title: "BankSystem-API"
description: "Einstiegspunkt, Bankkonten, synchroner und asynchroner Zugriff, Geldformatierung und Auszahlungen."
---

# BankSystem-API { #banksystem-api }

Diese Seite zeigt, wie eine andere Mod Bankkonten von BankSystem liest und ändert. Alles beginnt bei `BankSystemAPI`. Alle öffentlichen Typen liegen im Package `net.kroia.banksystem.api` und seinen Unterpackages. Wie du BankSystem in deinen Build aufnimmst, steht unter [Projekt einrichten](../setup.md).

## Der Einstiegspunkt { #the-entry-point }

```java
BankSystemAPI api = BankSystemMod.getAPI();
```

| Methode | Rückgabewert | Was du damit bekommst |
|---|---|---|
| `getModID()` / `getModVersion()` | `String` | Die Mod-ID von BankSystem und die geladene Version. |
| `getServerBankManager()` | `IBankManager` | Die Bankkonten auf diesem Server, synchron und asynchron. `null`, bevor der Server gestartet ist und nachdem er gestoppt wurde, prüfe das also. Siehe [Synchron oder asynchron](#sync-or-async). |
| `getClientBankManager()` | `IClientBankManager` | Bankdaten auf der Client-Seite. Siehe [Auf dem Client](#on-the-client). |
| `getEvents()` | `IBankSystemEvents` | Events und Signale. Siehe [Events und Signale](events.md). |
| `getDataHandler()` | `IBankSystemDataHandler` | Speichert und lädt die Daten von BankSystem (`saveAll`, `loadAll`, `save_bank`, `load_bank`, `save_globalSettings`, `load_globalSettings`; jede Methode gibt bei Erfolg `true` zurück). Ruf ihn auf dem Server-Thread auf. BankSystem speichert nach einem eigenen Zeitplan und beim Herunterfahren, du brauchst ihn also selten. |
| `isSlave()` | `boolean` | Ob dieser Server ein Slave in einem Netzwerk ist. |
| `getLedger()` | `ITransactionLedger` | Schreibt Einträge ins Transaktionsbuch. Nur auf dem Master. Siehe [Transaktionsbuch](transaction-ledger.md). |
| `getNoteFlowLog()` | `INoteFlowLog` | Zeichnet Geld-Items auf, die außerhalb der Bank entstehen oder vernichtet werden. Siehe [Banknotenfluss-Protokoll](#note-flow-log). |
| `setItemPriceProvider(…)` / `getItemPriceProvider()` | `void` / `ItemPriceProvider` (kann null sein) | Item-Preise für das Gesamtvermögen. Siehe [Item-Preisanbieter](item-price-provider.md). |
| `setPriceCurrencyItem(short)` / `getPriceCurrencyItem()` | `void` / `short` | Das Item, in dem diese Preise angegeben sind. |
| `registerCurrencyProvider(…)` / `unregisterCurrencyProvider(String)` | `void` / `boolean` | Fügt einen Adapter für eine Währungs-Mod hinzu oder entfernt ihn. Siehe [Währungsintegration](currency-integration.md). |
| `getCurrencyProviders()` / `getCurrencyProvider(String)` | `Collection<…>` / kann null sein | Die registrierten Währungsadapter. Eingebaute Adapter, die der Admin abgeschaltet hat, fehlen darin. |
| `getPayoutManager()` / `getDividendPayer()` | `IPayoutManager` / `IDividendPayer` | Auszahlungen und Dividenden von Unternehmen. Nur auf dem Master. Siehe [API für Unternehmen, Auszahlungen und Dividenden](companies-api.md). |
| `getVisualLookup()` / `getShareIconRenderer()` | `IBankSystemVisualLookup` / `IShareIconRenderer` (kann null sein) | Das Aktien-Design auf dem Client. Siehe [API für Unternehmen, Auszahlungen und Dividenden](companies-api.md#share-visuals-on-the-client). |

## Wie die Daten aufgebaut sind { #how-the-data-is-organised }

```text
Bank manager                      all accounts on the server
 └─ Bank account                  one account number, a name, an icon
     ├─ Users                     players with rights on the account
     └─ Banks                     one per item: money, diamonds, ...
         ├─ money    balance 1500, locked 200
         └─ diamond  balance 64,   locked 0
```

- Ein **Bankkonto** hat eine eindeutige Kontonummer. Jeder Spieler bekommt ein persönliches Konto. Spieler können weitere Konten anlegen und mit anderen Spielern teilen.
- Jeder Nutzer eines Kontos hat Rechte, gespeichert als Bit-Flags aus `BankPermission`: `DEPOSIT` (1), `WITHDRAW` (2) und `MANAGE` (4).
- Eine **Bank** enthält den Kontostand eines Items in einem Konto. Du holst zuerst das Konto und dann die Bank für das Item.
- Items werden über `ItemID` (`net.kroia.banksystem.util`) erkannt. `MoneyItem.getItemID()` liefert das Geld-Item.

## Synchron oder asynchron { #sync-or-async }

`IBankManager` bietet zwei Zugänge:

```java
IBankManager bankManager = api.getServerBankManager();

bankManager.hasSyncAccess();   // true on the master and on a single server
bankManager.hasAsyncAccess();  // true on the master, and on a slave while it is connected

IServerBankManager sync = bankManager.getSync();  // null on a slave
IAsyncBankManager async = bankManager.getAsync(); // always there
```

| | Synchron (`getSync()`) | Asynchron (`getAsync()`) |
|---|---|---|
| Läuft auf | dem Master und Einzelservern | dem Master und verbundenen Slaves |
| Rückgabewert | Werte direkt | `CompletableFuture<T>` |
| Nimm es, wenn | dein Code nur auf dem Master läuft | dein Code auf einem Slave laufen kann |
| Kann fehlschlagen | Nein, es gibt einen Status zurück | Auf einem Slave ja. Siehe [Wenn ein asynchroner Aufruf fehlschlägt](#when-an-async-call-fails) |

**Nimm den asynchronen Zugang, außer du weißt sicher, dass du auf dem Master bist.** Er funktioniert überall. Auf dem Master laufen asynchrone Aufrufe lokal und sind sofort abgeschlossen.

`getSync()` gibt einen `IServerBankManager` zurück, der die synchronen und die asynchronen Methoden hat. Ruf keine von beiden auf der Client-Seite auf.

### Wer was lesen darf { #who-may-read-what }

Asynchrone Lesezugriffe auf Kontodaten sind Kontomitgliedern, BankSystem-Admins und serverinternen Aufrufen (Aufrufen ohne Spieler als Absender) erlaubt. Eine Anfrage, die über einen nicht vertrauenswürdigen Slave kommt, bekommt nur die Daten für Mitglieder, weil ein Slave den Absender fälschen könnte. Ein abgelehnter Lesezugriff auf Kontodaten wird mit `null`, einer leeren Liste oder einer Kopie nur mit Namen abgeschlossen. Ein abgelehnter Lesezugriff auf den Kontostand einer Bank (`getBalanceAsync`, `getLockedBalanceAsync`, `getTotalBalanceAsync` und ihre `Real`-Varianten) wird mit `0` oder `0.0` abgeschlossen und sieht damit wie eine leere Bank aus. Andere abgelehnte Lesezugriffe auf eine Bank, etwa formatierte Kontostände oder JSON, werden mit `null` abgeschlossen. Clients können Kontostände nie ändern: Einzahlungen, Abhebungen und Überweisungen müssen von Servercode auf dem Master oder einem vertrauenswürdigen Slave kommen.

### Wenn ein asynchroner Aufruf fehlschlägt { #when-an-async-call-fails }

Auf einem Slave gehen asynchrone Aufrufe an den Master, und die Antwort kann verloren gehen. BankSystem schaltet in ModUtilities Anfragefehler für die ganze Spielinstanz ein (`RequestManager.ENABLE_REQUEST_FAILURES = true`). Das betrifft die Anfragen aller Mods, nicht nur die von BankSystem: Eine Anfrage ohne Antwort lässt ihr Future fehlschlagen, statt ewig zu warten.

| Was passiert ist | Was du bekommst |
|---|---|
| Der Slave ist nicht mit dem Master verbunden | Das Future wird sofort mit einem Ersatzwert abgeschlossen: `FAILED_NO_MASTER_CONNECTION` bei `BankStatus`-Aufrufen, sonst `false`, `0`, `""`, eine leere Liste oder `null`. Es wurde nichts gesendet. |
| Die Anfrage konnte nicht gesendet werden | Schlägt mit `RequestNotSentException` fehl. Nichts hat den Master erreicht, **eine Erstattung ist also sicher**. |
| Keine Antwort in der Zeit, oder die Verbindung ist abgebrochen | Schlägt mit `RequestOutcomeUnknownException` (einer `TimeoutException`) fehl. Der Master **hat den Aufruf vielleicht ausgeführt**. Erstatte nicht blind und wiederhole nicht blind. |
| Der Master hat die Anfrage abgelehnt | Wird meist mit `null` abgeschlossen. Behandle `null` als Fehlschlag. |

Beide Exceptions liegen in `net.kroia.modutilities.networking.client_server.arrs`. Das Timeout beträgt 30 Sekunden (`RequestManager.DEFAULT_TIMEOUT_MS`). Langsame Lesezugriffe wie Audit-Seiten und der Kontostandsverlauf warten 150 Sekunden.

**Einzahlungen und Abhebungen von einem Slave** (`deposit*Async`, `withdraw*Async`) tragen eine Transfer-ID. Geht ihre Antwort verloren, fragt der Slave beim Master nach, ob der Aufruf ausgeführt wurde:

- ausgeführt: wird mit `SUCCESS` abgeschlossen;
- nicht ausgeführt oder nie gesendet: wird mit `FAILED_NO_MASTER_CONNECTION` abgeschlossen. Dieser Status bedeutet immer, dass sich nichts geändert hat, ein Zurückrollen ist also sicher;
- weiter unbekannt: schlägt mit `RequestOutcomeUnknownException` fehl. Erstatte nichts.

Der Master führt jede Transfer-ID höchstens einmal aus. Überweisungen, Reservierungen, Freigaben und Aufrufe, die den Kontostand setzen, bekommen diese Prüfung nicht: Geht ihre Antwort verloren, schlagen sie mit `RequestOutcomeUnknownException` fehl.

```java
// The player's items were already taken out of the world; put them in the bank.
bank.depositAsync(amount).whenComplete((status, ex) -> {
    if (ex != null) {
        Throwable cause = ex instanceof CompletionException && ex.getCause() != null ? ex.getCause() : ex;
        if (cause instanceof RequestNotSentException) giveItemsBack(); // never reached the master
        else log("deposit outcome unknown, items kept: " + cause);    // may have been applied
        return;
    }
    if (status != BankStatus.SUCCESS) giveItemsBack();                // any other status: nothing changed
});
```

## Ein Konto und eine Bank holen { #getting-an-account-and-a-bank }

```java
IAsyncBankManager manager = api.getServerBankManager().getAsync();

manager.getBankAccountAsync(accountNumber).thenCompose(account -> {
    if (account == null)                       // no such account
        return CompletableFuture.completedFuture(null);
    return account.getBankAsync(itemID);       // null if the account has no bank for this item
}).thenAccept(bank -> {
    if (bank != null) { /* use the IAsyncBank */ }
});
```

Nützliche Abfragen auf `IAsyncBankManager` (jede hat auf `ISyncServerBankManager` einen synchronen Zwilling ohne `Async`):

| Methode | Rückgabewert |
|---|---|
| `getBankAccountAsync(int accountNumber)` | Das Konto oder `null` |
| `getPersonalBankAccountAsync(UUID)` / `(String name)` | Das persönliche Konto eines Spielers oder `null` |
| `getOrCreatePersonalBankAccountAsync(UUID)` | Das persönliche Konto, angelegt, falls es fehlt |
| `getBankAccountsAsync(UUID)` | Jedes Konto, in dem der Spieler Mitglied ist |
| `getPersonalBankAsync(UUID owner, ItemID)` / `getOrCreatePersonalBankAsync(…)` | Eine Bank des persönlichen Kontos |
| `bankAccountExistsAsync(int)` / `isAccountFrozenAsync(int)` | Ob das Konto existiert oder eingefroren ist |
| `isItemIDAllowedAsync(ItemID)` / `getAllowedItemsAsync()` | Welche Items in die Bank dürfen |
| `getItemFractionScaleFactorAsync()` | Roh-Einheiten pro Item, `100` |
| `isSlaveServerTrustedAsync(String slaveID)` | Ob ein Slave vertrauenswürdig ist. Siehe [Ist dieser Slave vertrauenswürdig?](#is-this-slave-trusted) |

## Mit einer Bank arbeiten (`IAsyncBank`) { #working-with-a-bank-iasyncbank }

Jede Methode gibt ein `CompletableFuture` zurück und funktioniert auf dem Master und auf Slaves gleich.

### Rohbeträge und echte Beträge { #raw-and-real-amounts }

Banken speichern Beträge als `long` in **Roh-Einheiten**. Ein Item sind 100 Roh-Einheiten, Geld behält also zwei Nachkommastellen: `150` roh sind `1.50`. Methoden mit `Real` im Namen nehmen oder liefern stattdessen den `double`-Wert.

```java
bank.depositAsync(150L);       // deposits 1.50
bank.depositRealAsync(1.50);   // the same
```

### Kontostände { #balances }

| Methode | Rückgabewert |
|---|---|
| `getBalanceAsync()` / `getRealBalanceAsync()` | Der freie Kontostand |
| `getLockedBalanceAsync()` / `getRealLockedBalanceAsync()` | Der reservierte Kontostand |
| `getTotalBalanceAsync()` / `getRealTotalBalanceAsync()` | Frei plus reserviert |
| `hasSufficientFundsAsync(long)` | Ob der freie Kontostand den Betrag deckt |
| `getMinimalDataAsync()` | Item-ID, Kontostand und reservierter Kontostand in einem `BankData` |
| `getItemIDAsync()` | Das Item (direkt zurückgegeben, nicht als Future) |

### Den Kontostand ändern { #changing-the-balance }

| Methode | Was sie tut |
|---|---|
| `depositAsync(long)` / `depositRealAsync(double)` | Erhöht den freien Kontostand |
| `withdrawAsync(long)` / `withdrawRealAsync(double)` | Nimmt vom freien Kontostand |
| `withdrawLockedAsync(long)` / `withdrawLockedRealAsync(double)` | Nimmt nur vom reservierten Kontostand |
| `withdrawLockedPreferedAsync(long)` / `withdrawLockedPreferedRealAsync(double)` | Nimmt zuerst vom reservierten, dann vom freien Kontostand |
| `transferAsync(long, int toAccount)` / `transferRealAsync(…)` | Verschiebt freien Kontostand in die Bank desselben Items in einem anderen Konto |
| `transferFromLockedAsync(…)` / `transferFromLockedPreferedAsync(…)` | Dasselbe vom reservierten Kontostand (mit `Real`-Varianten) |
| `setBalanceAsync(long)` / `setRealBalanceAsync(double)` | Setzt den Kontostand; gibt `Boolean` zurück. Für Admin-Tools. |

### Reservieren { #locking }

Reservieren hält einen Betrag für etwas zurück, das noch nicht abgeschlossen ist, zum Beispiel eine offene Order auf dem Markt. Reserviertes Geld kann nicht zweimal ausgegeben werden.

```java
bank.lockAmountAsync(amount);              // 1. reserve it when the order is placed
bank.withdrawLockedPreferedAsync(amount);  // 2a. take it when the order fills
bank.unlockAmountAsync(amount);            // 2b. or release it when the order is cancelled
```

Nimm `withdrawLockedPreferedAsync` statt `withdrawLockedAsync`: Es funktioniert auch dann, wenn ein Admin in der Zwischenzeit einen Teil des reservierten Betrags freigegeben hat. `unlockAllAsync()` gibt alles frei. Auch die Aufrufe zum Reservieren und Freigeben haben `Real`-Varianten.

### Formatierung { #formatting }

| Methode | Rückgabewert |
|---|---|
| `getNormalizedBalanceAsync()` (auch `…Locked…`, `…Total…`) | Der Kontostand mit kurzem Suffix: `1.5k`, `2M` |
| `getFormattedBalanceAsync()` (auch `…Locked…`, `…Total…`) | Der Kontostand mit Tausendertrennzeichen: `15'649'864` |
| `getNormalizedAmountAsync(…)` / `getFormattedAmountAsync(…)` | Ein beliebiger Betrag, roh (`long`) oder echt (`double`) |
| `convertToRawAmountAsync(double)` / `convertToRealAmountAsync(long)` | Rechnet zwischen roh und echt um |
| `getItemNameAsync()` | Der Anzeigename des Items |
| `toJsonAsync()` / `toJsonStringAsync()` | Die Bank als JSON |

### Bankstatus { #bank-status }

Jede Änderung gibt einen `BankStatus` zurück. Alles außer `SUCCESS` bedeutet, dass sich nichts geändert hat.

| Wert | Bedeutung |
|---|---|
| `SUCCESS` | Erledigt. |
| `FAILED_NOT_ENOUGH_FUNDS` | Der freie oder der reservierte Kontostand deckt den Betrag nicht. |
| `FAILED_OVERFLOW` | Der neue Kontostand würde überlaufen. |
| `FAILED_NEGATIVE_VALUE` | Es wurde ein negativer Betrag übergeben. |
| `FAILED_WRONG_INSTANCE_TYPE` | Intern: Die Zielbank ist keine Server-Bank. |
| `FAILED_INVALID_ITEM_ID` | Die Item-ID ist ungültig. |
| `FAILED_NO_BANK` | Das Konto hat keine Bank für dieses Item, zum Beispiel das Ziel einer Überweisung. |
| `FAILED_NO_MASTER_CONNECTION` | Nur auf einem Slave: Der Master wurde nicht erreicht, oder er meldet, dass der Aufruf nicht ausgeführt wurde. Es hat sich nichts geändert. |
| `FAILED_EXTERNAL_UNAVAILABLE` | Die Bank ist an eine Währungs-Mod gebunden, die gerade nicht verfügbar ist. |
| `FAILED_ACCOUNT_FROZEN` | Das Konto ist eingefroren, und der Aufruf war eine Spieleraktion. |

## Mit einem Konto arbeiten (`IAsyncBankAccount`) { #working-with-an-account-iasyncbankaccount }

| Methode | Was sie tut |
|---|---|
| `getAccountNumberAsync()` | Die Kontonummer (direkt zurückgegeben) |
| `getAccountNameAsync()` / `setAccountNameAsync(String)` | Der Kontoname |
| `getAccountIconAsync()` / `setAccountIconAsync(ItemID)` | Das Symbol oder `null` |
| `getAccountDataAsync()` | Ein `BankAccountData`-Schnappschuss des ganzen Kontos |
| `addUserAsync(User, int permission)` / `removeUserAsync(UUID)` / `setUsersAsync(Map<User, Integer>)` | Die Mitglieder und ihre Rechte |
| `getPermissionAsync(UUID)` / `setPermissionAsync(UUID, int)` | Die Rechte-Flags eines Mitglieds |
| `hasPermissionAsync(UUID, BankPermission)` | Ob ein Mitglied ein bestimmtes Recht hat |
| `getPersonalBankOwnerAsync()` | Der Besitzer eines persönlichen Kontos oder `null` |
| `getBankAsync(ItemID)` / `getOrCreateBankAsync(ItemID)` | Eine Bank |
| `createBankAsync(ItemID, long startBalance)` | Legt eine Bank an oder gibt die vorhandene zurück |
| `getAllBanksAsync()` | Alle Banken als `Map<ItemID, IAsyncBank>` |
| `removeBankAsync(ItemID)` / `removeAllBanksAsync()` | Löscht Banken. **Der Kontostand geht verloren.** |
| `removeEmptyBanksAsync()` | Löscht Banken mit Kontostand null und gibt ihre Items zurück |

### Ein Konto beobachten (Master) { #watching-an-account-master }

```java
// ISyncServerBankAccount
void subscribeBankChanges(Consumer<BankAccountData> callback);
void unsubscribeBankChanges(Consumer<BankAccountData> callback);
// ISyncServerBankManager: the same by account number (does nothing if the account doesn't exist)
void subscribeBankChanges(int accountNr, Consumer<BankAccountData> callback);
void unsubscribeBankChanges(int accountNr, Consumer<BankAccountData> callback);
```

Nach einer Änderung am Konto bekommt der Callback einen Schnappschuss auf dem Server-Thread, höchstens einmal pro Tick. Dieselbe Instanz zweimal zu abonnieren bewirkt nichts; melde dich mit derselben Instanz wieder ab. Abonnements werden nicht gespeichert, abonniere also nach einem Neustart erneut.

### Eingefrorene Konten { #frozen-accounts }

Admins können ein Konto einfrieren. Solange es eingefroren ist, lehnt der Master Spieleraktionen darauf (Einzahlungen, Abhebungen, Überweisungen, Konverter, Upload- und Download-Blöcke, Crafting, Aktienhandel) mit `FAILED_ACCOUNT_FROZEN` ab.

```java
// ISyncServerBankManager (master)
boolean isAccountFrozen(int accountNumber);
boolean setAccountFrozen(int accountNumber, boolean frozen, LedgerActor actor); // false = no such account
// IAsyncBankManager (master and slaves)
CompletableFuture<Boolean> isAccountFrozenAsync(int accountNumber);
```

Eine echte Änderung schreibt einen `ACCOUNT_FREEZE`-Eintrag ins Transaktionsbuch und löst [`getAccountFreezeChangedEvent()`](events.md#account-freezes) aus. Den aktuellen Zustand erneut zu setzen bewirkt nichts.

!!! warning "Rohe Bank-Aufrufe ignorieren das Einfrieren"
    Einfache `deposit`-, `withdraw`-, Reservierungs- und Freigabe-Aufrufe ohne Typ für das Transaktionsbuch sowie Änderungen durch Admins gehen auf einem eingefrorenen Konto weiterhin durch. Wenn deine Mod Guthaben eines Spielers bewegt, prüfe zuerst `isAccountFrozen(Async)`.

### Einen Nutzer entfernen { #removing-a-user }

`removeUser(UUID)` (synchron) und `removeUserAsync(UUID)` löschen den Nutzer, sein persönliches Konto und jedes Konto, das danach keine Nutzer mehr hat. Unternehmenskonten bleiben erhalten. Die Kontostände bekommt der Spieler als Items: zuerst auf diesem Server, dann auf jedem Slave. Was sich nicht ausliefern lässt, wird vernichtet und als `ACCOUNT_DELETE_LOSS` verbucht; der Rest wird als `ACCOUNT_DELETE_PAYOUT` verbucht.

Beide kehren zurück, bevor feststeht, ob die Auslieferung geklappt hat. `true` bedeutet nur, dass der Nutzer existierte und entfernt wurde.

## Auf dem Client { #on-the-client }

`api.getClientBankManager()` liest Bankdaten von dem Server, mit dem der Spieler verbunden ist. Dieser Server kann die Anfrage an den Master weiterreichen. Kontodaten gehen nur an Kontomitglieder und BankSystem-Admins: Ein abgelehnter Lesezugriff wird mit `null` oder einer leeren Liste abgeschlossen, eine abgelehnte Änderung mit `false`.

| Methode | Rückgabewert |
|---|---|
| `getBankAccountDataAsync(int)` | Ein Konto oder `null` |
| `getPersonalBankAccountDataAsync(UUID)` | Das persönliche Konto eines Spielers oder `null` |
| `getBankAccountsDataAsync(UUID)` | Die Konten des Spielers, die der Betrachter lesen darf |
| `getBankManagerDataAsync()` | Nutzer und Konten: vollständige Daten für Admins, für alle anderen nur die Namen |
| `getItemInfoDataAsync(ItemID)` | Serverweite Summen und Besitzer eines Items |
| `allowItemIDAsync(ItemID)` / `disallowItemIDAsync(ItemID)` | Nur für Admins. Das Verbieten löscht den Kontostand des Items bei allen Besitzern, ohne Erstattung. |
| `deleteBankAccountAsync(int)` | Admins oder Mitglieder mit `MANAGE` |
| `isServerTrustedAsync()` | `false`, wenn dieser Server ein Slave ist, dem der Master nicht vertraut |
| `requestUpdateBankAccount(…)` | Ändert Name, Symbol, Mitglieder oder Rechte (braucht `MANAGE`); `null`, wenn abgelehnt |
| `requestRemoveEmptyBanks(int)` | Entfernt leere Banken und gibt ihre Items zurück |
| `requestBalanceHistory(int[, long fromMs, long toMs, int maxPoints])` | Der Kontostandsverlauf; nur für Mitglieder und Admins |
| `requestAllowdItems()` | Jedes Item, das in die Bank darf |
| `getUserCustomData()` / `updateUserCustomData(CompoundTag)` | Die eigenen UI-Einstellungen des Spielers, auf dem Server gespeichert |
| `getItemFractionScaleFactor()` / `convertToRawAmount(double)` / `convertToRealAmount(long)` | Umrechnungen mit dem zwischengespeicherten Faktor (frag ihn einmal mit `getItemFractionScaleFactorAsync()` ab) |

## Ist dieser Slave vertrauenswürdig? { #is-this-slave-trusted }

Der Master lehnt Änderungen ab, die über einen nicht vertrauenswürdigen Slave kommen. So prüfst du das im Code:

- auf einem Client: `getClientBankManager().isServerTrustedAsync()`;
- auf einem Server: `getServerBankManager().getAsync().isSlaveServerTrustedAsync("")`. Die leere ID fragt nach dem Server, über den die Anfrage kommt: `true` auf dem Master und auf einem Einzelserver, auf einem Slave die Antwort des Masters. Eine nicht leere ID fragt nach diesem Slave.

Ein Slave ohne Verbindung antwortet sofort mit `false`. Um auf Änderungen am Vertrauen zu reagieren, nutze [`getTrustChangedSignal()`](events.md#trust-changes). Wie Admins das Vertrauen verwalten, steht unter [Master- und Slave-Server](../../admin/multi-server.md#trusted-slaves).

## Geldformatierung { #money-formatting }

`MoneyFormat` formatiert Geld genauso wie die Platzhalter von BankSystem, damit deine Mod Geld im selben Stil zeigt. Alle Methoden sind statisch und threadsicher.

| Methode | Rückgabewert |
|---|---|
| `formatMoney(long raw)` | Mit dem Geldformat des Servers (Standard `$%s`): `123456` → `"$1'234.56"` |
| `formatMoney(long raw, String pattern)` | Mit deinem eigenen Muster; `%s` ist die Zahl. Ohne `%s` nur die Zahl. |
| `formatMoneyRaw(long raw)` | Nur die Zahl: `123456` → `"1234.56"` |
| `getPattern()` | Das aktuelle Muster |

Die Zahl hat immer `'` als Tausendertrennzeichen und zwei Nachkommastellen, abgerundet. Bei einem negativen Betrag steht das Minus innerhalb des Musters: `"$-1'234.56"`. BankSystem setzt das Muster beim Serverstart; auf einem Client, der mit einem entfernten Server verbunden ist, nutzt `formatMoney(long)` den Standard `$%s`. Ruf `setPattern` nicht selbst auf.

```java
long raw = 123456;                                   // 1234.56
String shown = MoneyFormat.formatMoney(raw);         // "$1'234.56"
String euro  = MoneyFormat.formatMoney(raw, "%s €"); // "1'234.56 €"
String plain = MoneyFormat.formatMoneyRaw(raw);      // "1234.56"
```

## Banknotenfluss-Protokoll { #note-flow-log }

`api.getNoteFlowLog()` zeichnet Geld-Items auf, die außerhalb der Bank entstehen oder vernichtet werden, zum Beispiel Geld, das ein Dorfbewohner auszahlt. Die Einträge landen in der eigenen Diagnose-Datenbank dieses Servers, daher funktioniert es auf jedem Server, Slaves eingeschlossen. Es blockiert nie und wirft nie eine Exception; ist die Diagnose-Datenbank aus, tut es nichts.

```java
INoteFlowLog flow = api.getNoteFlowLog();
// call on the server thread
flow.record("mymod:villager_pay", player.getUUID(), moneyItemId, +count, villager, "trade #12");
flow.record("mymod:burn", player.getUUID(), moneyItemId, -count, null); // without a villager
```

| Parameter | Bedeutung |
|---|---|
| `source` | Was passiert ist, mit deiner Mod-ID: `mymod:villager_pay` |
| `player` | Der beteiligte Spieler oder `null` |
| `item` | Die `ItemID` des Geldes |
| `amount` | Vorzeichenbehaftete **Item-Anzahl**: positiv = entstanden, negativ = vernichtet |
| `villager` | Der handelnde Dorfbewohner oder `null`. BankSystem speichert seine UUID, Dimension und Position. |
| `context` | Beliebiger weiterer Text oder `null` |

Diese Quellen schreibt BankSystem selbst: `banksystem:converter_in` und `banksystem:converter_out` (Banknoten in den oder aus dem Konverter), `banksystem:give` (`/give` eines Geld-Items) und `banksystem:creative_create` / `banksystem:creative_destroy` (Banknoten, die aus dem Kreativinventar genommen oder darin gelöscht wurden).

## Verwandte Seiten { #related-pages }

- [Events und Signale](events.md): auf Änderungen an Konten, Netzwerk und Transaktionsbuch reagieren.
- [Transaktionsbuch](transaction-ledger.md): eigene Einträge ins Transaktionsbuch schreiben.
- [API für Unternehmen, Auszahlungen und Dividenden](companies-api.md): Auszahlungen, Dividenden und Aktien-Design.
- [Entwickler](../index.md): welche API für welche Aufgabe.
