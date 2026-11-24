---
title: "Villager trading"
description: "The villager trade data file and the Villager Trading settings."
---

# Villager trading

StockMarket changes villager trades from emeralds to money and prices them from the markets. This page covers the settings. What players see is on the player page [Villager trading](../../stockmarket/villager-trading.md).

## How the prices are made

- A trade changes to money when its item has a market. Wandering traders work the same way.
- **A villager buys** at the market price times **Villager buy margin** (default 0.8).
- **A villager sells** at the market price times **Villager sell margin** (default 1.2).
- Prices are updated every **Price refresh interval (minutes)**, default 20 real minutes, about one Minecraft day.
- Villager trades never place orders. They don't change any market price.
- Discounts (reputation, Hero of the Village, cured zombies) still apply to money trades, up to 20%.
- Trades with an extra item, such as an enchanted book (book plus emeralds), keep the item. Only the emeralds become money.

When you create a market, the matching villager trades change to money at the next refresh. When you delete it, they go back to emeralds.

## Items without a market

By default, trades of items without a market keep their emeralds. Two settings change that:

| Setting | Effect |
|---|---|
| **Replace emeralds for unlisted items** | These trades are paid in money too: the number of emeralds times the emerald market price, without margin. Needs an emerald market. The emerald price is rounded to two digits, such as 12.00, so prices don't change with every small move. |
| **Use preset prices for villagers** | Only with the setting above. These trades use the item's [preset](presets.md) price instead, even if it has no market. Items without a preset price fall back to the emerald price. |

Both take effect the next time a player opens a villager's trades.

## Turning it off

Turn off **Villager trading enabled** in the [Mod Settings](mod-settings.md#villager-trading). Each villager gets its original emerald trades back the next time a player opens its trades. Trades that were partly used up stay that way.

## The data file

The original emerald trades are saved in `<world>/data/StockMarket/villager_trades.nbt`. They are needed to restore the trades. Every server has its own file, also slaves. It is saved at every autosave when it changed.

## On a network

The master's settings count for all servers. The master sends its price table to every slave, so turning the feature on at the master turns it on everywhere. Changes in the **Villager Trading** group reach the slaves at once.

## Related pages

- [Mod Settings](mod-settings.md#villager-trading): every villager setting with its range.
- [Market presets](presets.md): the prices for items without a market.
- [Villager trading](../../stockmarket/villager-trading.md): the player's view.
