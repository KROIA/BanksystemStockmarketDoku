---
title: "Your company on the stock market"
description: Open a StockMarket market for your company's shares, pause it, and close it for good.
---

# Your company on the stock market

With StockMarket installed, your company's shares can get their own market. Players then buy and sell your shares like any other item, at prices they set themselves. Without StockMarket, shares can still be handed over as items, and they still earn [dividends](payouts.md).

## Before you start

- At least one share must exist. Stamp one with the [Share Stamper](shares.md) first.
- You need **Allowed to manage** on the company account, or be a founder.

## Opening the market

1. In [Company Management](companies.md#the-company-management-screen), open the **Market** tab. It says *No market exists for this company's shares yet.*
2. Enter the **Initial price**: the starting price of one share.
3. Click **Create Market**.

The tab now says *A market exists for this company's shares.* and shows the live price chart. **Open in StockMarket** opens the market in the trading screen.

<figure markdown="span">
  ![The Market tab of Company Management with an open market](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/company-market-tab.png</figcaption>
</figure>

## How a share market differs

A company market has no market bots. Only players trade on it, so:

- The price only moves when players trade. The initial price is just the start.
- Someone has to sell before anyone can buy. To bring shares onto the market, put them into a bank account at a [Bank Terminal](bank-terminal.md) and place sell orders. See [Trading company shares](../stockmarket/company-shares.md).

## Pausing trading

**Pause trading** stops the market for players. All open player orders are cancelled, and the money and shares in them go back to their owners. The price history stays. The market shows *Under Maintenance* in the trading screen.

**Resume trading** opens it again, with an empty order book.

## Closing the market for good

Only founders can do this.

1. Type the exact company name into the box under **Close market**.
2. Click **Close market** and confirm.

!!! danger "This can't be undone"
    The market and its whole price history are deleted. You can create a new market later, but it starts from scratch.

## If something goes wrong

| Message | What it means | What to do |
|---|---|---|
| *No share item found for this company.* | No share of the company has been stamped yet. | Stamp at least one share. |
| *A market already exists for this share item.* | The market is already there. | Nothing to do. |
| *This share item is blacklisted from trading.* | The admin doesn't allow a market for it. | Ask your admin. |
| *Please enter a valid positive price.* | The initial price is empty, zero or not a number. | Enter a price above zero. |
| *You do not have permission to do this.* | You lack **Allowed to manage**, or you tried to close the market without being a founder. | Ask a manager or a founder. |
| *Market integration not available.* | StockMarket isn't installed or isn't answering. | Ask your admin. |

## Related pages

- [Trading company shares](../stockmarket/company-shares.md): the shareholder's side.
- [Shares and the Share Stamper](shares.md): making the shares.
- [Trading basics](../stockmarket/trading.md): how orders work.
