---
title: "How the two mods work together"
description: "How your bank account, the Terminal Block and company shares connect BankSystem with StockMarket."
---

# How the two mods work together

!!! info "Not written yet"
    This page will cover: The Terminal Block family (Bank Terminal, ATM and Stock Market Block are one block with different software); your bank account as your trading wallet (which accounts can trade, money and items reserved while an order is open, frozen accounts); company shares as markets; villagers paying in money; total wealth from market prices.

<!-- Sources for the rewrite:
  - SM:README.md#getting-started
  - SM:code screen/TradeScreen.java (account selector), networking/request/CreateOrderRequest.java
  - BS:code minecraft/block/custom/TerminalBlock.java, integration/stockmarket/StockMarketBridge.java
-->

<figure markdown="span">
  ![Items move between your inventory and your bank account at the Bank Terminal, and between your bank account and the markets at the Stock Market Block; company shares get their own market](assets/images/shared/economy-overview.svg){ width="600" }
</figure>

<figure markdown="span">
  ![Terminal Block, Bank Terminal Block, ATM and Stock Market Block side by side](assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: shared/terminal-family.png</figcaption>
</figure>
