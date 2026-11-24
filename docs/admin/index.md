---
title: "Server Admin"
description: "A first-setup checklist for both mods, and where each config and data file lives."
---

# Server Admin

This part is for the people who run a server with BankSystem and StockMarket. The bank works out of the box: every player gets an account, and a few common items can be banked. Markets you create yourself. The checklist below gets a server ready for players.

## First setup

1. **Install** BankSystem, StockMarket and their required mods on the server and every client. See [Installation and updates](install.md).
2. **Make yourself admin** of both mods: `/banksystem op` and `/stockmarket op`. See [Admins and permissions](permissions.md).
3. **Choose the bankable items** with `/banksystem manage`, or turn on **Allow all items**. See [Bankable items](banksystem/bankable-items.md).
4. **Set the starting money and limits** in the BankSystem [Mod Settings](banksystem/settings.md): **Starting balance**, accounts and companies per player.
5. **Set up the markets** with `/stockmarket manage`: which items can be traded, their prices and bots. See [StockMarket for admins](stockmarket/index.md).
6. **Plan your backups**. See [Data files and backups](backups.md).
7. **Optional:** connect more servers ([Master and slave servers](multi-server.md)), show balances in the tab list ([Placeholders](placeholders.md)), or post to Discord ([Discord feed](discord.md)).

## Where the files are

| What | Where |
|---|---|
| BankSystem data and settings | `<world>/data/BankSystem/` |
| StockMarket data and settings | `<world>/data/StockMarket/` |
| Network connection | `config/modutilities/MultiServerConfig.json` |
| Discord webhooks | `config/modutilities/discord/` |
| News events | `config/StockMarket/news/` |

The settings live in the world folder, so each world has its own. [Data files and backups](backups.md) lists every file.

## Find your topic

| I want to | Read |
|---|---|
| See every switch of both mods | [Features you can turn on and off](features.md) |
| Look up a command | [Admin commands](commands.md) |
| Fix a player's balance or freeze an account | [Managing accounts](banksystem/accounts.md) |
| Find out who cheated | [Audit and anti-cheat](audit/index.md) |
| Fix a problem | [Troubleshooting](troubleshooting.md) |

## Related pages

- [BankSystem for admins](banksystem/index.md): the bank admin tools.
- [StockMarket for admins](stockmarket/index.md): markets, plugins and news.
- [How the two mods work together](../together.md): the big picture.
