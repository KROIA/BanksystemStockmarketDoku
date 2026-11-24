---
title: "StockMarket for admins"
description: "The StockMarket admin tools at a glance and the recommended setup order."
---

# StockMarket for admins

Most StockMarket admin work happens in one screen: `/stockmarket manage`. From there you create markets, edit presets, open the Mod Settings and tune the plugins. You need the StockMarket admin flag for it. Give it with `/stockmarket op <player>`, see [Admins and permissions](../permissions.md).

## Setting up a new server

A new world has no markets. This order gets you to a working stock market quickly:

1. **Make yourself admin** with `/stockmarket op`.
2. **Choose the kind of market**: with bot orders, so players can always trade, or players only. See [Choosing a market setup](setup-use-cases.md). If unsure, keep the default with bots.
3. **Check the presets.** They hold the starting price and settings of each item. See [Market presets](presets.md).
4. **Create the markets** on the **Create Markets** tab. See [Creating and managing markets](markets.md#creating-markets).
5. **Look through the Mod Settings**, for example the candle length and how fast player trades fade from the price. See [Mod Settings](mod-settings.md).
6. **Optional:** set [trading hours](trading-hours.md), turn [villager trading](villager-trading.md) on or off, and adjust the [news](news/index.md).

The price plugins work with their defaults. Tune them later, once you see how your players trade.

## What you can do

| I want to | Read |
|---|---|
| Decide between bot markets and players-only markets | [Choosing a market setup](setup-use-cases.md) |
| Create, change, pause or remove a market | [Creating and managing markets](markets.md) |
| Change the starting price of items for new markets | [Market presets](presets.md) |
| Change server-wide settings | [Mod Settings](mod-settings.md) |
| Open and close markets at set times | [Trading hours](trading-hours.md) |
| Make villagers trade at market prices | [Villager trading](villager-trading.md) |
| Change how prices move by themselves | [Plugins](plugins/index.md) |
| Write or change news events | [News system](news/index.md) |
| Run StockMarket on several servers | [Master and slave servers](../multi-server.md) |
| Back up the market data | [Data files and backups](../backups.md) |

## Good to know

- **The admin flag is not operator status.** An operator still needs `/stockmarket op` to open the management screen. A server with LuckPerms can tie the flag to a permission node instead.
- **Use maintenance mode while you change things.** A paused market can't be traded, so nobody profits from a price jump while you tune it. See [Maintenance mode](markets.md#maintenance-mode).
- **On a network, the master decides.** Markets, presets, plugins and news live on the master server.

## Related pages

- [Server Admin overview](../index.md): setup, integrations and both mods.
- [Admin commands](../commands.md): every admin command of both mods.
- [Features you can turn on and off](../features.md): every switch in one place.
