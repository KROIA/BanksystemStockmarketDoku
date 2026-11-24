---
title: "Daily digest and reports"
description: "The daily audit digest, on-demand reports with /banksystem auditreport, and the audit log files."
---

# Daily digest and reports

BankSystem writes plain files you can read without starting the game: a log of every admin action and flag, a daily summary, and summaries on demand. All of them are written by the master server into

```text
<world>/data/BankSystem/audit/
```

BankSystem never deletes these files. Clean them up yourself if the folder gets large.

## The audit log

`<yyyy-mm-dd>.log` gets one line per event of that day:

- every admin change to an account: balances set, added or removed, amounts unlocked, banks closed, accounts edited, frozen or unfrozen;
- items allowed or removed by an admin, with one extra line for every account that lost an item;
- BankSystem admin rights given or taken, and slave servers trusted or untrusted;
- share alerts accepted with `/company shares acknowledge`;
- every [suspicion flag](alerts.md).

Each line has the time, what happened, the account, item and amount, and who did it: a player's name and UUID, `Console`, or `LuckPerms` when the [LuckPerms sync](../permissions.md) changed an admin flag.

## The daily digest

On the first server tick after midnight, the master writes a summary of the day before to `digest-<yyyy-mm-dd>.md`. It is a Markdown file with:

- the money supply at the start and end of the day, and the change;
- the accounts that gained the most cash;
- every suspicion flag of the day;
- how many admin actions of each kind there were, and the last 20.

If the server was offline at midnight, the digest is written at the next start. A digest that already exists is never written again.

| Setting | Default | What it does |
|---|---|---|
| **Daily audit digest** | on | Writes the daily digest. |
| **Digest: top gainers** | `10` | How many accounts the gainers list shows, 1 to 100. |

Both are under **Suspicious activity** in the [Mod Settings](../banksystem/settings.md#suspicious-activity).

## A report on demand

```text
/banksystem auditreport <hours>
```

writes the same summary for the last 1 to 720 hours, to `digest-<date>_<time>-<hours>h.md`, and tells you the full path. Run on a slave server, the report is written on the master.

Cash values come from the balance history, so the digest needs **Balance snapshot interval (minutes)** to be on.

## StockMarket

StockMarket writes its alerts to the server log, as lines starting with `[StockMarket Alert]`. The master also keeps every alert, and the server each order was placed on, in `<world>/data/StockMarket/Database/stockmarket_diagnostics.db`. You can open it with any SQLite browser. The [Audit Tool](audit-tool.md) reads it too.

## Related pages

- [Alerts and suspicion flags](alerts.md): what the flags mean.
- [Investigating in game](investigating.md): follow an account in the Audit screen.
- [Data files and backups](../backups.md): every data file of both mods.
