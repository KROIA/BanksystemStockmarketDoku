---
title: "Features you can turn on and off"
description: "Every on/off switch of both mods in one list, with its default and where to change it."
---

# Features you can turn on and off

This page lists every feature you can switch on or off, with its default. Most switches are in the **Mod Settings** screen of each mod, which only shows on the master server:

- BankSystem: `/banksystem manage` → **Mod Settings**, see [BankSystem Mod Settings](banksystem/settings.md).
- StockMarket: `/stockmarket manage` → **Mod Settings**, see [StockMarket Mod Settings](stockmarket/mod-settings.md).

Switches marked "restart" only take effect after a server restart.

## Both mods

| Feature | BankSystem setting | StockMarket setting | Default |
|---|---|---|---|
| [Placeholders](placeholders.md) for TAB and Placeholder API | **Placeholders enabled** (restart) | **Placeholders (TAB / Placeholder API)** (restart) | on |
| [Discord feed](discord.md) | **Discord feed** | **Discord feed (trades and alerts)** | off |
| [LuckPerms sync](permissions.md#syncing-the-admin-flag-with-luckperms) of the admin flag | **Sync admin flag with LuckPerms** | **Sync admin flag with LuckPerms** (restart) | off |
| Alerts in chat for admins who never chose | **Admin alerts on by default** | **Alert chat on by default** | on |
| Debug messages in the log | **Enable debug logging** | **Log debug messages** | off |

## BankSystem

| Feature | Setting | Default |
|---|---|---|
| Bank every item except a blacklist | **Allow all items** | off |
| [Numismatics](../banksystem/currency-bindings.md) bindings | **Numismatics integration** | on |
| [Lightman's Currency](../banksystem/currency-bindings.md) bindings | **Lightman's Currency integration** | on |
| Balance history | **Balance snapshot interval (minutes)**, `0` = off | on (every minute) |
| Thinning out old history | **History retention sweep (minutes)**, `0` = off | on |
| [Suspicion flags](audit/alerts.md#banksystem-flags) 1 to 5 | One **Flag …** switch each | on |
| [Daily digest](audit/reports.md#the-daily-digest) | **Daily audit digest** | on |

A currency mod that you switch off behaves as if it weren't installed: money bound to it stays there, frozen, until you switch it back on.

## StockMarket

| Feature | Setting | Default |
|---|---|---|
| [Villager trading](stockmarket/villager-trading.md) at market prices | **Villager trading enabled** | on |
| Villager trades of items without a market use money too, priced from the emerald market | **Replace emeralds for unlisted items** | off |
| Those trades use the preset's default price instead | **Use preset prices for villagers** | off |
| [Profit alert](audit/alerts.md#stockmarket-alerts) | **Profit alert threshold**, `0` = off | on |
| [Pump-and-dump detection](audit/alerts.md#stockmarket-alerts) | **Pump-and-dump detection** | on |
| [Web interface](web-interface.md), read only | **Web interface (read-only)** | off |
| Candles follow the in-game clock instead of real time | **Candles: use in-game time** (restart) | off |
| Trading hours follow real time instead of the in-game clock | **Trading hours: use real time** | off |

### Per market

These switches are in the market's settings in the management screen (`/stockmarket manage`), see [Markets](stockmarket/markets.md).

| Feature | Setting | Default |
|---|---|---|
| Players can't place orders; their open orders are cancelled and refunded | **Maintenance mode** | off |
| Bots add liquidity and steer the price | **Enable Virtual Orderbook** | on |
| [Trading hours](stockmarket/trading-hours.md) | **Trading hours** | |
| [Price plugins](stockmarket/plugins/index.md) and [news events](stockmarket/news/index.md) | Each plugin's own screen | |

## Related pages

- [BankSystem Mod Settings](banksystem/settings.md): every BankSystem setting.
- [StockMarket Mod Settings](stockmarket/mod-settings.md): every StockMarket setting.
- [Admins and permissions](permissions.md): who can change the settings.
