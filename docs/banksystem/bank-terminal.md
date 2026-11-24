---
title: Bank Terminal
description: Put items into your bank and take them out at the Bank Terminal, craft with bank items, and read the balance history of your account.
---

# Bank Terminal

The **Bank Terminal Block** is where items go into your bank account and come back out. You can also craft with the items in your bank without taking them out first, and look at how your balances changed over time.

To make one, right-click a **Terminal Block** with **Banking Software**. See [Blocks and recipes](blocks-and-recipes.md).

<figure markdown="span">
  ![The Bank Terminal with the item banks of the account and the player inventory](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/bank-terminal.png</figcaption>
</figure>

## The screen

Right-click the Bank Terminal Block. The screen has two halves:

- **On the left**, the items in your bank account, one line per item with its balance. Type in the **Filter** box to find an item by name. The account button at the top switches to another account you have access to.
- **On the right**, the **Bank Terminal Inventory** (27 slots), a crafting grid and your own inventory.

The Bank Terminal Inventory belongs to you alone. Other players using the same block see their own slots, like an ender chest.

## Putting items into the bank

1. Move the items from your inventory into the Bank Terminal Inventory slots.
2. Click **Send items to bank**.

Everything in the slots goes into the selected account. Items that can't be stored stay in the slots:

- Items the server doesn't allow in the bank. Ask your admin which items are allowed.
- Damaged or enchanted items. The bank only stores items in their plain state.

## Taking items out

1. Find the item in the list on the left.
2. Set the amount with the **+1**, **+10**, **+32** and **+64** buttons, or type it. The amount can't go above your balance.
3. Set amounts for more items if you want. One click takes them all out.
4. Click **Receive items from bank**.

The items appear in the Bank Terminal Inventory slots. Move them into your inventory.

<figure markdown="span">
  ![Sending a stack of iron to the bank at the Bank Terminal and taking ten back](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/bank-terminal-deposit.gif</figcaption>
</figure>

!!! warning "Don't leave items in the slots"
    When the Bank Terminal Block is broken or reprogrammed with another software, everything still in its slots drops on the ground. This counts for every player's slots. Items in the bank account are safe.

**Remove empty banks** removes the lines of items with a balance of zero from the list.

## Crafting with bank items

The 3×3 crafting grid works like a crafting table, with all normal recipes. Two checkboxes connect it to your bank:

- **Use Bank Items**: missing ingredients come from the bank account. Put at least one real item into the grid to start the recipe. Faded icons then show which items the bank will add. Money is never used as an ingredient. You need **Allowed to withdraw** on the account.
- **Auto-deposit output**: what you craft goes straight into the bank account, not into your inventory. You need **Allowed to deposit**. If the bank can't store the item, it goes to your inventory and a message says why.

The terminal remembers both checkboxes for you. Items left in the grid go back to your inventory when you close the screen.

<figure markdown="span">
  ![The crafting view of the Bank Terminal with Use Bank Items and Auto-deposit output turned on](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/bank-terminal-crafting.png</figcaption>
</figure>

### With JEI

If the JEI mod is installed:

- The **+** button in a JEI recipe fills the crafting grid. With **Use Bank Items** on, it only places the recipe pattern, and the bank supplies the ingredients when you craft.
- Clicking an item in the bank list looks up its recipes and picks one your bank can pay for.

## Balance history

The **History** button at the top right opens a chart of your account's balances over time, one coloured line per item. With StockMarket installed, a gold **Total Wealth** line shows the value of the whole account at market prices.

- The buttons **1h**, **6h**, **1d**, **7d**, **30d** and **all** set the time span.
- Drag to move the chart, scroll to zoom. ++space++ fits the view to the data, ++ctrl+space++ jumps back to now.
- The search box and the checkboxes next to each item turn lines on and off. The chart remembers your choice.

<figure markdown="span">
  ![The Balance History chart of an account over seven days](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/balance-history.png</figcaption>
</figure>

## If something goes wrong

| Message | What it means | What to do |
|---|---|---|
| *<Item> is not allowed to be stored in the bank* | The server doesn't allow this item in the bank. | Keep it, or ask your admin. |
| *The condition of <item> prevents banking it* | The item is in a state the bank can't store, for example spoiled food from another mod. | Keep it in your inventory. |
| *Crafted <item> could not be deposited into the bank and was moved to your inventory* | **Auto-deposit output** was on, but the bank can't store this item. | Nothing: the item is in your inventory. |
| The **Use Bank Items** checkbox is greyed out | You don't have **Allowed to withdraw** on this account. | Pick another account, or ask a manager for the right. |
| A chat message says the account is frozen | An admin has frozen the account. Nothing can move in or out. | Ask an admin. Your items stay where they are. |

## Related pages

- [Bank accounts](bank-accounts.md): sharing an account and its rights.
- [Automation](automation.md): move items into and out of the bank with redstone.
- [How the two mods work together](../together.md): what Total Wealth means.
