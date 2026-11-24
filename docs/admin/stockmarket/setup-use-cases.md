---
title: "Choosing a market setup"
description: "Bot-driven market with a virtual order book versus a purely player-driven market, with trade-offs."
---

# Choosing a market setup

A market can get its orders from bots and players, or from players only. You choose per market, so both kinds can run side by side: for example, bots for common items and a players-only market for rare ones.

## Bots and players (the default)

Every new market starts with the **virtual order book**: bot orders around the current price, kept up by the [price plugins](plugins/index.md). Players can always buy and sell at once, and the price moves with player trades plus a little natural movement.

Nothing to set up: create the markets and you're done. Markets from the default presets start with the virtual order book and get the default plugins.

**Good for:** public survival servers, small player numbers, and servers where players expect a trade to go through at once.

**Keep in mind:** prices are partly made by the bots. They follow what players do, but not only that.

## Players only

The market has no bot orders. Every trade is between two players, and the price only moves when they trade. This is the closest to a real exchange.

**For new markets**, set it in the preset:

1. Run `/stockmarket manage` and open the **Presets** tab.
2. For the item, turn off **Virtual Orderbook** and turn on **No Plugin Autosubscribe**.
3. Click **Save Changes**. Markets you create from it now start without bots.

You can also turn off **Orderbook Enabled** on the **Create Markets** tab for a single market.

**For an existing market:**

1. Select the market on the **Overview** tab and click **Market Settings**.
2. Turn off **Enable Virtual Orderbook** and click **Apply**.
3. If you like, remove the market from its plugins in **Manage Plugins**. The price plugins skip it anyway.

**Good for:** roleplay and economy servers, faction servers where scarcity matters, and small trading groups.

**Keep in mind:**

- The order book is empty until a player places a limit order.
- A new market has no real price until players trade on both sides.
- Buyers and sellers can be far apart, so market orders can fill at bad prices or only in part. The rest is cancelled and refunded.
- Without trades, the price doesn't move at all.
- Players used to bot markets may be confused. Tell them which markets are players-only.

## Our advice

Start with bots and players everywhere. Once you have an active player base, switch some valuable items to players only, where real prices matter more than quick trades.

## Related pages

- [Creating and managing markets](markets.md): the Market Settings.
- [Market presets](presets.md): settings for new markets.
- [Price plugins](plugins/index.md): what the bots do.
