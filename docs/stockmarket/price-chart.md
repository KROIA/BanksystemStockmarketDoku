---
title: Price chart and order book
description: Reading the candlestick chart and the order book next to it, moving around the chart, and why a price moves.
---

# Price chart and order book

The left half of the trading screen shows the price history of the market as a candlestick chart. Along its right edge you see the order book: how many items wait to be bought or sold at each price. This page explains how to read both and why the price moves.

<figure markdown="span">
  ![The price chart with candles, the order book along its right edge and two of your order markers](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: stockmarket/price-chart.png</figcaption>
</figure>

## Candles

Each candle covers one time span. It shows four prices:

- **Open**: the price at the start of the time span.
- **Close**: the price at the end.
- **High** and **Low**: the highest and lowest price in between. The thin line (the wick) reaches from the low to the high.

A **green** candle closed higher than it opened: the price went up. A **red** candle closed lower: the price went down.

<figure markdown="span">
  ![One candle with its open, close, high and low price marked](../assets/images/stockmarket/candle.svg){ width="600" }
</figure>

The small bars under the candles show how many items were traded in each time span. They have the colour of their candle.

The label on the right edge of the chart marks the current price. The current price is always the price of the last trade.

### Timeframes

The buttons on the chart set how long one candle is: **1m**, **5m**, **15m**, **1h**, **4h** or **1d**. Short timeframes show the last minutes in detail. Long ones show the trend over days.

Some servers measure candles in in-game time instead. The buttons are then **1h**, **4h**, **1D** and **1W**, counted in in-game hours, and the time axis shows the in-game day.

## Moving around the chart

| To | Do this |
|---|---|
| Move the view | Drag the chart with the left mouse button. |
| Zoom in or out | Scroll the mouse wheel over the chart. It zooms around the mouse pointer. |
| Zoom only along the time axis | Hold ++shift++ and scroll. |
| Zoom only along the price axis | Hold ++ctrl++ and scroll. |
| Fit the price axis to the visible candles | Press ++space++. |
| Jump to the newest candle | Press ++ctrl+space++. |

When you move back in time, the chart loads older candles as you go.

## The order book

The bars along the right edge of the chart show the order book: the [limit orders](trading.md#limit-order-trade-at-your-price) that wait to be filled. Each bar sits at a price. The longer the bar, the more items wait at that price.

- **Green bars** below the current price are buy orders: someone wants to buy at that price.
- **Red bars** above the current price are sell orders: someone wants to sell at that price.

The order book tells you what a [market order](trading.md#market-order-trade-now) will cost. A buy market order fills against the red bars, starting at the lowest one. If the red bars near the price are short, a big buy goes through several of them and pays more and more. The same goes for a sell against the green bars.

## Your orders on the chart

Each of your open limit orders shows as a horizontal line at its price.

- **Drag the handle** on the line to move the order to a new price. A buy order only moves up if you have enough money for the higher price.
- **Click the X** on the line to cancel the order. The reserved money or items go back to your account.

Your orders also appear on the **Pending Orders** tab of the trading panel.

## Why a price moves

The price only changes when a trade happens. Each trade sets the price to the price it filled at. So:

- **A buy market order** fills against the cheapest sell orders. When it uses up all items at one price, the next trade happens at a higher price, and the price goes up.
- **A sell market order** does the same downwards, against the highest buy orders.
- **A limit order** that reaches across the current price trades right away, like a market order, up to its own price. The rest waits in the order book.

A limit order that only waits doesn't move the price. It changes the order book, which decides how far the next market order moves the price.

Players are not the only ones who trade. On most servers, market plugins add orders of their own, so prices move even when nobody is online. [Market news](newspaper.md) can push a price up or down for a while.

!!! tip "Big orders on quiet markets"
    If the order book next to the price is thin, a big market order can move the price a lot, and you pay more than the price you saw. Split big trades, or use a limit order.

## Related pages

- [Trading basics](trading.md): placing market and limit orders.
- [Market news](newspaper.md): news that moves prices.
- [Glossary](../glossary.md): spread, liquidity, sweep and other market words.
