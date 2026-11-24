---
title: "Entwickler"
description: "Welche API für welche Aufgabe, ein erster Aufruf für jede Mod und die Regeln für Threads."
---

# Entwickler { #developers }

Diese Seiten sind für Mod-Autoren, die BankSystem oder StockMarket aus ihrer eigenen Mod heraus nutzen wollen: Kontostände lesen, Spieler bezahlen, Märkte öffnen oder ein Plugin schreiben, das Preise bewegt. Beide Mods sind Architectury-Mods für Fabric und NeoForge, und ihre APIs liegen im Common-Modul.

Beginne mit [Dein Projekt einrichten](setup.md), um die Mods zu deinem Gradle-Build hinzuzufügen.

## Welche API für welche Aufgabe { #which-api-for-which-job }

| Du willst | Nutze | Seite |
|---|---|---|
| Kontostände lesen oder ändern, Konten erstellen, Geld überweisen | `BankSystemMod.getAPI()` → `getServerBankManager()` | [BankSystem-API](banksystem/api.md) |
| Auf neue Konten, protokollierte Transaktionen, Auszahlungen oder Slave-Verbindungen reagieren | `BankSystemMod.getAPI().getEvents()` | [Events und Signale](banksystem/events.md) |
| Eigene Zeilen in den Transaktionsverlauf schreiben | `BankSystemMod.getAPI().getLedger()` | [Transaktionsbuch](banksystem/transaction-ledger.md) |
| Deine Währungs-Mod unter **Währungs-Verknüpfungen** erscheinen lassen | `ExternalCurrencyProvider` | [Währungsintegration](banksystem/currency-integration.md) |
| Items einen Preis für die Rangliste des Gesamtvermögens geben | `ItemPriceProvider` | [Item-Preisanbieter](banksystem/item-price-provider.md) |
| Auszahlungen von Unternehmen planen oder Dividenden zahlen | `getPayoutManager()`, `getDividendPayer()` | [API für Unternehmen, Auszahlungen und Dividenden](banksystem/companies-api.md) |
| Einen Markt erstellen, schließen oder pausieren | `StockMarketMod.getAPI().getIntegration()` | [Marktintegrations-API](stockmarket/market-creation-api.md) |
| Das Handelsfenster öffnen oder ein Preischart in deinem eigenen Fenster zeigen | `StockMarketClientIntegration` | [Marktintegrations-API](stockmarket/market-creation-api.md) |
| Märkte, Preise und Orders auf dem Client lesen | Die Client-Manager von StockMarket | [Marktzugriffs-API](stockmarket/market-access-api.md) |
| Preise bewegen, Bot-Orders platzieren oder das Orderbuch formen | Ein StockMarket-Plugin | [Überblick über das Plugin-System](stockmarket/plugins/index.md) |

## Ein erster Aufruf für jede Mod { #a-first-call-to-each-mod }

**BankSystem:** Lies den Geld-Kontostand eines Spielers. Das funktioniert auf jedem Server, auch auf einem Slave:

```java
BankSystemAPI api = BankSystemMod.getAPI();
IAsyncBankManager bank = api.getServerBankManager().getAsync();

bank.getPersonalBankAccountAsync(player.getUUID())
    .thenCompose(account -> account == null ? CompletableFuture.completedFuture(null)
                                            : account.getBankAsync(MoneyItem.getItemID()))
    .thenCompose(moneyBank -> moneyBank == null ? CompletableFuture.completedFuture(null)
                                                : moneyBank.getRealBalanceAsync())
    .thenAccept(balance -> {
        // on a slave this runs on another thread: go back to the server thread first
        server.execute(() -> player.sendSystemMessage(Component.literal("Balance: " + balance)));
    });
```

**StockMarket:** Prüfe, ob der Diamant-Markt offen ist. Auf dem Server-Thread:

```java
IStockMarketIntegration markets = StockMarketMod.getAPI().getIntegration();
if (markets != null) {   // null on a client without a running server
    ItemID diamond = ItemID.of(new ItemStack(Items.DIAMOND));
    boolean open = markets.marketExistsFor(diamond) && markets.isMarketOpen(diamond);
}
```

`ItemID` ist der Item-Schlüssel von BankSystem (`net.kroia.banksystem.util.ItemID`). StockMarket verwendet ihn ebenfalls.

## Die Regeln, die überall gelten { #the-rules-that-apply-everywhere }

- **Master und Slave.** In einem Netzwerk gehören alle Bank- und Marktdaten einem Server (dem Master). Die anderen (Slaves) leiten Anfragen an ihn weiter. Siehe [Master- und Slave-Server](../admin/multi-server.md).
- **Sync oder async.** Jeder Manager hat eine Sync-Seite und eine Async-Seite. Sync-Aufrufe geben Werte sofort zurück, gibt es aber nur auf dem Master; `getSync()` gibt auf einem Slave `null` zurück. Async-Aufrufe geben eine `CompletableFuture` zurück und funktionieren auf jedem Server. Nutze async, außer dein Code läuft immer nur auf dem Master.
- **Threads.** Ruf die APIs vom Server-Thread aus auf. Auf dem Master werden Async-Aufrufe sofort abgeschlossen. Auf einem Slave kommt die Antwort auf einem anderen Thread an: Wechsle zurück auf den Server-Thread (`server.execute(...)`), bevor du die Welt oder Spieler anfasst.
- **Fehler.** Auf einem Slave kann ein Async-Aufruf fehlschlagen, zum Beispiel wenn die Verbindung zum Master abbricht. Behandle den Fall, dass die Future mit einer Exception endet. Eine Anfrage ohne Antwort kann trotzdem ausgeführt worden sein, also erstatte oder wiederhole nie blind. Die Seite [BankSystem-API](banksystem/api.md) erklärt, welcher Fehler was bedeutet.
- **Rohe und reale Beträge.** Geld wird als ganze Zahlen gespeichert (roh) und Spielern mit zwei Nachkommastellen angezeigt (real). Methoden mit `...Real...` im Namen nehmen oder liefern den angezeigten Wert, zum Beispiel `12.50`.

## Verwandte Seiten { #related-pages }

- [Dein Projekt einrichten](setup.md): Gradle und die Abhängigkeit zu den Mods.
- [BankSystem-API](banksystem/api.md): die Bank im Detail.
- [Überblick über das Plugin-System](stockmarket/plugins/index.md): ein StockMarket-Plugin schreiben.
