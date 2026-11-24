---
title: "Transaktionsbuch"
description: "Typ-Codes und Spalten des Transaktionsbuchs und wie deine Mod eigene Einträge schreibt."
---

# Transaktionsbuch { #transaction-ledger }

BankSystem schreibt für jede Änderung eines Kontostands einen Eintrag ins Transaktionsbuch, in die Tabelle `TransactionLog` von `Database/banksystem.db` auf dem Master (siehe [Datendateien und Backups](../../admin/backups.md#where-the-data-is)). Admins lesen es im [Audit-Fenster](../../admin/audit/investigating.md) und im [Audit Tool](../../admin/audit/audit-tool.md).

Diese Seite zeigt, wie deine Mod eigene Einträge schreibt, was die Typ-Codes und Spalten bedeuten und wie deine Mod ihre Dateien zum Exportpaket für das Audit hinzufügt.

## Wie Einträge geschrieben werden { #how-rows-are-written }

- **Nur der Master schreibt Einträge.** Jede Änderung eines Kontostands läuft auf dem Master, auch wenn ein Slave sie angefragt hat. Der Eintrag nennt den Slave dann in `origin_server`.
- **Das Schreiben blockiert den Bank-Aufruf nie und lässt ihn nie fehlschlagen.** Einträge werden in eine Warteschlange gestellt und von einem Datenbank-Thread gespeichert. Lässt sich ein Eintrag nicht speichern, schreibt BankSystem eine Warnung ins Log, und der Bank-Aufruf gilt trotzdem.
- **Nichts fehlt.** Jede Änderung am Gesamtbetrag einer Bank (frei + reserviert) schreibt dort, wo sie passiert, einen Eintrag. Deckt kein typisierter Eintrag sie ab, schreibt BankSystem einen `RAW_CHANGE`-Eintrag. Für jedes Konto und Item ist der Gesamtbetrag am Ende minus dem Gesamtbetrag am Anfang also die Summe der vorzeichenbehafteten Einträge dazwischen.

Jeder Eintrag löst auf dem Master [`getTransactionLoggedEvent()`](events.md#ledger-rows) aus. Abonniere es, wenn du nur auf Einträge reagieren willst.

## Einträge aus deiner Mod schreiben { #writing-rows-from-your-mod }

```java
ITransactionLedger ledger = BankSystemMod.getAPI().getLedger();

// A row with your own type and actor
ledger.log(accountNumber, LedgerType.ADMIN_ADD, MoneyItem.getItemID(), rawAmount,
        LedgerActor.console(), /* ref */ null, /* note */ "event reward");
```

| Parameter von `log` | Bedeutung |
|---|---|
| `accountNumber` | Das Konto, zu dem der Eintrag gehört |
| `type` | Ein `LedgerType`, siehe [Typ-Codes](#type-codes) |
| `item` | Das Item der Bank, die sich geändert hat |
| `amount` | Rohbetrag (100 = 1.00); ohne Vorzeichen, außer bei den Typen, die unter der Tabelle stehen |
| `actor` | Wer die Änderung verursacht hat, siehe unten |
| `ref` | Optionaler Text, der zusammengehörige Einträge gruppiert, zum Beispiel deine Order-ID |
| `note` | Optionaler freier Text |

Jeder Aufruf ist threadsicher und kehrt sofort zurück. Auf einem Slave und bevor der Server gestartet ist oder nachdem er gestoppt wurde, tun `log` und `logTrade` nichts. Ruf sie auf dem Master auf, wo sich der Wert bewegt.

Deine Einträge werden wie die von BankSystem behandelt: Sie lösen das Event für das Transaktionsbuch aus und durchlaufen die Audit- und Verdachtsprüfungen für Admins. Ein `ADMIN_*`-Eintrag landet im [Audit-Log](../../admin/audit/reports.md#the-audit-log), und eine große eingehende Überweisung auf ein neues Konto kann eine Markierung auslösen.

### Akteure { #actors }

`LedgerActor(UUID uuid, String name, Source source)` sagt, wer eine Änderung verursacht hat. Nutze die Factory-Methoden:

| Factory-Methode | `source_kind` |
|---|---|
| `LedgerActor.player(uuid, name)` | `PLAYER` |
| `LedgerActor.admin(uuid, name)` | `ADMIN` |
| `LedgerActor.console()` | `CONSOLE` |
| `LedgerActor.system()` | `SYSTEM` |
| `LedgerActor.stockmarket()` | `STOCKMARKET` |
| `LedgerActor.unknown()` | `UNKNOWN` |

### Handelseinträge { #trade-rows }

`logTrade(TradeLogEntry)` schreibt einen `TRADE_BUY`- oder `TRADE_SELL`-Eintrag mit der Quelle `STOCKMARKET`. StockMarket nutzt das für ausgeführte Orders.

```java
ledger.logTrade(new TradeLogEntry(accountNumber, playerUuid, TradeSide.BUY,
        itemId, qtyRaw, currencyId, moneyRaw, avgPriceRaw, virtualQtyOrNull,
        orderRef, TradeRowKind.PERIODIC, System.currentTimeMillis(), /* note */ null));
```

Handelseinträge sind **Deltas**: Alle Einträge mit derselben `ref` ergeben zusammen die Summen der Order. `TradeSide.BUY` schreibt `TRADE_BUY`, `SELL` schreibt `TRADE_SELL`. `TradeRowKind` landet in der Spalte `tag`: `PERIODIC` (eine regelmäßige Aktualisierung einer offenen Order), `SHUTDOWN` (beim Stoppen des Servers geschrieben) oder `CLOSE` (die Order wurde vollständig ausgeführt oder abgebrochen).

### Doppelte Einträge vermeiden { #avoiding-double-rows }

Ein roher Bank-Aufruf (`deposit`, `withdraw`, `setBalance`, `withdrawLocked…` und ihre asynchronen und `Real`-Varianten) schreibt seinen eigenen `RAW_CHANGE`-Eintrag. Schreibt deine Mod für dieselbe Bewegung einen typisierten Eintrag, führe die Bank-Aufrufe in `callerLogs` aus, damit die Bewegung nicht doppelt erfasst wird:

```java
ledger.callerLogs(() -> {
    itemBank.deposit(qty);
    return moneyBank.withdrawLockedPrefered(cost);
});
ledger.logTrade(entry);
```

`callerLogs` funktioniert auf dem Master, nur auf dem aktuellen Thread, und lässt sich verschachteln. Es gibt zurück, was der Rumpf zurückgibt. Überweisungen schreiben auch darin ihr `TRANSFER`-Paar.

Was von selbst Einträge schreibt:

- Rohe Bank-Aufrufe, die kein typisierter Eintrag abdeckt: `RAW_CHANGE` mit der vorzeichenbehafteten Änderung, Quelle `UNKNOWN` (oder der Spieler einer Slave-Anfrage) und dem Namen des Aufrufs in der Notiz.
- Das Anlegen einer Bank mit Startguthaben und das Entfernen von Banken, die noch einen Kontostand haben: `RAW_CHANGE`.
- Das Binden einer Bank an eine [Währungs-Mod](currency-integration.md) oder das Lösen der Bindung: `EXTERNAL_BIND` oder `EXTERNAL_UNBIND` mit der Änderung, die es verursacht hat.
- Überweisungen, auch aus dem reservierten Kontostand: ein `TRANSFER`-Paar.
- Reservieren und Freigeben verschieben nur Wert zwischen frei und reserviert und schreiben nichts.

!!! note "Slaves schreiben untypisierte Einträge"
    `log` tut auf einem Slave nichts, und die asynchronen Bank-Aufrufe tragen keinen Typ. Eine Einzahlung oder Abhebung, die deine Mod auf einem Slave macht, erscheint auf dem Master also als `RAW_CHANGE`-Eintrag mit dem Slave in `origin_server`. Brauchst du typisierte Einträge, nimm die Änderung auf dem Master vor.

## Typ-Codes { #type-codes }

Der Code steht in `type_code`. Codes werden nie neu nummeriert oder wiederverwendet; neue Typen bekommen neue Codes. `LedgerType.code()` liefert den Code eines Typs, `LedgerType.fromCode(int)` den Typ zu einem Code (`UNKNOWN_LEGACY` bei einem unbekannten Code, nie `null`).

| Code | Typ | Wann er geschrieben wird |
|---:|---|---|
| 0 | `UNKNOWN_LEGACY` | Ein alter Eintrag, dessen Art sich nicht zuordnen ließ, oder ein unbekannter Code |
| 1 | `DEPOSIT` | Items oder Geld wurden an einem Bank Terminal oder über eine Einzahlungsanfrage eingezahlt |
| 2 | `WITHDRAW` | Items oder Geld wurden abgehoben (Bank Terminal, Banknoten, Abhebungsanfrage) |
| 3 | `TRANSFER` | Eine Überweisung zwischen Konten; zwei Einträge, `-x` beim Sender und `+x` beim Empfänger |
| 4 | `TRADE_BUY` | Ein Kauf in StockMarket (`logTrade`) |
| 5 | `TRADE_SELL` | Ein Verkauf in StockMarket (`logTrade`) |
| 6 | `WITHDRAW_REFUND` | Der Teil einer Banknoten-Abhebung, der nicht ausgegeben werden konnte und zurückgebucht wurde |
| 7 | `ADMIN_SET` | Ein Admin hat einen Kontostand gesetzt; Betrag = die Änderung, Notiz = `old->new` |
| 8 | `ADMIN_ADD` | `/money add` |
| 9 | `ADMIN_REMOVE` | `/money remove` |
| 10 | `ADMIN_UNLOCK` | Ein Admin hat einen reservierten Kontostand freigegeben; Betrag = der freigegebene Betrag |
| 11 | `ADMIN_ACCOUNT_EDIT` | Kontoname, Mitglieder, Rechte oder Symbol wurden geändert; Betrag `0`, die Notiz listet die Änderungen auf |
| 12 | `BANK_CLOSED` | Ein Konto wurde gelöscht, während es noch einen Kontostand hatte; ein Eintrag pro Item, Betrag = der verlorene Kontostand |
| 13 | `CONVERTER_DEPOSIT` | Der Bank-Konverter hat Items in die Bank gelegt |
| 14 | `CONVERTER_WITHDRAW` | Reserviert; wird zurzeit nicht geschrieben |
| 15 | `UPLOAD_DEPOSIT` | Ein Bank Upload Block hat Items eingezahlt; Akteur = Besitzer des Blocks, Notiz = Position |
| 16 | `DOWNLOAD_WITHDRAW` | Ein Bank Download Block hat Items abgehoben; Akteur `SYSTEM`, Notiz = Position |
| 17 | `CRAFT_CONSUME` | Beim Craften wurden Zutaten aus der Bank verbraucht |
| 18 | `CRAFT_OUTPUT` | Ein gecraftetes Ergebnis ging zurück in die Bank |
| 19 | `STARTING_BALANCE` | Das Startguthaben eines neuen persönlichen Kontos |
| 20 | `PAYOUT` | Eine Auszahlung eines Unternehmens; ein Paar wie bei `TRANSFER`, `company_id` gesetzt |
| 21 | `DIVIDEND` | Eine Dividende; ein Paar pro Aktionär, `company_id` gesetzt |
| 22 | `SHARE_STAMP` | Aktien wurden an einer Aktien-Prägestation geprägt |
| 23 | `SHARE_REDEEM` | Aktien wurden an einer Aktien-Prägestation eingelöst |
| 24 | `SHARE_TRADE` | Geprägte Aktien wurden in eine Bank gelegt oder aus ihr genommen |
| 25 | `ACCOUNT_DELETE_PAYOUT` | Der Kontostand eines gelöschten Nutzers wurde ihm als Items ausgehändigt |
| 26 | `ACCOUNT_FREEZE` | Ein Konto wurde eingefroren oder aufgetaut; Betrag `0`, Item `0`, Notiz `frozen` oder `unfrozen` |
| 27 | `ADMIN_DISALLOW_ITEM` | Ein Admin hat ein Item verboten; ein Eintrag pro Besitzer mit dem entfernten Kontostand |
| 28 | `ACCOUNT_DELETE_LOSS` | Der Kontostand eines gelöschten Nutzers, der nicht ausgehändigt werden konnte und vernichtet wurde; die Notiz endet mit `not delivered: <reason>` |
| 29 | `RAW_CHANGE` | Eine Änderung, die kein anderer Eintrag abdeckt (siehe [Doppelte Einträge vermeiden](#avoiding-double-rows)); mit Vorzeichen, die Notiz nennt den Aufruf |
| 30 | `EXTERNAL_BIND` | Eine Bank wurde an ein Konto einer Währungs-Mod gebunden; vorzeichenbehaftete Änderung des Gesamtbetrags, Notiz `bound to <provider>:<account>` |
| 31 | `EXTERNAL_UNBIND` | Die Bindung einer Bank wurde gelöst; vorzeichenbehaftete Änderung, die Notiz sagt, wo das Guthaben geblieben ist |
| 32 | `REFUND_LOST` | Ein Marker ohne Änderung am Kontostand: Für einen Spieler abgehobene Banknoten wurden nicht ausgehändigt, und die Erstattung ließ sich nicht zurückbuchen |

Beträge sind ohne Vorzeichen, außer bei `TRANSFER`, `PAYOUT` und `DIVIDEND` (`-x` beim Zahler, `+x` beim Empfänger), `RAW_CHANGE`, `EXTERNAL_BIND` und `EXTERNAL_UNBIND`. `REFUND_LOST`-Einträge bewegen nichts und zählen nicht zur Summe der Kontostände.

## Spalten { #columns }

| Spalte | Bedeutung |
|---|---|
| `id` | ID des Eintrags, in der Reihenfolge des Einfügens |
| `account_number` | Das Konto, zu dem der Eintrag gehört |
| `actor_uuid`, `actor_name` | Wer die Änderung verursacht hat; die UUID ist bei Konsole und System leer |
| `source_kind` | `PLAYER`, `ADMIN`, `CONSOLE`, `SYSTEM`, `STOCKMARKET` oder `UNKNOWN` |
| `type_code` | Der Typ-Code von oben |
| `kind` | Der Name des Typs, für ältere Leseprogramme |
| `item_id` | Das Item der Bank, die sich geändert hat |
| `amount` | Rohbetrag |
| `other_account` | Das andere Konto einer Überweisung, Auszahlung oder Dividende |
| `company_id` | Das Unternehmen bei Auszahlungs-, Dividenden- und Aktieneinträgen |
| `ts` | Zeit in Epoch-Millisekunden |
| `note` | Freier Text, zum Beispiel `old->new` oder eine Blockposition |
| `ref` | Eine Referenz: eine Order-ID aus StockMarket oder die Transfer-ID eines Slaves |
| `tag` | Handelseinträge: `PERIODIC`, `SHUTDOWN` oder `CLOSE` |
| `money_amount`, `price`, `currency_item` | Handelseinträge: bewegtes Geld, Durchschnittspreis, Währungs-Item |
| `virtual_qty` | Handelseinträge: Menge, die gegen Bot-Orders ausgeführt wurde, ohne anderes Konto |
| `balance_after` | Gesamtbetrag der Bank (frei + reserviert) direkt nach der Änderung; leer bei Handelseinträgen |
| `origin_server` | Der Slave, dessen Anfrage den Eintrag verursacht hat; leer bei Änderungen auf dem Master |
| `dimension`, `x`, `y`, `z` | Der Block, an dem es passiert ist (Bank Terminal, Upload- oder Download-Block, Geldautomat, Aktien-Prägestation); leer, wenn kein Block beteiligt war |

## Verdachtsmarkierungen { #suspicion-flags }

Die eigenen Prüfungen von BankSystem setzen Verdachtsmarkierungen und alarmieren Admins. Was jede Markierung für einen Admin bedeutet, steht unter [Alarme und Verdachtsmarkierungen](../../admin/audit/alerts.md#banksystem-flags). Deine Mod kann mit [`getSuspicionFlaggedEvent()`](events.md#suspicion-flags) auf sie hören, aber keine Markierungen setzen: Dafür gibt es keinen API-Aufruf.

| Code | Name | Wann sie gesetzt wird |
|---:|---|---|
| 1 | `BANKNOTE_LAUNDERING` | Banknoten werden in einem verdächtigen Muster eingezahlt |
| 2 | `LARGE_NOTE_WITHDRAWAL` | Große Banknoten-Abhebungen kurz hintereinander |
| 3 | `WEALTH_JUMP` | Das Gesamtvermögen eines Kontos macht einen Sprung (braucht einen [Item-Preisanbieter](item-price-provider.md)) |
| 4 | `TRANSFER_TO_NEW_ACCOUNT` | Eine große Überweisung, Auszahlung oder Dividende auf ein neues Konto |
| 5 | `MONEY_SUPPLY_GROWTH` | Die Geldmenge des Servers wächst schnell; Konto `0` |
| 6 | `TRANSFER_PARKED` | Eine Überweisung an einen Slave, deren Ergebnis unbekannt blieb; `ref` = die Transfer-ID |
| 7 | `EXTERNAL_BINDING_SUSPENDED` | Eine Währungsbindung wurde beim Start gesperrt; `ref` = `provider:account` |
| 8 | `SHARE_EXCESS` | Ein Unternehmen hat mehr Aktien in Bankkonten, als es geprägt hat; auf dem Unternehmenskonto |
| 9 | `SHARE_CREATED` | Aktien-Items wurden mit `/give` oder über das Kreativinventar erzeugt; auf dem Unternehmenskonto |

Codes werden nie wiederverwendet. Ein unbekannter Code erreicht deinen Listener mit dem Namen `FLAG_<code>`.

## Deine Dateien zum Audit-Export hinzufügen { #adding-your-files-to-the-audit-export }

`/banksystem backup export [name]` schreibt ein Paket für das Audit Tool: einen Ordner `<world>/audit_exports/<yyyyMMdd-HHmmss>[-name]/` und ein Zip mit demselben Inhalt (siehe [Das Exportpaket](../../admin/backups.md#the-export-package)). Deine Mod kann mit `AuditExport` (`net.kroia.banksystem.api.audit`) eigene Dateien hinzufügen:

```java
// once, when your mod starts; on master and slave servers alike
AuditExport.register("mymod", ctx -> {
    Path data = server.getWorldPath(LevelResource.ROOT).resolve("data/MyMod");
    ctx.copyFile(data.resolve("settings.json"), "data/MyMod/settings.json");
    ctx.copyDir(data.resolve("orders"), "data/MyMod/orders");
    ctx.addDatabase("data/MyMod/Database/mymod.db",
            target -> myDb.vacuumInto(target)); // returns a CompletableFuture<Void>
});
```

Registrierst du dieselbe Mod-ID erneut, ersetzt das den früheren Teilnehmer. Bei jedem Export ruft BankSystem jeden Teilnehmer auf dem Server-Thread mit einem `Context` auf. Der Kontext gilt nur während dieses Aufrufs.

| `Context`-Methode | Was sie tut |
|---|---|
| `packageRoot()` | Der Paketordner (absoluter Pfad) |
| `isSlave()` | `true` auf einem Slave |
| `copyFile(Path src, String relPath)` | Kopiert eine Datei sofort, auf dem Server-Thread, damit es nicht mit deinen eigenen Speichervorgängen kollidiert. Eine fehlende Datei wird übersprungen und als `missing` markiert. |
| `copyDir(Path src, String relPath)` | Kopiert einen Ordner mit allem, was darin ist. Ein fehlender Ordner wird übersprungen. |
| `addDatabase(String relPath, Function<Path, CompletableFuture<Void>>)` | BankSystem übergibt die Zieldatei (die Ordner sind schon angelegt). Schreib dort auf deinem eigenen Datenbank-Thread eine konsistente Kopie deiner Datenbank hin, zum Beispiel mit `VACUUM INTO` von SQLite, und schließe das Future ab. |

`relPath` ist relativ zum Paket, mit `/`. Nutze dieselbe Struktur wie im `data/`-Ordner der Welt, zum Beispiel `data/MyMod/...`. Ein Pfad, der aus dem Paket hinausführt, wirft eine `IllegalArgumentException`.

BankSystem wartet auf alle Datenbankkopien, ohne den Server-Thread zu blockieren, höchstens 5 Minuten. Ein fehlgeschlagenes oder verspätetes Future lässt den Export fehlschlagen.

`manifest.json` im Wurzelordner des Pakets listet den Server (`server_uid`, `role` master, slave oder single, Minecraft-Version, Loader, Mods) und pro Mod-ID jede Datei mit Pfad, Methode (`file_copy`, `vacuum_into` oder `missing`), Größe und SHA-256.

## Verwandte Seiten { #related-pages }

- [Events und Signale](events.md): auf Einträge und Markierungen reagieren.
- [BankSystem-API](api.md): die Bank-Aufrufe, die Einträge schreiben.
- [Alarme und Verdachtsmarkierungen](../../admin/audit/alerts.md): was Admins sehen.
- [Audit Tool](../../admin/audit/audit-tool.md): wo das Exportpaket gelesen wird.
