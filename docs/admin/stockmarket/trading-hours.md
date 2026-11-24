---
title: "Trading hours"
description: "Setting opening hours per market, the clock source, and closed versus maintenance."
---

# Trading hours

Each market can have daily trading hours, like a real stock exchange. Outside them the market is **closed**: nobody can place orders, and the price stands still until it opens again. By default every market is open around the clock.

## Setting the hours

1. Run `/stockmarket manage`, select a market and click **Market Settings**.
2. Enter the open and close time in the **Trading hours** row, as `HH:MM`.
3. Click **Apply**, or **Apply to all** to give every market the same hours.

The rules for the times:

- `08:00`–`18:00` is open from 08:00 until 17:59.
- An open time later than the close time runs over midnight: `22:00`–`06:00` is open at night.
- `00:00`–`24:00` means always open. Any other pair of equal times is invalid.
- An invalid time turns the field red and shows *Invalid time (HH:MM, 00:00-24:00)*.

**Apply to all** asks first, then copies only the hours to every market and reports how many it changed.

Below the row, the screen shows the server's real time, its in-game time and which one the markets follow. Check it when the server is in another time zone than you.

## Which clock

All markets follow one clock, set in the [Mod Settings](mod-settings.md) with **Trading hours: use real time**:

| Setting | Clock |
|---|---|
| Off (default) | The in-game time of the master's overworld. Tick 0 is 06:00. `/time set` moves the clock. With the daylight cycle frozen, the clock stands still and so do the markets. |
| On | The real time of the computer the master runs on, in its time zone. |

The change takes effect at once. Price candles have their own clock setting, see [In-game candles](mod-settings.md#in-game-candles).

## What "closed" means

- **No new orders** from players, bots or plugins. Players see *Market is closed - outside trading hours*.
- **Waiting orders stay.** Players can still cancel them. They can fill again after the market opens.
- **Item-for-item orders wait** until both markets are open.
- **The price is frozen.** The chart shows flat candles.
- **News still counts.** A news event can change the market's base price while it is closed, so the price can jump when it opens.

Players see a **Market Closed** banner on the trading screen and the trading hours next to the clock. See [Trading](../../stockmarket/trading.md) for the player's view.

## Opening and closing by command

| Command | What it does |
|---|---|
| `/stockmarket open "<market>"` | Opens the market now. |
| `/stockmarket close "<market>"` | Closes the market now. |

`<market>` is the item id in quotes, for example `"minecraft:diamond"`, or the market's number. If several markets share an item id, such as different enchanted books, use the number: tab completion shows it with the full item name.

The command holds until the market's hours would open or close it next. Example: with hours 08:00–18:00, `open` at 20:00 keeps the market open until 08:00. On an always-open market, `close` holds until you run `open`. The override survives a restart.

The commands need the StockMarket admin flag. From the console they need operator level 2.

## Closed or maintenance?

Both stop player trading. Use the trading hours for a schedule, and [maintenance mode](markets.md#maintenance-mode) when you change a market or something goes wrong.

| | Closed | Maintenance |
|---|---|---|
| Waiting player orders | Kept | Cancelled and refunded |
| Bots and plugins | Pause | Keep trading |
| Price | Frozen | Keeps moving |
| Banner | **Market Closed** | **Under Maintenance** |

The open/close commands don't end maintenance.

## On a network

The master decides, using its own clock. Players on slaves see the master's state and clock. You can change the hours and use the commands on a slave too; they are passed to the master.

## Related pages

- [Creating and managing markets](markets.md): the Market Settings and maintenance mode.
- [Mod Settings](mod-settings.md): the clock setting.
- [Admin commands](../commands.md): all commands.
