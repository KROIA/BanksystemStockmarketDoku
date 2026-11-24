---
title: "Audit and anti-cheat"
description: "What both mods record about money, items and trades, where it is stored and how to read it."
---

# Audit and anti-cheat

Both mods keep records of every balance change and every trade. When something goes wrong, for example a duplication exploit or stolen money, these records show who gained what and how. This page says what is recorded and where to read it.

All records are written by the master server. On a network, it also records what happens on the slave servers, with the server it came from.

## What is recorded

| Record | Holds | Read it with |
|---|---|---|
| **Transaction ledger** | Every balance change of every account: deposits, withdrawals, transfers, payouts, dividends, trades, admin edits, freezes. Each entry has the time, the amount, who caused it and the balance afterwards. | The [Audit screen](investigating.md#the-audit-screen) |
| **Balance history** | The balances of all accounts over time. | The [balance chart](investigating.md#balance-history-with-flags) and the [server history](investigating.md#the-whole-server) |
| **Suspicion flags** | Patterns that often mean cheating, such as large withdrawals or sudden wealth. | [Chat alerts](alerts.md), markers on the balance chart, the audit log |
| **Audit log** | Every admin action and flag, one plain text file per day. | Any text editor, see [Daily digest and reports](reports.md) |
| **Daily digest** | A summary of each day: money supply, biggest gainers, flags, admin actions. | Any Markdown viewer, see [Daily digest and reports](reports.md) |
| **Banknote flow** | Banknotes that enter or leave the world outside the bank, for example from `/give` or the creative inventory. | The [Audit Tool](audit-tool.md) |
| **Trade alerts and order origin** | StockMarket's alerts, and on which server each order was placed. | The server log and the [Audit Tool](audit-tool.md) |

The records are kept in SQLite databases and text files in the world folder, see [Data files and backups](../backups.md). They are never cleaned up automatically, except that old balance history is thinned out.

## Where to start

- **An alert came in:** read what it means in [Alerts and suspicion flags](alerts.md), then open the account as shown in [Investigating in game](investigating.md).
- **A player reports missing money:** open their account in the [Audit screen](investigating.md#the-audit-screen) and follow the money.
- **A big case across several servers:** export the saves and load them into the [Audit Tool](audit-tool.md).
- **A daily look at the economy:** read the [daily digest](reports.md#the-daily-digest).

!!! tip "Freeze first, then investigate"
    While you look into an account, [freeze it](../banksystem/accounts.md#freezing-an-account). Nothing can move in or out, and nothing is lost.

## Related pages

- [Alerts and suspicion flags](alerts.md): what both mods warn about.
- [Investigating in game](investigating.md): the Audit screen and the balance charts.
- [Audit Tool](audit-tool.md): the offline tool for big cases.
