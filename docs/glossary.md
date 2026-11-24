---
title: Glossary
description: Short definitions of the bank and market words used on this site, from bank account to virtual order book.
---

# Glossary

Short definitions of the words this site uses. Each entry links to the page that explains it in full.

## Bank words

### Bank account

Holds your money and your items. You get a personal account the first time you join. You can also open shared accounts and give other players rights on them. A company has its own account. See [Bank accounts](banksystem/bank-accounts.md).

### Account rights

What a player may do with an account: **Allowed to deposit**, **Allowed to withdraw** and **Allowed to manage** (add users, change rights). To trade with an account you need both the deposit and the withdraw right.

### Item bank

One line in your account for one item, for example your iron or your money. It shows how many of that item you own. **Remove empty banks** in the Bank Terminal cleans up the lines with nothing in them.

### Bankable item

An item that is allowed in the bank. By default these are money, iron ingots, gold ingots, diamonds, emeralds, coal and every item that has a market. The server admin can allow more.

### Locked balance

Money or items in your account that are reserved by an open order. You can't spend or withdraw them until the order fills or you cancel it. See [Trading basics](stockmarket/trading.md#where-the-money-and-items-come-from).

### Frozen account

An account that an admin has stopped. It can't trade until the admin unfreezes it.

### Money

The bank's currency, shown in dollars and cents. In the bank it is a number. In your hand it is banknotes and coins from the **ATM**. See [Money and the ATM](banksystem/money.md).

### Company

A group with its own bank account, workers and shares. See [Founding and running a company](banksystem/companies.md).

### Share

A **Company Share** item that stands for a part of a company. Shares can have their own market. See [Shares and the Share Stamper](banksystem/shares.md).

### Supply

How many shares of a company exist, compared with the most it may issue.

### Dividend

Money a company pays to the people who hold its shares. See [Payouts and dividends](banksystem/payouts.md).

## Market words

### Market

The place where one item is traded for money. Each item has at most one market. Only admins create markets, except for company shares. See [Trading basics](stockmarket/trading.md).

### Order

Your request to buy or sell an amount of an item. The market matches it with orders of other players or bots.

### Market order

An order that trades right away at the best prices on offer. You choose the amount, not the price.

### Limit order

An order with your own price. It only trades at that price or better, and waits in the order book until then.

### Order book

The list of all limit orders that are waiting: buy orders below the current price, sell orders above it. The trading screen shows it along the right edge of the chart. See [Price chart and order book](stockmarket/price-chart.md).

### Spread

The gap between the highest buy order and the lowest sell order. A small spread means you lose little when you buy and sell again right away.

### Volume

An amount of items: either waiting in the order book or traded in a time span.

### Liquidity

How much volume waits close to the current price. On a liquid market, a big order barely moves the price. On a market with little liquidity, it can move the price a lot.

### Sweep

What happens when a big market order uses up the orders at the best price and keeps filling at worse and worse prices. The price jumps, and your average price is worse than the price you saw. See [Trading basics](stockmarket/trading.md#market-order-trade-now).

### Candle

One bar of the price chart. It shows the price at the start (open), the highest and lowest price, and the price at the end (close) of a time span.

### Timeframe

The time span of one candle, for example one minute or one hour. You switch it with the buttons on the chart.

### Item / Item mode

Trading one item directly for another, for example iron for diamonds, without handling money yourself. See [Trading item for item](stockmarket/pair-trading.md).

### Trading hours

The times when a market is open. Outside them you can't place new orders, and your open orders wait until the market opens. See [When a market is closed](stockmarket/trading.md#when-a-market-is-closed).

### Maintenance

A pause on one market, set by an admin. Open orders on it are cancelled and refunded.

### Trade cooldown

A short wait after each accepted order before you can place the next one. Half a second by default.

### Max order size

The most items one order may buy or sell on a market. Split bigger trades into several orders.

## Server words

These words appear on the [Server Admin](admin/index.md) pages.

### Abundance

A market setting that says how common an item is. A higher abundance gives the market more volume and a bigger default max order size.

### Virtual order book

Orders that market plugins add, not players. They give a market volume, so you can trade even when no other player is online. See [Choosing a market style](admin/stockmarket/setup-use-cases.md).

### Plugin

An add-on that runs on markets: it adds volume, moves the price, trades as a bot or reacts to news. See [Plugins](admin/stockmarket/plugins/index.md).

### Preset

A template for new markets with a start price, abundance and other settings. See [Presets](admin/stockmarket/presets.md).

### Master and slave

When several servers share one economy, the **master** keeps all bank accounts and markets. The **slaves** pass every bank and market action on to it. See [Several servers, one economy](admin/multi-server.md).
