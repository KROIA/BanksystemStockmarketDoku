---
title: "Events und Signale"
description: "Jedes Event, das eine abhängige Mod abonnieren kann, mit den Regeln für Threads."
---

# Events und Signale { #events-and-signals }

BankSystem sagt anderen Mods Bescheid, wenn sich etwas ändert: Nutzer und Konten, Items, die Netzwerkverbindung, das Vertrauen in Slaves, Auszahlungen, das Einfrieren von Konten, Einträge im Transaktionsbuch und Verdachtsmarkierungen. Abonniere die Events, statt regelmäßig nachzufragen.

```java
IBankSystemEvents events = BankSystemMod.getAPI().getEvents();
```

`getEvents()` gibt für die ganze Spielsitzung dasselbe Objekt zurück, über Welten hinweg. BankSystem leert seine Listener nie: Ein Listener, den du hinzufügst, bleibt registriert, wenn ein Spieler eine Einzelspielerwelt verlässt und eine andere öffnet. Füge deine Listener einmal hinzu, wenn deine Mod startet, nicht jedes Mal, wenn eine Welt geladen wird.

## Zwei Arten von Events { #two-kinds-of-events }

BankSystem nutzt zwei Typen aus ModUtilities (`net.kroia.modutilities.event`):

| Typ | Nutzdaten | Abonnieren mit |
|---|---|---|
| `Signal` | keine | `addListener(Runnable)` |
| `DataEvent<T>` | ein Wert vom Typ `T` | `addListener(Consumer<T>)` |

Beide nehmen auch `addListener(listener, maxCalls)`: Der Listener entfernt sich nach `maxCalls` Aufrufen selbst (`-1` = keine Grenze). `removeListener(listener)` entfernt ihn früher und gibt `true` zurück, wenn er registriert war.

```java
// Signal: no payload
events.getBanksystemSetupCompleteSignal().addListener(() -> loadMyData());

// DataEvent: one value
events.getTrustChangedSignal().addListener(info -> onTrust(info.slaveID(), info.trusted()));

// Only the next call, then the listener removes itself
events.getBanksystemSetupCompleteSignal().addListener(this::onReady, 1);
```

Ein Listener darf während seiner Ausführung Listener hinzufügen oder entfernen. Die Änderung gilt ab dem nächsten Aufruf.

Um einen Listener zu entfernen, behalte genau die Instanz, die du hinzugefügt hast, zum Beispiel in einem Feld. Ein neues Lambda mit demselben Rumpf ist eine andere Instanz. `events.removeListeners()` entfernt alle Listener aller Events, auch die anderer Mods; ruf es also nicht auf.

## Threads { #threads }

Jedes Event wird auf einer Seite (Master, Slave oder beide) und auf einem Thread ausgelöst:

- **Server-Thread.** Die meisten Events. Du darfst den Spielzustand direkt anfassen.
- **Netzwerk-Thread.** Die vier Verbindungs-Events werden auf einem Netzwerk-Thread ausgelöst. Blockiere im Listener nicht und fasse dort keinen Spielzustand an: Gib die Arbeit zuerst an den Server-Thread weiter, zum Beispiel mit `server.execute(() -> …)`.
- **Thread des Schreibers.** Einträge im Transaktionsbuch und Verdachtsmarkierungen werden auf dem Thread ausgelöst, der den Eintrag geschrieben hat: dem Server-Thread, einem Thread, der Anfragen bearbeitet (von einem Slave weitergeleitete Aufrufe), oder dem Datenbank-Thread (regelmäßige Prüfungen). Halte diese Listener schnell und threadsicher, und gib Arbeit am Spielzustand an den Server-Thread weiter.
- **Thread des Aufrufers.** `getAccountFreezeChangedEvent()` wird auf dem Thread ausgelöst, der das Konto eingefroren oder aufgetaut hat. Gib Arbeit am Spielzustand an den Server-Thread weiter.

Im Zweifel gib die Arbeit an den Server-Thread weiter.

## Alle Events { #all-events }

