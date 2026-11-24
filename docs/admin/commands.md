---
title: "Admin commands"
description: "Every admin command of both mods in one table, with the permission each one needs."
---

# Admin commands

This page lists every admin command of both mods. Player commands are on the [BankSystem](../banksystem/commands.md) player page.

**Needs** says what a player must have:

- **Flag**: the mod's admin flag (`/banksystem op` or `/stockmarket op`). Every player sees these commands.
- **Op 2** or **Op 3**: operator level 2 or 3, or the permission node in brackets.

See [Admins and permissions](permissions.md) for the flags and the nodes. Commands marked "master" only work on the master server of a [network](multi-server.md).

## BankSystem

### Admins and servers

| Command | Needs | What it does |
|---|---|---|
| `/banksystem op [player]` | Op 2 (`banksystem.admin.command.op`) | Gives the BankSystem admin flag. Master. |
| `/banksystem deop [player]` | Op 2 (`banksystem.admin.command.op`) | Takes the flag away. Master. |
| `/banksystem trust <slave id>` | Op 2 (`banksystem.admin.command.trust`) | Trusts a slave server. Master. See [Master and slave servers](multi-server.md#trusted-slaves). |
| `/banksystem untrust <slave id>` | Op 2 (`banksystem.admin.command.trust`) | Takes the trust away. Master. |
| `/banksystem serverInfo` | Everyone | Shows the role of this server and, on a slave, whether it is trusted. |
| `/banksystem serverNetworkInfo` | Flag | Lists all connected servers and their trust. |

`op`, `deop`, `trust` and `untrust` must be typed by a player in game. They don't work from the server console.

### Items and accounts

| Command | Needs | What it does |
|---|---|---|
| `/banksystem manage` | Flag | Opens the Bank Settings screen. |
| `/banksystem allowItem <item id>` | Flag | Allows an item in the bank. |
| `/banksystem allowItemInHand` | Flag | Allows the item in your hand. |
| `/banksystem disallowItem <item id>` | Flag | Removes an item from the bank and from every account. |
| `/banksystem disallowItemInHand` | Flag | The same for the item in your hand. |
| `/bank <player> manage` | Flag | Opens a player's account. |
| `/bank <player> show` | Flag | Shows a player's balances in chat. |
| `/money add [player] <amount>` | Flag | Adds money. |
| `/money remove [player] <amount>` | Flag | Removes money. |
| `/money set [player] <amount>` | Flag | Sets the money balance. |
| `/banksystem freeze <account> [on\|off]` | Flag | Freezes or unfreezes an account. From the console: master. |
| `/company manage "<name>"` | Flag | Opens any company's management screen. |
| `/company shares acknowledge "<name>"` | Flag | Accepts a share excess and resumes the dividends. |
| `/banksystem symbols list\|add\|remove\|reload` | Flag | Manages the share symbols. Master. See [Companies and shares](banksystem/companies.md#share-symbols). |
| `/banksystem restorebinding <account> [item]` | Flag | Restores a suspended currency binding. Master. |

### Audit

| Command | Needs | What it does |
|---|---|---|
| `/banksystem audit <player or account>` | Flag | Opens the Audit screen. |
| `/banksystem history <player or account>` | Flag | Opens the balance history with flag markers. |
| `/banksystem alerts on\|off` | Flag | Turns the chat alerts on or off for you. |
| `/banksystem auditreport <hours>` | Flag | Writes a report of the last 1 to 720 hours. |

### Backups and Discord

| Command | Needs | What it does |
|---|---|---|
| `/banksystem backup snapshot <path>` | Op 2 (`banksystem.admin.command.backup`) | Writes a safe copy of the database. Master. |
| `/banksystem backup pause\|resume\|status` | Op 2 (`banksystem.admin.command.backup`) | Pauses database writes for a file backup. Master. |
| `/banksystem backup export [name]` | Op 2 (`banksystem.admin.command.backup`) | Writes the export package. Every server. |
| `/banksystem discord status\|reload` | Op 3 (`modutilities.command.discord`) | Shows or reloads the Discord feed setup. |

See [Data files and backups](backups.md) and [Discord feed](discord.md).

## StockMarket

| Command | Needs | What it does |
|---|---|---|
| `/stockmarket op [player]` | Op 2 (`stockmarket.admin.command.op`) | Gives the StockMarket admin flag. Master. |
| `/stockmarket deop [player]` | Op 2 (`stockmarket.admin.command.op`) | Takes the flag away. Master. |
| `/stockmarket manage` | Flag | Opens the market management. See [Markets](stockmarket/markets.md). |
| `/stockmarket preset add <category> [name]` | Flag | Saves the item in your hand as a market preset. See [Presets](stockmarket/presets.md). |
| `/stockmarket open "<market>"` | Flag | Opens a market until its next scheduled change. See [Trading hours](stockmarket/trading-hours.md). |
| `/stockmarket close "<market>"` | Flag | Closes a market until its next scheduled change. |
| `/stockmarket "<market>" remove` | Flag | Removes a market, also one whose item no longer exists. |
| `/stockmarket news …` | Flag | Controls the news events. See [News commands](stockmarket/news/commands.md). |
| `/stockmarket alerts on\|off` | `stockmarket.admin.notify` | Turns the trading alerts in chat on or off for you. Master. |
| `/stockmarket backup pause\|resume\|status` | Op 2 (`stockmarket.admin.command.backup`) | Pauses database writes for a file backup. Master. |
| `/stockmarket discord status\|reload` | Op 3 (`modutilities.command.discord`) | Shows or reloads the Discord feed setup. |

A market is named by its item id in quotes, for example `"minecraft:iron_ingot"`, or by its number.

## Related pages

- [Admins and permissions](permissions.md): the flags and the nodes.
- [Player commands](../banksystem/commands.md): what players can type.
- [News commands](stockmarket/news/commands.md): all `/stockmarket news` subcommands.
