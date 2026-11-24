---
title: "Data files and backups"
description: "Where both mods keep their data, the backup commands, automatic safety copies and the export package."
---

# Data files and backups

Both mods keep their data inside the world folder, so a normal world backup includes it. The one catch is the databases: a copy taken while the server writes to them can be broken. This page shows how to copy them safely.

## Where the data is

**BankSystem**, in `<world>/data/BankSystem/`:

| File or folder | Holds |
|---|---|
| `Bank_data/`, `Companies/`, `ItemIDs.nbt`, `Meta_data.nbt`, `BankAccountBindings.nbt` | Accounts, balances, companies, the item list and the currency bindings. Saved every few seconds. |
| `settings.json` | The [Mod Settings](banksystem/settings.md). |
| `Database/banksystem.db` | The transaction ledger and the balance history (SQLite). |
| `Database/banksystem_diagnostics.db` | Banknote flow and, on slaves, every transfer to and from the master. Only read by the [Audit Tool](audit/audit-tool.md). |
| `dividend_history.db` | The dividend history of all companies. |
| `audit/` | The [audit log and digests](audit/reports.md). |
| `share_symbols/` | The [share symbols](banksystem/companies.md#share-symbols). |

**StockMarket**, in `<world>/data/StockMarket/`:

| File or folder | Holds |
|---|---|
| `MarketManager/`, `PluginManager/` | Markets, their settings and the plugin data. |
| `News/` | News history, the event registry and the pictures. |
| `settings.json` | The StockMarket Mod Settings. |
| `villager_trades.nbt` | Villager trading data. |
| `Database/stockdata.db` | Price candles, order and trade history (SQLite). |
| `Database/stockmarket_diagnostics.db` | Trade alerts and the server each order came from. |

**Config files** outside the world: `config/modutilities/MultiServerConfig.json` ([network](multi-server.md)), `config/modutilities/discord/` ([Discord feed](discord.md)) and `config/StockMarket/news/` (news events).

On a network, the master holds almost everything. A slave keeps only its `settings.json`, its diagnostics database, `Meta_data.nbt` and a copy of the share symbols in `share_symbols/`. The `audit/` files are written on the master only.

## Backing up a running server

The `.db` files are written all the time. Use one of these ways to copy them safely. Everything else can be copied as usual.

### A database snapshot

```text
/banksystem backup snapshot <path>
```

writes a consistent copy of `banksystem.db` to the given path, relative to the server folder. The server keeps running normally. This is the easiest way for BankSystem.

### Pausing the writes

For a backup script that copies the whole world (`tar`, `rsync` and similar), pause the database writes first:

| Command | What it does |
|---|---|
| `/banksystem backup pause` | Finishes queued writes, then stops writing to `banksystem.db`. |
| `/stockmarket backup pause` | The same for `stockdata.db`. |
| `/banksystem backup resume`, `/stockmarket backup resume` | Starts writing again. Writes from the pause are done now. |
| `/banksystem backup status`, `/stockmarket backup status` | Shows whether writes are paused. |

Wait for the console line `[BankSystem] db-worker paused for backup` (or `[StockMarket] …`) before you start copying. A pause ends by itself after **120 seconds**, so a forgotten `resume` can't stop the data for good. Copy within that time.

The commands need operator level 2 and only work on the master. They work from the console, so a script can send them through RCON. Trading and banking go on during the pause.

!!! tip "Copy the -wal file too"
    Next to each `.db` file there may be a `-wal` and a `-shm` file. During a pause and after a clean stop, the `.db` file alone is complete. After a crash, keep the `-wal` file with the `.db`: it holds the latest changes.

The diagnostics databases are not paused. Copy them while the server is stopped, or use the export package below.

## The export package

```text
/banksystem backup export [name]
```

collects the data of both mods into one package: a folder `<world>/audit_exports/<date>-<time>[-name]/` and a zip with the same content. The databases are copied safely while the server runs. A `manifest.json` lists every file with its checksum and the server's versions.

Use it for the [Audit Tool](audit/audit-tool.md) or when you report a problem. It works on every server, also on slaves. Player data and region files are not included. Old packages are never deleted automatically.

## Automatic safety copies

The mods make copies on their own before risky changes:

- **Before an update** changes the data format: a zip of the old data in `<world>/data/BankSystem_backups/` or `<world>/data/StockMarket_backups/`. See [Installation and updates](install.md#updating).
- **Before removing items of missing mods** with the one-shot setting: a backup of the BankSystem data. See [Troubleshooting](troubleshooting.md).
- **A damaged diagnostics database** is renamed to `.corrupt-<time>` and replaced by a new one.
- **A BankSystem data file that can't be read** (`Meta_data.nbt`, `settings.json`, `ItemIDs.nbt`, `Bank_data/`, `BankAccountBindings.nbt` or `Companies/`) is renamed to `<name>.corrupt-<time>`, and BankSystem starts with a fresh, empty one. Stop the server and restore that file from a backup.

## Restoring

1. Stop the server.
2. Replace the world folder, or only `data/BankSystem/` and `data/StockMarket/`, with the backup.
3. On a network, restore the master and the slaves from the same point in time.
4. Start the server.

## Related pages

- [Audit Tool](audit/audit-tool.md): reads the export package.
- [Installation and updates](install.md): back up before every update.
- [Master and slave servers](multi-server.md): what each server stores.
