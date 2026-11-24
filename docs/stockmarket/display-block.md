---
title: Stock Market Display
description: Build a wall screen from Stock Market Displays and choose which market or item pair it shows.
---

# Stock Market Display

The **Stock Market Display** shows the live price chart of a market on a wall. Several displays next to each other that show the same market join into one big screen. You can show a normal market, or the exchange rate between two items.

<figure markdown="span">
  ![A 3×2 Stock Market Display with the diamond chart above a Stock Market Block, next to three stacked smaller displays that each show another market](../assets/images/stockmarket/display-in-world.png){ width="600" }
</figure>

## Before you start

- You have one or more **Stock Market Displays**. The recipe is on [Blocks and recipes](blocks-and-recipes.md).
- The market you want to show exists on your server.

## Building a screen

1. Place the displays on a wall, side by side and on top of each other.
2. Make sure they all face the same way. Displays that face the same way, touch each other and show the same market join into one screen. New displays aren't set up yet, so they join each other: place the whole screen first, then set it up.
3. Fill a full rectangle, for example 3 wide and 2 high. The screen covers the largest rectangle that starts at the top-left display.

A new screen shows *Right-click to configure*.

## Choosing what it shows

1. Right-click the screen. The **Configure Display** window opens.
2. Under **I want (item to display):**, pick the market to show.
3. Optional: under **I have / currency (optional):**, pick a second item. The screen then shows the exchange rate between the two items, like the [Item / Item mode](pair-trading.md). **Clear pair** goes back to a normal price chart.
4. Click **Apply**.

<figure markdown="span">
  ![The Configure Display screen of a Stock Market Display with diamond and iron ingot chosen as a pair](../assets/images/stockmarket/display-config.png){ width="600" }
</figure>

## Looking closer

Once the screen shows a chart, right-click it to open the chart full screen. Move and zoom it the same way as in the trading screen, see [Moving around the chart](price-chart.md#moving-around-the-chart). When you close the full-screen chart, the wall screen keeps the view you chose.

## Showing a different market

!!! warning "You have to rebuild the screen"
    After you click **Apply**, right-clicking always opens the chart, not the settings. To show a different market, break all displays of the screen and place them again. The screen keeps its settings as long as one of its displays is still there.

## Related pages

- [Price chart and order book](price-chart.md): reading the chart.
- [Trading item for item](pair-trading.md): what the exchange rate means.
- [Blocks and recipes](blocks-and-recipes.md): crafting the display.
