---
title: "Placeholders"
description: "Showing prices, balances and rankings in TAB or Placeholder API, for both mods."
---

# Placeholders

Both mods offer placeholders: short codes that other mods replace with live values. Put them into a tab list, a scoreboard or a chat format to show a player's balance, the richest players or the price of diamonds.

## What you need

Install one of these mods on the server, see [Installation and updates](install.md#optional-mods):

| Mod | Loaders | How a placeholder looks |
|---|---|---|
| TAB | Fabric, NeoForge | `%banksystem_balance%`, `%stockmarket_price_diamond%` |
| Placeholder API | Fabric | `%banksystem:balance%`, `%stockmarket:price_diamond%` |

That's all. Both mods register their placeholders by themselves. Players don't need TAB or Placeholder API. In singleplayer, put the mod into the game's own `mods` folder.

!!! note "TAB 5.5.0 in singleplayer"
    With TAB 5.5.0, opening a second singleplayer world in the same game session disconnects you with *An objective with the name TAB-PlayerList already exists*. This is a TAB problem. Restart the game between worlds. Servers are not affected.

The tables below use the TAB form. For Placeholder API, write `:` instead of the first `_`.

## Formatted and raw values

Every placeholder with a number has a `_raw` variant:

- `%banksystem_balance%` shows `$1'234.56`: thousands separator, two decimals, currency symbol.
- `%banksystem_balance_raw%` shows `1234.56`: a plain number for conditions and calculations in other mods.

The money format is BankSystem's **Money format** setting (default `$%s`). StockMarket prices use it too, so all money looks the same.

## BankSystem placeholders

**Per player**, for the player who sees the text:

| Placeholder | Example | Shows |
|---|---|---|
| `%banksystem_balance%` | `$1'234.56` | Available money in the personal account. |
| `%banksystem_locked%` | `$100.00` | Money locked in open orders. |
| `%banksystem_total%` | `$1'334.56` | Available plus locked. |
| `%banksystem_account_number%` | `12` | The personal account's number. |
| `%banksystem_rank%` | `3` | Place in the richest-players list. |

**For the whole server:**

| Placeholder | Example | Shows |
|---|---|---|
| `%banksystem_circulation%` | `$1'250'000.00` | All available money in all accounts. |
| `%banksystem_circulation_locked%` | `$20'000.00` | All locked money. |
| `%banksystem_account_count%` | `57` | Number of bank accounts. |
| `%banksystem_player_count%` | `42` | Number of players with a personal account. |
| `%banksystem_average_balance%` | `$29'761.90` | Average money per personal account. |
| `%banksystem_top_1_name%` | `Steve` | Name of the richest player. |
| `%banksystem_top_1_balance%` | `$250'000.00` | Their money. |

The richest-players list ranks personal accounts by available plus locked money. Replace `1` with any place up to **Richest players list size** (default 10). Empty places show no name and a zero balance.

## StockMarket placeholders

**Per market.** Replace `diamond` with the market's name, see below.

| Placeholder | Example | Shows |
|---|---|---|
| `%stockmarket_price_diamond%` | `$1'234.56` | Current price. |
| `%stockmarket_change_diamond%` | `+3.21%` | Price change in the last 24 hours. `0` without price history. |
| `%stockmarket_volume_diamond%` | `12'500.00` | Items traded in the last 24 hours. |

**Per player:**

| Placeholder | Example | Shows |
|---|---|---|
| `%stockmarket_open_orders%` | `3` | Open orders on all markets. |
| `%stockmarket_portfolio%` | `$8'420.00` | Market value of the items in the personal account. Money doesn't count; items without a market count as zero. |

### Market names

The name comes from the item id:

| Item | Name |
|---|---|
| `minecraft:diamond` | `diamond` |
| `create:brass_ingot` | `create_brass_ingot` |
| An enchanted book | `enchanted_book_` plus a 6-character code, for example `enchanted_book_3fa91c` |

The `minecraft:` part is dropped; other mod names stay in front. Everything except letters, digits and `_` becomes `_`. Items with extra data, such as enchanted books and potions, get a code for that data. That code can change after a Minecraft update, so check those placeholders after updating.

If two items end up with the same name, only one of them gets placeholders. The server log names both.

## How fresh the values are

The values are refreshed in the background, so they can lag a little:

| Values | Refreshed every |
|---|---|
| BankSystem, per player | **Player placeholder refresh (ms)**, default 1 second |
| BankSystem, whole server | **Server placeholder refresh (ms)**, default 30 seconds |
| StockMarket, all | 2 seconds |

The BankSystem settings are in the **Integrations** section of the [Mod Settings](banksystem/settings.md#integrations).

## On a network

The master computes all values. Slaves fetch them, so players see the same numbers everywhere.

- On a slave the master doesn't [trust](multi-server.md#trusted-slaves), all BankSystem placeholders with account data and the StockMarket player placeholders stay empty. Market prices still work.
- While a slave has no connection, it shows the last values it got.
- A slave leaves out markets for items it doesn't have installed.
- Turning placeholders off on the master turns them off on the slaves too.

## Turning placeholders off

Each mod has its own switch, and both need a restart:

- BankSystem: **Placeholders enabled** in the [Mod Settings](banksystem/settings.md#integrations).
- StockMarket: **Placeholders (TAB / Placeholder API)** in the [StockMarket Mod Settings](stockmarket/mod-settings.md).

## Related pages

- [Discord feed](discord.md): post events to Discord.
- [Installation and updates](install.md): install TAB or Placeholder API.
- [Master and slave servers](multi-server.md): trusting a slave.
