---
title: Currency bindings
description: Link a slot of your bank account to an account in Numismatics or Lightman's Currency, so both mods use the same money.
---

# Currency bindings

If your server also runs a currency mod, you can link it to BankSystem. A **binding** connects one item of your bank account to an account in the other mod. From then on, both mods use the same money: what you pay in at the currency mod's own machines shows up in BankSystem, and what you spend on the stock market comes out of the currency mod's account.

BankSystem supports two currency mods:

| Currency mod | Fabric | NeoForge |
|---|:---:|:---:|
| Numismatics | yes | yes |
| Lightman's Currency | no | yes |

Bindings are optional. Nothing is linked until you bind a slot yourself.

## What changes after binding

- The balance of the bound item is read live from the currency mod.
- Deposits and withdrawals at the [Bank Terminal](bank-terminal.md), the [ATM](money.md) and the [automation blocks](automation.md) move money in the currency mod's account.
- Trades on the stock market with this bank account do the same.
- Your account rights stay as they are in BankSystem.

## Before you start

- You need **Allowed to manage** on the bank account.
- You need an account in the currency mod. With Numismatics, you get one when you join the world. With Lightman's Currency, right-click any of its ATMs once.
- The bank account already has a slot for the currency mod's base coin: **Spur** for Numismatics, the gold coin for Lightman's Currency. Only that slot can be bound.

## Binding a slot

1. Open the management screen of the account (`/bank manage <name>`) and click **Bindings**. The **Currency Bindings** screen lists every item of the account with its balance.
2. Click **Bind...** next to the currency slot.
3. If both currency mods are installed, pick one under **Pick a currency mod**.
4. Under **Pick an account**, choose the account in the currency mod.
5. Confirm. Any balance already in the slot moves to the currency mod's account.

The row now shows the currency mod's account and an **Unbind** button.

<figure markdown="span">
  ![The Currency Bindings screen with one slot bound to an external account](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/currency-bindings.png</figcaption>
</figure>

### Personal and shared accounts

You can only bind accounts of the same kind:

- A **personal** bank account binds to a personal account in the currency mod.
- A **shared** bank account binds to a shared one: a Blaze Banker you are trusted on (Numismatics) or a team account you belong to (Lightman's Currency). These show a **shared** badge in the list.

If the kind you need is missing, create it first: a shared bank account with `/bank create <name>`, or a Blaze Banker or team in the currency mod.

With Numismatics, every user of the shared bank account who has **Allowed to withdraw** is added to the Blaze Banker's trust list. With Lightman's Currency, you manage the team members in that mod yourself.

<figure markdown="span">
  ![Choosing the external account when binding a slot](../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: banksystem/currency-bind-dialog.png</figcaption>
</figure>

## Paying in other coins

Currency mods have coins of different values. At a Bank Terminal, you can pay in any coin of the bound currency. Its value is added to the bound slot. For example, a Numismatics Crown adds its value in Spurs. When you take money out, you get the currency mod's coins, as from its own ATM.

Without a binding, each coin type is just a separate item in your bank.

## Unbinding

Click **Unbind** and choose where the money goes:

| Choice | What happens |
|---|---|
| **Keep on BankSystem** | The money moves from the currency mod into the BankSystem slot. Pick this if the currency mod is going away. |
| **Keep on** *currency mod* | The money stays in the currency mod's account. The BankSystem slot is emptied. Amounts below one unit are lost. |
| **Cancel** | Nothing changes. |

## Good to know

- The Currency Bindings screen doesn't update by itself. After paying in or out at the currency mod's own machines, click **Refresh**.
- If you spend money in the currency mod that BankSystem had reserved for open stock market orders, those orders are cancelled.
- A greyed-out row means the currency mod isn't running or the admin switched it off. The binding stays, but no money moves until it is back.
- A row marked *Suspended* must be checked by an admin first. Until then, nothing can be paid in or out through it.

## If something goes wrong

| Message | What it means | What to do |
|---|---|---|
| *The slot's item (…) does not match …'s currency* | You tried to bind a slot that isn't the currency mod's base coin. | Bind the base coin slot. |
| *The existing balance would overflow the external account* | Numismatics accounts can hold at most about 2.1 billion Spurs. | Take some money out of the slot, then bind. |
| *Personal and shared accounts cannot be mixed on a binding.* | The two accounts are of different kinds. | Pick an account of the same kind. |
| *No external currency mods are installed on this server.* | The server has no supported currency mod. | Ask your admin. |
| *The external currency mod is not available.* | The currency mod is switched off or was removed. | Ask your admin. |
| The **Bind...** button is greyed out, *Requires MANAGE permission* | You don't have **Allowed to manage**. | Ask a manager of the account. |

## Related pages

- [Bank accounts](bank-accounts.md): personal and shared accounts, rights.
- [Money and the ATM](money.md): BankSystem's own money.
- [How the two mods work together](../together.md): trading with your bank account.
