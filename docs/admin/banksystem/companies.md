---
title: "Companies and shares"
description: "Company limits, share symbols, share alerts and admin actions on company accounts and markets."
---

# Companies and shares

Players found and run their companies themselves, see [Founding and running a company](../../banksystem/companies.md). This page covers what you can do as an admin. You need the BankSystem admin flag, see [Admins and permissions](../permissions.md).

## Limits

**Max companies per player** in the [Mod Settings](settings.md#player) sets how many companies a player may found (default 3). A company also uses one of the player's bank accounts, so **Max bank accounts per player** must leave room for it.

## Managing any company

`/company manage "<name>"` opens the management screen of any company for you, as if you had the **Manage** right on its account. You can edit workers, payouts, the share visuals and the description, and pause or resume its market.

Some actions stay with the founders, even for admins:

- **Transfer founder** and **Dissolve company**
- **Close market**

The company's money is in a normal bank account. Open it like any other, see [Managing accounts](accounts.md).

## Share integrity

Each company knows how many shares it has stamped. The master server compares that number with the shares held in all bank accounts. More shares in the banks than were ever stamped means shares were copied somewhere.

When that happens, BankSystem doesn't remove anything. Instead:

- A **share excess** flag is raised on the company's account. It shows the stamped and banked numbers, the share deposits since the numbers last matched, and per player how many shares they took out or deposited. That last part is a hint, not proof: shares can change hands as items without a record.
- The company's **dividends are paused**. **Pay Dividend** and dividend schedules are skipped with the status *Paused*. Normal payouts keep running.

The check runs after every share deposit and once a day. There is only one open alert per company; a new one only comes if the excess grows.

When you have looked into it, accept the current numbers:

```text
/company shares acknowledge "<name>"
```

This marks the flag as reviewed and resumes the dividends. The company's own admins (founders and players with **Manage**) can run it for their company too. If the extra shares are destroyed and the numbers match again, the alert closes and dividends resume by themselves.

Shares that disappear for good lower the stamped number: shares in a deleted account or a closed bank, and shares you remove in the [account screen](accounts.md#what-you-can-change).

!!! warning "Shares from /give or the creative inventory"
    Stamped shares taken from `/give` or the creative inventory raise a **share created** flag at once, with the player's name. Hand out shares only through a Share Stamper.

See [Alerts and suspicion flags](../audit/alerts.md) for how flags reach you.

## Share symbols

The symbols players can pick in the **Share Visuals** editor are PNG images on the master server. BankSystem comes with 45. You can add your own, up to 256 in total.

To add a symbol:

1. Make a square PNG, 64 × 64 pixels or smaller, with a power of two as its size (16, 32 or 64), at most 128 KB.
2. Put it into `<world>/data/BankSystem/share_symbols/inbox/` on the master server. The file name is the symbol id: lowercase letters, digits and `_`, at most 32 characters, for example `rocket.png`.
3. Run `/banksystem symbols add rocket`.

An existing id is replaced. The new symbol reaches all players and slave servers at once.

| Command | What it does |
|---|---|
| `/banksystem symbols list` | Lists all symbols. |
| `/banksystem symbols add <id>` | Adds or replaces a symbol from the inbox folder. |
| `/banksystem symbols remove <id>` | Removes a symbol. |
| `/banksystem symbols reload` | Reads the symbol folder again after you changed files in it by hand. |

All four commands work on the master server only.

## Related pages

- [Founding and running a company](../../banksystem/companies.md): the player's view.
- [Your company on the stock market](../../banksystem/company-market.md): pausing and closing a share market.
- [Alerts and suspicion flags](../audit/alerts.md): all flags in one table.
