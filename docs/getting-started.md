---
title: "Getting started"
description: "Your first ten minutes as a player: check your bank account, deposit items, build a Stock Market Block and make your first trade."
---

# Getting started

This page takes you from a fresh start to your first trade. You check your bank account, put items into it, sell some of them on the stock market, buy something back and take it out again. It takes about ten minutes.

## Before you start

- The server runs **BankSystem** and **StockMarket**.
- You have a few iron ingots, or another item that has a market on your server.
- You can craft a **Terminal Block**, a **Banking Software** and a **Trading Software**. The recipes are on the [BankSystem](banksystem/blocks-and-recipes.md) and [StockMarket](stockmarket/blocks-and-recipes.md) recipe pages.

## 1. Check your bank account

You already have a bank account. The mod opens a personal account for you the first time you join the server.

Type this in chat to see how much money is in it:

```text
/money
```

New players usually start with no money. Some servers give you a starting balance. Either way, your first money comes from selling items, as shown below.

## 2. Build a Bank Terminal

The **Bank Terminal Block** is where items go into the bank and come back out.

1. Place a **Terminal Block**.
2. Hold the **Banking Software** and right-click the Terminal Block. It turns into a **Bank Terminal Block**.

The software is not used up. Keep it: you can program more blocks with it later.

<figure markdown="span">
  ![Right-clicking a Terminal Block with Banking Software turns it into a Bank Terminal, and Trading Software turns another one into a Stock Market Block](assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: shared/program-terminal.gif</figcaption>
</figure>

## 3. Put items into the bank

1. Right-click the Bank Terminal Block. The bank screen opens. On the right you see the **Bank Terminal Inventory**: 27 slots that only you can see at this block.
2. Move your iron ingots from your inventory into those slots.
3. Click **Send items to bank**.

The iron leaves the slots and shows up in the item list on the left, with its balance.

<figure markdown="span">
  ![Sending a stack of iron to the bank at the Bank Terminal and taking ten back](assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/bank-terminal-deposit.gif</figcaption>
</figure>

Not every item can go into the bank. Iron ingots, gold ingots, diamonds, emeralds, coal and every item that has a market always can. Your server admin may allow more. Items that can't be banked stay in the slots, so you don't lose them.

## 4. Build a Stock Market Block

Place a second **Terminal Block**. Hold the **Trading Software** and right-click it. It turns into a **Stock Market Block**.

!!! tip "One block family"
    The Bank Terminal, the ATM and the Stock Market Block are all the same Terminal Block with different software. Right-click any of them with another software to reprogram it. See [How the two mods work together](together.md).

## 5. Sell your first items

1. Right-click the Stock Market Block. The trading screen opens.
2. Pick the iron market in the top bar, or find it with **Select Market**.
3. Open the **Market** tab.
4. Type a **Quantity**, for example `10`.
5. Click **Sell**.

The market sells the iron from your bank account right away. The money lands in the same account. The **Bank Balance** at the top of the screen goes up.

<figure markdown="span">
  ![The trading screen in Item / Money mode with the Market tab open](assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: stockmarket/trading-screen.png</figcaption>
</figure>

## 6. Buy something

Now use the money. Pick another market, type a **Quantity** and click **Buy**. The items land in your bank account, not in your inventory.

A market order like this trades at once, at the best price on offer. To trade at a price you choose, use a limit order instead. [Trading basics](stockmarket/trading.md) explains both.

## 7. Take your items out

1. Go back to the Bank Terminal Block and open it.
2. Find the item in the list on the left. Set the amount with the **+1**, **+10**, **+32** and **+64** buttons, or type it.
3. Click **Receive items from bank**.

The items appear in the Bank Terminal Inventory slots. Move them into your inventory.

## If something goes wrong

| Message | What it means | What to do |
|---|---|---|
| *<Item> is not allowed to be stored in the bank* | The server doesn't allow this item in the bank. | Ask your admin, or check whether the item has a market. |
| *The condition of <item> prevents banking it* | The item is in a state the bank can't store, for example spoiled food from another mod. | Keep it in your inventory. |
| Damaged or enchanted items stay in the slots | The bank only stores items in their plain state. | Take them back into your inventory. |
| The market you want isn't in the list | Nobody has created a market for that item. | Ask your admin. Only admins create markets. |

## Related pages

- [How the two mods work together](together.md): how the bank and the stock market share your account.
- [Bank Terminal](banksystem/bank-terminal.md): the bank screen in detail, including crafting from the bank.
- [Trading basics](stockmarket/trading.md): market and limit orders, and what each part of the trading screen does.
- [Bank accounts](banksystem/bank-accounts.md): shared accounts and who may use them.