| Getter | Typ | Seite | Thread | Wird ausgelöst, wenn |
|---|---|---|---|---|
| `getUserAddedEvent()` | `DataEvent<User>` | Master | Server | Ein Nutzer zum Bank-Manager hinzugefügt wird. |
| `getUserRemovedEvent()` | `DataEvent<User>` | Master | Server | Ein Nutzer entfernt wird. |
| `getBankAccountCreatedEvent()` | `DataEvent<ISyncServerBankAccount>` | Master | Server | Ein Bankkonto angelegt wird. |
| `getBankAccountDeletedEvent()` | `DataEvent<ISyncServerBankAccount>` | Master | Server | Ein Bankkonto gelöscht wird. |
| `getItemIDsMergedEvent()` | `DataEvent<Map<ItemID, ItemID>>` | Master | Server | Item-IDs zusammengeführt wurden. Siehe [Zusammengeführte und entfernte Items](#merged-and-removed-items). |
| `getItemIDsRemovedEvent()` | `DataEvent<Set<ItemID>>` | Master | Server | Ein Admin die Items fehlender Mods entfernt hat. |
| `getBankDataSavedToFileSignal()` | `Signal` | Master | Server | Die Bankdaten gespeichert wurden. |
| `getBankDataLoadedFromFileSignal()` | `Signal` | beide | Server | Die Bankdaten geladen wurden. |
| `getSettingsSavedToFileSignal()` | `Signal` | beide | Server | Die Einstellungen gespeichert wurden. |
| `getSettingsLoadedFromFileSignal()` | `Signal` | beide | Server | Die Einstellungen geladen wurden. |
| `getBanksystemSetupCompleteSignal()` | `Signal` | beide | Server | BankSystem die Welt fertig eingerichtet hat. |
| `getMasterServerSlaveConnected()` | `Signal` | Master | Netzwerk | Ein Slave die Verbindung fertig aufgebaut hat. |
| `getMasterServerSlaveDisconnected()` | `DataEvent<String>` | Master | Netzwerk | Ein Slave die Verbindung getrennt hat; die Nutzdaten sind seine Slave-ID. |
| `getSlaveConnectionAcceptedSignal()` | `Signal` | Slave | Netzwerk | Dieser Slave sich mit seinem Master verbunden hat. |
| `getSlaveConnectionLostSignal()` | `Signal` | Slave | Netzwerk | Dieser Slave seinen Master verloren hat. |
| `getTrustChangedSignal()` | `DataEvent<TrustChangeInfo>` | Master | Server | Einem Slave vertraut oder das Vertrauen entzogen wurde. |
| `getPayoutExecutedEvent()` | `DataEvent<PayoutExecutedInfo>` | Master | Server | Ein Auszahlungsplan gelaufen ist, gezahlt hat oder fehlgeschlagen ist. |
| `getDividendPaidEvent()` | `DataEvent<DividendPaidEvent>` | Master | Server | `payDividend` eine Dividende gezahlt hat. |
| `getAccountFreezeChangedEvent()` | `DataEvent<AccountFreezeChangedEvent>` | Master | Aufrufer | Ein Konto eingefroren oder aufgetaut wurde. |
| `getTransactionLoggedEvent()` | `DataEvent<TransactionLoggedEvent>` | Master | Schreiber | Ein Eintrag ins Transaktionsbuch geschrieben wurde. |
| `getSuspicionFlaggedEvent()` | `DataEvent<SuspicionFlaggedEvent>` | Master | Schreiber | Eine Verdachtsmarkierung gesetzt wurde. |

## Wann du abonnierst { #when-to-subscribe }

1. Abonniere, wenn deine Mod startet.
2. Lade alles, was die Weltdaten von BankSystem braucht, in `getBanksystemSetupCompleteSignal()`.
3. Warte auf einem Slave auf `getSlaveConnectionAcceptedSignal()`, bevor du den Master etwas fragst. Bis dahin antworten asynchrone Aufrufe sofort mit ihrem Ersatzwert (siehe [BankSystem-API](api.md#when-an-async-call-fails)).

## Verbindungen zwischen Master und Slave { #master-and-slave-connections }

Zwei Events werden auf dem Master ausgelöst und beschreiben Slaves; zwei werden auf einem Slave ausgelöst und beschreiben seine eigene Verbindung zum Master. Wähle sie danach aus, wo dein Code läuft.

```text
        master                               slave
  getMasterServerSlaveConnected     <-->   getSlaveConnectionAcceptedSignal
  getMasterServerSlaveDisconnected  <-->   getSlaveConnectionLostSignal
          (payload: slave id)
```

- **`getSlaveConnectionAcceptedSignal()`** wird auf dem Slave ausgelöst, sobald die Verbindung zum Master für asynchrone Aufrufe bereit ist. Nach jedem erneuten Verbinden wird es wieder ausgelöst. Nutze es, um Caches aufzubauen, deren Daten vom Master kommen.
- **`getSlaveConnectionLostSignal()`** wird auf dem Slave einmal ausgelöst, wenn eine funktionierende Verbindung abbricht, auch beim sauberen Herunterfahren. Es wird nicht bei jedem fehlgeschlagenen Verbindungsversuch erneut ausgelöst, sondern erst wieder nach der nächsten erfolgreichen Verbindung. Nutze es, um diese Caches zu verwerfen.
- **`getMasterServerSlaveConnected()`** wird auf dem Master ausgelöst, nachdem ein Slave die Verbindung fertig aufgebaut hat. Es hat keine Nutzdaten.
- **`getMasterServerSlaveDisconnected()`** wird auf dem Master ausgelöst, wenn ein Slave die Verbindung trennt. Die Nutzdaten sind die Slave-ID, damit du verwerfen kannst, was du für diesen Slave aufbewahrt hast.

Alle vier werden auf einem Netzwerk-Thread ausgelöst. Siehe [Threads](#threads).

## Änderungen am Vertrauen { #trust-changes }

`getTrustChangedSignal()` wird auf dem Master ausgelöst, wenn ein Admin einem Slave vertraut oder ihm das Vertrauen entzieht. Die Nutzdaten `TrustChangeInfo(String slaveID, boolean trusted)` enthalten den neuen Zustand, du kannst ihn also weitergeben, ohne erneut zu fragen.

```java
events.getTrustChangedSignal().addListener(info -> {
    // info.slaveID(): the slave; info.trusted(): true if it is trusted now
    sendTrustStateToSlave(info.slaveID(), info.trusted());
});
```

Auf einem Slave wird es nie ausgelöst. Ein Slave erfährt nicht, welchen anderen Slaves der Master vertraut. Braucht deine Mod den Vertrauensstatus auf einem Slave, schick ihn selbst vom Master, oder frag mit [`isSlaveServerTrustedAsync`](api.md#is-this-slave-trusted) nach.

## Zusammengeführte und entfernte Items { #merged-and-removed-items }

**`getItemIDsMergedEvent()`** wird auf dem Master ausgelöst, nachdem BankSystem Item-IDs zusammengeführt hat, die sich als dasselbe Item herausgestellt haben, und seine eigenen Daten (Kontostände, reservierte Kontostände, erlaubte Items, Kontosymbole) auf die verbleibende ID verschoben hat. Die Nutzdaten ordnen jeder alten ID die ID zu, in die sie zusammengeführt wurde. Verschiebe deine eigenen Daten, die an Item-IDs hängen (Märkte, Orders, Preisverlauf), genauso.

**`getItemIDsRemovedEvent()`** wird auf dem Master ausgelöst, nachdem ein Admin zugestimmt hat, die Items von Mods zu entfernen, die nicht mehr installiert sind. BankSystem hat ihre Kontostände bereits entfernt. Das Event wird einmal pro Serverstart ausgelöst, direkt nach `getBanksystemSetupCompleteSignal()`, und gar nicht, wenn nichts entfernt wurde. Die Nutzdaten sind die Menge der entfernten IDs. Lösche deine eigenen Daten, die an diesen IDs hängen:

```java
events.getItemIDsRemovedEvent().addListener(removed -> {
    for (ItemID id : removed) myMarkets.remove(id);
});
```

Die Nutzdaten beider Events lassen sich nicht ändern.

## Auszahlungen und Dividenden { #payouts-and-dividends }

Beide werden nur auf dem Master ausgelöst, auf dem Server-Thread.

**`getPayoutExecutedEvent()`** wird bei jeder Ausführung eines Auszahlungsplans ausgelöst, Dividendenpläne eingeschlossen, **auch wenn sie fehlschlägt**. Ein pausierter Plan läuft nicht und löst nichts aus. Nutze es für Abzeichen, Statistiken oder Warnungen an die Verwalter des Unternehmens.

| Feld von `PayoutExecutedInfo` | Bedeutung |
|---|---|
| `companyId` | Das Unternehmen |
| `scheduleId` | Der Plan |
| `sourceAccount` | Das Bankkonto des Unternehmens |
| `targetUuid` | Der Zielspieler; kann bei einem Dividendenplan `null` sein |
| `amount` | Rohbetrag in der Währung des Plans (100 = 1.00) |
| `status` | Das Ergebnis, siehe unten |
| `time` | Zeit in Epoch-Millisekunden |

| `status` | Bedeutung |
|---|---|
| `OK` | Gezahlt. |
| `INSUFFICIENT_FUNDS` | Ein Plan in Geld: Der freie Kontostand des Unternehmenskontos konnte den Betrag nicht decken. |
| `TARGET_MISSING` | Der Zielspieler oder das Zielkonto existiert nicht mehr. Bei einem Dividendenplan: Niemand hält Aktien. |
| `TARGET_NO_DEPOSIT_RIGHT` | Der Zielspieler hat auf dem gewählten Zielkonto kein Recht zum Einzahlen. |
| `CURRENCY_ITEM_MISSING` | Ein Plan in einem Item: Das Unternehmenskonto hat keine Bank für das Item oder nicht genug davon, oder für den Plan ist kein Item gesetzt. |
| `PAUSED` | Ein Dividendenplan wurde zurückgehalten: Die Aktienprüfung des Unternehmens hat mehr Aktien in Bankkonten gefunden, als geprägt wurden, und noch kein Admin hat das bestätigt. |
| `ACCOUNT_FROZEN` | Das Unternehmenskonto ist eingefroren. |
| `UNKNOWN` | Jeder andere Fehlschlag. |

`status` ist ein `PayoutHistoryRecord.Status` aus `net.kroia.banksystem.data.table.record`, also außerhalb des API-Packages. Vergleiche über den Namen; es können neue Werte hinzukommen.

**`getDividendPaidEvent()`** wird jedes Mal einmal ausgelöst, wenn [`payDividend`](companies-api.md#paying-a-dividend) eine Dividende gezahlt hat: aufgerufen von einer Mod oder über **Dividende auszahlen** im Unternehmensfenster. Eine abgelehnte Dividende löst es nicht aus. `totalPaid` und `holderCount` sagen, was wirklich gezahlt wurde: Nur ganze Aktien zählen, und in seltenen Fällen schlägt nach der Deckungsprüfung eine einzelne Überweisung fehl, sodass dieser Aktionär übersprungen wird. Dividendenpläne melden sich stattdessen über `getPayoutExecutedEvent()`.

| Feld von `DividendPaidEvent` | Bedeutung |
|---|---|
| `companyId` | Das Unternehmen |
| `perShareAmount` | Rohbetrag pro Aktie |
| `totalPaid` | Gezahlte Rohsumme |
| `holderCount` | Anzahl der bezahlten Konten |
| `time` | Zeit in Epoch-Millisekunden |

## Eingefrorene Konten { #account-freezes }

`getAccountFreezeChangedEvent()` wird auf dem Master einmal pro echter Änderung ausgelöst, auf dem Thread, der das Konto eingefroren oder aufgetaut hat. Denselben Zustand erneut zu setzen löst es nicht aus.

| Feld von `AccountFreezeChangedEvent` | Bedeutung |
|---|---|
| `accountNumber` | Das Konto |
| `frozen` | `true` = jetzt eingefroren |
| `actor` | Der `LedgerActor`, der es geändert hat |

Wie das Einfrieren funktioniert, steht unter [BankSystem-API](api.md#frozen-accounts).

## Einträge im Transaktionsbuch { #ledger-rows }

`getTransactionLoggedEvent()` wird auf dem Master einmal pro Eintrag im [Transaktionsbuch](transaction-ledger.md) ausgelöst, direkt nachdem der Eintrag zum Speichern eingereiht wurde und bevor die Audit- und Verdachtsprüfungen darauf laufen. Auch Einträge, die andere Mods schreiben, lösen es aus. Es wird auf dem Thread des Schreibers ausgelöst. Wirft dein Listener eine Exception, schreibt BankSystem eine Warnung ins Log, und der Eintrag wird trotzdem geschrieben.

Einträge werden nur geschrieben, während BankSystem auf dem Master läuft, vom Serverstart bis zum Serverstopp. Eine Änderung außerhalb dieser Zeit schreibt keinen Eintrag, dieses Event wird also nicht ausgelöst. Verdachtsmarkierungen entstehen aus diesen Einträgen, daher entstehen dann auch keine.

| Feld von `TransactionLoggedEvent` | Bedeutung |
|---|---|
| `accountNumber` | Das Konto, zu dem der Eintrag gehört |
| `type` | Der `LedgerType` |
| `itemId` | Short-ID des Items; `0` bei Einträgen ohne Item (Einfrieren, Kontobearbeitung) |
| `amount` | Rohbetrag; `0`, wenn es keinen gibt. Bei manchen Typen mit Vorzeichen, zum Beispiel bei Überweisungen: `-x` beim Sender, `+x` beim Empfänger. Siehe [Typ-Codes](transaction-ledger.md#type-codes). |
| `actor` | Der `LedgerActor`, der ihn verursacht hat |
| `otherAccount` | Das andere Konto einer Überweisung oder Auszahlung oder `null` |
| `companyId` | Das Unternehmen eines Auszahlungs-, Dividenden- oder Aktieneintrags oder `null` |
| `timeMs` | Zeit in Epoch-Millisekunden |
| `note` | Freier Text oder `null` |

```java
events.getTransactionLoggedEvent().addListener(row -> {
    if (row.type() == LedgerType.TRANSFER && row.amount() > 0)
        server.execute(() -> notifyReceiver(row.accountNumber(), row.amount())); // to the server thread
});
```

## Verdachtsmarkierungen { #suspicion-flags }

`getSuspicionFlaggedEvent()` wird auf dem Master einmal pro Markierung ausgelöst, nachdem die Markierung gespeichert und die Admins alarmiert wurden. Es wird auf dem Thread ausgelöst, der die Markierung gesetzt hat.

| Feld von `SuspicionFlaggedEvent` | Bedeutung |
|---|---|
| `accountNumber` | Das markierte Konto; `0` bei Markierungen, die den ganzen Server betreffen |
| `flagType` | Der Code der Markierung, siehe [Transaktionsbuch](transaction-ledger.md#suspicion-flags) |
| `flagName` | Der Name des Codes, zum Beispiel `WEALTH_JUMP`, oder `FLAG_<code>` bei einem unbekannten Code |
| `severity` | Höher ist schlimmer |
| `amount` | Rohbetrag, der die Markierung ausgelöst hat; `0`, wenn es keinen gibt |
| `ref` | Eine Referenz wie eine Transfer-ID oder `null` |
| `details` | Der Grund als Text oder `null` |
| `timeMs` | Zeit in Epoch-Millisekunden |

## Verwandte Seiten { #related-pages }

- [BankSystem-API](api.md): Konten, Banken und die asynchronen Aufrufe.
- [Transaktionsbuch](transaction-ledger.md): die Einträge hinter `getTransactionLoggedEvent()`.
- [API für Unternehmen, Auszahlungen und Dividenden](companies-api.md): Pläne und Dividenden.
- [Master- und Slave-Server](../../admin/multi-server.md): wie das Netzwerk aufgebaut ist.
