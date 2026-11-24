---
title: "Datendateien und Backups"
description: "Wo beide Mods ihre Daten ablegen, die Backup-Befehle, automatische Sicherheitskopien und das Exportpaket."
---

# Datendateien und Backups { #data-files-and-backups }

Beide Mods legen ihre Daten im Weltordner ab, also sind sie in einem normalen Welt-Backup enthalten. Der einzige Haken sind die Datenbanken: Eine Kopie, die entsteht, während der Server in sie schreibt, kann beschädigt sein. Diese Seite zeigt, wie du sie sicher kopierst.

## Wo die Daten liegen { #where-the-data-is }

**BankSystem**, in `<world>/data/BankSystem/`:

| Datei oder Ordner | Enthält |
|---|---|
| `Bank_data/`, `Companies/`, `ItemIDs.nbt`, `Meta_data.nbt`, `BankAccountBindings.nbt` | Konten, Kontostände, Unternehmen, die Item-Liste und die Währungsbindungen. Wird alle paar Sekunden gespeichert. |
| `settings.json` | Die [Mod-Einstellungen](banksystem/settings.md). |
| `Database/banksystem.db` | Das Transaktionsbuch und der Verlauf der Kontostände (SQLite). |
| `Database/banksystem_diagnostics.db` | Der Fluss der Banknoten und, auf Slaves, jede Übertragung zum und vom Master. Wird nur vom [Audit Tool](audit/audit-tool.md) gelesen. |
| `dividend_history.db` | Der Dividendenverlauf aller Unternehmen. |
| `audit/` | Das [Audit-Log und die Berichte](audit/reports.md). |
| `share_symbols/` | Die [Aktiensymbole](banksystem/companies.md#share-symbols). |

**StockMarket**, in `<world>/data/StockMarket/`:

| Datei oder Ordner | Enthält |
|---|---|
| `MarketManager/`, `PluginManager/` | Märkte, ihre Einstellungen und die Plugin-Daten. |
| `News/` | Verlauf der News, das Ereignisregister und die Bilder. |
| `settings.json` | Die Mod-Einstellungen von StockMarket. |
| `villager_trades.nbt` | Daten des Dorfbewohner-Handels. |
| `Database/stockdata.db` | Preiskerzen, Verlauf der Orders und des Handels (SQLite). |
| `Database/stockmarket_diagnostics.db` | Handelsalarme und der Server, von dem jede Order kam. |

**Konfigurationsdateien** außerhalb der Welt: `config/modutilities/MultiServerConfig.json` ([Netzwerk](multi-server.md)), `config/modutilities/discord/` ([Discord-Feed](discord.md)) und `config/StockMarket/news/` (News-Ereignisse).

In einem Netzwerk hält der Master fast alles. Ein Slave behält nur seine `settings.json`, seine Diagnose-Datenbank, `Meta_data.nbt` und eine Kopie der Aktiensymbole in `share_symbols/`. Die Dateien in `audit/` werden nur auf dem Master geschrieben.

## Einen laufenden Server sichern { #backing-up-a-running-server }

In die `.db`-Dateien wird ständig geschrieben. Verwende einen dieser Wege, um sie sicher zu kopieren. Alles andere kannst du wie gewohnt kopieren.

### Ein Datenbank-Snapshot { #a-database-snapshot }

```text
/banksystem backup snapshot <path>
```

schreibt eine konsistente Kopie von `banksystem.db` an den angegebenen Pfad, relativ zum Serverordner. Der Server läuft normal weiter. Das ist der einfachste Weg für BankSystem.

### Die Schreibzugriffe pausieren { #pausing-the-writes }

Für ein Backup-Skript, das die ganze Welt kopiert (`tar`, `rsync` und ähnliche), pausierst du zuerst die Schreibzugriffe auf die Datenbank:

| Befehl | Was er tut |
|---|---|
| `/banksystem backup pause` | Schließt die anstehenden Schreibzugriffe ab und schreibt dann nicht mehr in `banksystem.db`. |
| `/stockmarket backup pause` | Dasselbe für `stockdata.db`. |
| `/banksystem backup resume`, `/stockmarket backup resume` | Schreibt wieder. Die Schreibzugriffe aus der Pause werden jetzt erledigt. |
| `/banksystem backup status`, `/stockmarket backup status` | Zeigt, ob die Schreibzugriffe pausiert sind. |

Warte auf die Konsolenzeile `[BankSystem] db-worker paused for backup` (bzw. `[StockMarket] …`), bevor du mit dem Kopieren beginnst. Eine Pause endet nach **120 Sekunden** von selbst, damit ein vergessenes `resume` die Daten nicht dauerhaft anhalten kann. Kopiere innerhalb dieser Zeit.

Die Befehle brauchen Operator-Level 2 und funktionieren nur auf dem Master. Sie funktionieren in der Konsole, also kann ein Skript sie über RCON senden. Handel und Bankgeschäfte laufen während der Pause weiter.

!!! tip "Kopiere auch die -wal-Datei"
    Neben jeder `.db`-Datei kann es eine `-wal`- und eine `-shm`-Datei geben. Während einer Pause und nach einem sauberen Stopp ist die `.db`-Datei allein vollständig. Nach einem Absturz behältst du die `-wal`-Datei zusammen mit der `.db`: Sie enthält die neuesten Änderungen.

Die Diagnose-Datenbanken werden nicht pausiert. Kopiere sie, während der Server gestoppt ist, oder verwende das Exportpaket unten.

## Das Exportpaket { #the-export-package }

```text
/banksystem backup export [name]
```

sammelt die Daten beider Mods in einem Paket: einem Ordner `<world>/audit_exports/<date>-<time>[-name]/` und einem Zip mit demselben Inhalt. Die Datenbanken werden sicher kopiert, während der Server läuft. Eine `manifest.json` listet jede Datei mit ihrer Prüfsumme und die Versionen des Servers auf.

Verwende es für das [Audit Tool](audit/audit-tool.md) oder wenn du ein Problem meldest. Es funktioniert auf jedem Server, auch auf Slaves. Spielerdaten und Regionsdateien sind nicht enthalten. Alte Pakete werden nie automatisch gelöscht.

## Automatische Sicherheitskopien { #automatic-safety-copies }

Die Mods legen vor riskanten Änderungen von selbst Kopien an:

- **Bevor ein Update** das Datenformat ändert: ein Zip der alten Daten in `<world>/data/BankSystem_backups/` oder `<world>/data/StockMarket_backups/`. Siehe [Installation und Updates](install.md#updating).
- **Bevor Items fehlender Mods entfernt werden**, mit der einmaligen Einstellung: ein Backup der Daten von BankSystem. Siehe [Fehlerbehebung](troubleshooting.md).
- **Eine beschädigte Diagnose-Datenbank** wird in `.corrupt-<time>` umbenannt und durch eine neue ersetzt.
- **Eine Datendatei von BankSystem, die sich nicht lesen lässt** (`Meta_data.nbt`, `settings.json`, `ItemIDs.nbt`, `Bank_data/`, `BankAccountBindings.nbt` oder `Companies/`), wird in `<name>.corrupt-<time>` umbenannt, und BankSystem startet mit einer frischen, leeren Datei. Stoppe den Server und stelle diese Datei aus einem Backup wieder her.

## Wiederherstellen { #restoring }

1. Stoppe den Server.
2. Ersetze den Weltordner, oder nur `data/BankSystem/` und `data/StockMarket/`, durch das Backup.
3. In einem Netzwerk stellst du den Master und die Slaves vom selben Zeitpunkt wieder her.
4. Starte den Server.

## Verwandte Seiten { #related-pages }

- [Audit Tool](audit/audit-tool.md): liest das Exportpaket.
- [Installation und Updates](install.md): sichere vor jedem Update.
- [Master- und Slave-Server](multi-server.md): was jeder Server speichert.
