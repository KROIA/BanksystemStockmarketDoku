---
title: "Player commands"
description: Every BankSystem command a normal player can use, for money, bank accounts and companies.
---

# Player commands

These commands work for every player. Commands for admins are on the [Admin commands](../admin/commands.md) page.

Put names with spaces in quotes, for example `/company info "Iron Works"`. Press ++tab++ while typing to complete player and company names.

## Money

| Command | What it does |
|---|---|
| `/money` | Shows your money balance. |
| `/money send <player> <amount>` | Sends money from your personal account to the player's personal account. |
| `/money circulation` | Shows how much money all players have together. |

See [Money and the ATM](money.md).

## Bank accounts

| Command | What it does |
|---|---|
| `/bank` | Shows the balances of your personal account, money and items. |
| `/bank manage` | Opens the management screen of your personal account. |
| `/bank manage <name>` | Opens the management screen of another account you have access to. |
| `/bank create <name>` | Creates a new bank account. Each player can create 3 by default. |

See [Bank accounts](bank-accounts.md).

## Companies

| Command | What it does | Who can use it |
|---|---|---|
| `/company create "<name>" <max supply>` | Founds a company with its own bank account. The max supply (1 to 1,000,000,000) can't be changed later. | Everyone |
| `/company info "<name>"` | Shows the company's founders, max supply, issued shares and description. | Everyone |
| `/company manage "<name>"` | Opens the Company Management screen. | Managers of the company |
| `/company shares acknowledge "<name>"` | Accepts the share count after more shares turned up than were stamped, so dividends run again. | Managers and founders |

See [Founding and running a company](companies.md) and [Payouts and dividends](payouts.md#when-a-payout-fails).

## StockMarket

StockMarket has one player command: `/stockmarket news` opens the [market news](../stockmarket/newspaper.md).

## Related pages

- [Bank accounts](bank-accounts.md): what `/bank` manages.
- [Founding and running a company](companies.md): the `/company` commands in context.
- [Admin commands](../admin/commands.md): commands for server admins.
