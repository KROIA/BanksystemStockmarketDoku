---
title: Villager trading
description: How villager prices follow the stock market, and how you pay villagers with banknotes and coins.
---

# Villager trading

With StockMarket on the server, villagers trade for money instead of emeralds. Their prices follow the stock market: when the market price of wheat goes up, a farmer pays you more for it. This page explains what changes for you.

<figure markdown="span">
  ![A villager's trade screen with prices in money](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: stockmarket/villager-trade.png</figcaption>
</figure>

## Which trades change

A villager trade changes to money when the item it trades has a market on your server. Trades for items without a market keep using emeralds, unless your admin has changed that. Wandering traders work the same way.

## Paying with money

Villagers take BankSystem banknotes and coins, not your bank balance. Take money out at an [ATM](../banksystem/money.md) before you go trading.

- Put any mix of banknotes and coins into the payment slots. They only need to add up to the price. For example, two 10 Dollar notes pay for a 20 Dollar trade.
- If you pay too much, the villager gives you change.
- When a villager buys from you, you get banknotes and coins. Put them into the bank at a Bank Terminal to use them for trading.

## How prices are set

Villager prices come from the market price, with a margin:

- **A villager buys** from you for less than the market price. By default it pays 80% of it.
- **A villager sells** to you for more than the market price. By default it charges 120% of it.

So the stock market usually gives you a better price than a villager. Villagers are handy when you're far from a Stock Market Block, or when nobody on the market wants your items.

The prices don't change with every trade on the market. The server updates them every 20 minutes by default.

!!! note "Villager trades don't move the market"
    Trading with a villager never places an order on the stock market. It doesn't change any market price.

Discounts from curing a zombie villager or from the Hero of the Village effect still apply, up to 20% off.

## Related pages

- [Money and the ATM](../banksystem/money.md): getting banknotes and coins.
- [Trading basics](trading.md): selling on the market instead.
- [How the two mods work together](../together.md): the bank, the market and villagers in one picture.
