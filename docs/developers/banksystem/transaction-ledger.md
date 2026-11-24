---
title: "Transaction ledger"
description: "Ledger type codes and columns, and writing rows from your mod."
---

# Transaction ledger

BankSystem writes one ledger row for every balance change into the table `TransactionLog` of `Database/banksystem.db` on the master (see [Data files and backups](../../admin/backups.md#where-the-data-is)). Admins read it in the [Audit screen](../../admin/audit/investigating.md) and the [Audit Tool](../../admin/audit/audit-tool.md).

This page shows how your mod writes its own rows, what the type codes and columns mean, and how your mod adds its files to the audit export package.

## How rows are written

- **Only the master writes rows.** Every balance change runs on the master, also when a slave asked for it. The row then names the slave in `origin_server`.
- **Writes never block or fail the banking call.** Rows are queued and saved by a database thread. If a row can't be saved, BankSystem logs a warning and the banking call still counts.
- **Nothing is left out.** Every change of a bank's total balance (free + locked) writes a row where it happens. If no typed row covers it, BankSystem writes a `RAW_CHANGE` row. So for every account and item, the closing total minus the opening total is the sum of the signed rows in between.

Each row fires [`getTransactionLoggedEvent()`](events.md#ledger-rows) on the master. Subscribe to it if you only want to react to rows.

## Writing rows from your mod

```java
ITransactionLedger ledger = BankSystemMod.getAPI().getLedger();

// A row with your own type and actor
ledger.log(accountNumber, LedgerType.ADMIN_ADD, MoneyItem.getItemID(), rawAmount,
        LedgerActor.console(), /* ref */ null, /* note */ "event reward");
```

| Parameter of `log` | Meaning |
|---|---|
| `accountNumber` | The account the row belongs to |
| `type` | A `LedgerType`, see [Type codes](#type-codes) |
| `item` | The item of the bank that changed |
| `amount` | Raw amount (100 = 1.00); unsigned except for the types listed under the table |
| `actor` | Who caused it, see below |
| `ref` | Optional text that groups related rows, for example your order id |
| `note` | Optional free text |

Every call is thread-safe and returns at once. On a slave, and before the server has started or after it stopped, `log` and `logTrade` do nothing. Call them on the master, where the value moves.

Your rows are treated like BankSystem's own: they fire the ledger event and run through the admin audit and suspicion checks. An `ADMIN_*` row lands in the [audit log](../../admin/audit/reports.md#the-audit-log), and a large incoming transfer into a new account can raise a flag.

### Actors

`LedgerActor(UUID uuid, String name, Source source)` says who caused a change. Use the factories:

| Factory | `source_kind` |
|---|---|
| `LedgerActor.player(uuid, name)` | `PLAYER` |
| `LedgerActor.admin(uuid, name)` | `ADMIN` |
| `LedgerActor.console()` | `CONSOLE` |
| `LedgerActor.system()` | `SYSTEM` |
| `LedgerActor.stockmarket()` | `STOCKMARKET` |
| `LedgerActor.unknown()` | `UNKNOWN` |

### Trade rows

`logTrade(TradeLogEntry)` writes a `TRADE_BUY` or `TRADE_SELL` row with source `STOCKMARKET`. StockMarket uses it for order fills.

```java
ledger.logTrade(new TradeLogEntry(accountNumber, playerUuid, TradeSide.BUY,
        itemId, qtyRaw, currencyId, moneyRaw, avgPriceRaw, virtualQtyOrNull,
        orderRef, TradeRowKind.PERIODIC, System.currentTimeMillis(), /* note */ null));
```

Trade rows are **deltas**: all rows with the same `ref` add up to the order's totals. `TradeSide.BUY` writes `TRADE_BUY`, `SELL` writes `TRADE_SELL`. `TradeRowKind` goes into the `tag` column: `PERIODIC` (a regular update of an open order), `SHUTDOWN` (written when the server stops) or `CLOSE` (the order filled or was cancelled).

### Avoiding double rows

A raw bank call (`deposit`, `withdraw`, `setBalance`, `withdrawLocked…` and their async and `Real` variants) writes its own `RAW_CHANGE` row. If your mod writes a typed row for the same movement, make the bank calls inside `callerLogs`, so the movement isn't logged twice:

```java
ledger.callerLogs(() -> {
    itemBank.deposit(qty);
    return moneyBank.withdrawLockedPrefered(cost);
});
ledger.logTrade(entry);
```

`callerLogs` works on the master, on the current thread only, and can be nested. It returns what the body returns. Transfers still write their `TRANSFER` pair inside it.

What writes rows on its own:

- Raw bank calls that no typed row covers: `RAW_CHANGE` with the signed change, source `UNKNOWN` (or the player of a slave request), and the call's name in the note.
- Creating a bank with a start balance, and removing banks that still hold a balance: `RAW_CHANGE`.
- Binding a bank to a [currency mod](currency-integration.md) or unbinding it: `EXTERNAL_BIND` or `EXTERNAL_UNBIND` with the change it caused.
- Transfers, also from the locked balance: a `TRANSFER` pair.
- Lock and unlock only move value between free and locked, and write nothing.

!!! note "Slaves write untyped rows"
    `log` does nothing on a slave, and the async bank calls carry no type. So a deposit or withdrawal your mod makes on a slave shows up on the master as a `RAW_CHANGE` row with the slave in `origin_server`. If you need typed rows, make the change on the master.

## Type codes

The code is stored in `type_code`. Codes are never renumbered or reused; new types get new codes. `LedgerType.code()` gives a type's code, `LedgerType.fromCode(int)` the type of a code (`UNKNOWN_LEGACY` for an unknown code, never `null`).

| Code | Type | Written when |
|---:|---|---|
| 0 | `UNKNOWN_LEGACY` | An old row whose kind couldn't be mapped, or an unknown code |
| 1 | `DEPOSIT` | Items or money deposited at a Bank Terminal or by a deposit request |
| 2 | `WITHDRAW` | Items or money withdrawn (Bank Terminal, banknotes, withdraw request) |
| 3 | `TRANSFER` | A transfer between accounts; two rows, `-x` on the sender and `+x` on the receiver |
| 4 | `TRADE_BUY` | A StockMarket buy (`logTrade`) |
| 5 | `TRADE_SELL` | A StockMarket sell (`logTrade`) |
| 6 | `WITHDRAW_REFUND` | Part of a banknote withdrawal that couldn't be handed out and was put back |
| 7 | `ADMIN_SET` | An admin set a balance; amount = the change, note = `old->new` |
| 8 | `ADMIN_ADD` | `/money add` |
| 9 | `ADMIN_REMOVE` | `/money remove` |
| 10 | `ADMIN_UNLOCK` | An admin released a locked balance; amount = the released amount |
| 11 | `ADMIN_ACCOUNT_EDIT` | Account name, members, rights or icon changed; amount `0`, the note lists the changes |
| 12 | `BANK_CLOSED` | An account was deleted while it still held a balance; one row per item, amount = the lost balance |
| 13 | `CONVERTER_DEPOSIT` | The Bank Converter put items into the bank |
| 14 | `CONVERTER_WITHDRAW` | Reserved; not written at the moment |
| 15 | `UPLOAD_DEPOSIT` | A Bank Upload block deposited items; actor = block owner, note = position |
| 16 | `DOWNLOAD_WITHDRAW` | A Bank Download block withdrew items; actor `SYSTEM`, note = position |
| 17 | `CRAFT_CONSUME` | Crafting used ingredients from the bank |
| 18 | `CRAFT_OUTPUT` | A crafted result went back into the bank |
| 19 | `STARTING_BALANCE` | The starting balance of a new personal account |
| 20 | `PAYOUT` | A company payout; a pair like `TRANSFER`, `company_id` set |
| 21 | `DIVIDEND` | A dividend; a pair per holder, `company_id` set |
| 22 | `SHARE_STAMP` | Shares stamped at a Share Stamper |
| 23 | `SHARE_REDEEM` | Shares turned back at a Share Stamper |
| 24 | `SHARE_TRADE` | Stamped shares put into or taken out of a bank |
| 25 | `ACCOUNT_DELETE_PAYOUT` | A deleted user's balance handed to them as items |
| 26 | `ACCOUNT_FREEZE` | An account was frozen or unfrozen; amount `0`, item `0`, note `frozen` or `unfrozen` |
| 27 | `ADMIN_DISALLOW_ITEM` | An admin disallowed an item; one row per holder with the removed balance |
| 28 | `ACCOUNT_DELETE_LOSS` | A deleted user's balance that couldn't be handed out and was destroyed; the note ends with `not delivered: <reason>` |
| 29 | `RAW_CHANGE` | A change no other row covers (see [Avoiding double rows](#avoiding-double-rows)); signed, the note names the call |
| 30 | `EXTERNAL_BIND` | A bank was bound to a currency mod account; signed change of the total, note `bound to <provider>:<account>` |
| 31 | `EXTERNAL_UNBIND` | A bank was unbound; signed change, the note says where the funds stayed |
| 32 | `REFUND_LOST` | A marker, no balance change: banknotes withdrawn for a player weren't handed out, and the refund couldn't be booked back |

Amounts are unsigned, except for `TRANSFER`, `PAYOUT` and `DIVIDEND` (`-x` on the payer, `+x` on the receiver), `RAW_CHANGE`, `EXTERNAL_BIND` and `EXTERNAL_UNBIND`. `REFUND_LOST` rows move nothing and don't count in the balance sum.

## Columns

| Column | Meaning |
|---|---|
| `id` | Row id, in insert order |
| `account_number` | The account the row belongs to |
| `actor_uuid`, `actor_name` | Who caused it; the UUID is empty for console and system |
| `source_kind` | `PLAYER`, `ADMIN`, `CONSOLE`, `SYSTEM`, `STOCKMARKET` or `UNKNOWN` |
| `type_code` | The type code above |
| `kind` | The type name, for older readers |
| `item_id` | The item of the bank that changed |
| `amount` | Raw amount |
| `other_account` | The other account of a transfer, payout or dividend |
| `company_id` | The company of payout, dividend and share rows |
| `ts` | Time in epoch milliseconds |
| `note` | Free text, for example `old->new` or a block position |
| `ref` | A reference: a StockMarket order id, or a slave's transfer id |
| `tag` | Trade rows: `PERIODIC`, `SHUTDOWN` or `CLOSE` |
| `money_amount`, `price`, `currency_item` | Trade rows: money moved, average price, currency item |
| `virtual_qty` | Trade rows: amount filled against bot orders, with no other account |
| `balance_after` | Bank total (free + locked) right after the change; empty for trade rows |
| `origin_server` | The slave whose request caused the row; empty for changes made on the master |
| `dimension`, `x`, `y`, `z` | The block where it happened (Bank Terminal, upload or download block, ATM, Share Stamper); empty when no block was involved |

## Suspicion flags

BankSystem's own checks raise suspicion flags and alert admins. What each flag means for an admin is on [Alerts and suspicion flags](../../admin/audit/alerts.md#banksystem-flags). Your mod can listen to them with [`getSuspicionFlaggedEvent()`](events.md#suspicion-flags), but can't raise flags: there is no API call for it.

| Code | Name | Raised when |
|---:|---|---|
| 1 | `BANKNOTE_LAUNDERING` | Banknotes are deposited in a suspicious pattern |
| 2 | `LARGE_NOTE_WITHDRAWAL` | Large banknote withdrawals in a short burst |
| 3 | `WEALTH_JUMP` | An account's total wealth jumps (needs an [item price provider](item-price-provider.md)) |
| 4 | `TRANSFER_TO_NEW_ACCOUNT` | A large transfer, payout or dividend into a new account |
| 5 | `MONEY_SUPPLY_GROWTH` | The server's money supply grows fast; account `0` |
| 6 | `TRANSFER_PARKED` | A transfer to a slave whose outcome stayed unknown; `ref` = the transfer id |
| 7 | `EXTERNAL_BINDING_SUSPENDED` | A currency binding was suspended at startup; `ref` = `provider:account` |
| 8 | `SHARE_EXCESS` | A company has more shares in bank accounts than it stamped; on the company account |
| 9 | `SHARE_CREATED` | Share items were created with `/give` or the creative inventory; on the company account |

Codes are never reused. An unknown code reaches your listener with the name `FLAG_<code>`.

## Adding your files to the audit export

`/banksystem backup export [name]` writes one package for the Audit Tool: a folder `<world>/audit_exports/<yyyyMMdd-HHmmss>[-name]/` and a zip with the same content (see [The export package](../../admin/backups.md#the-export-package)). Your mod can add its own files with `AuditExport` (`net.kroia.banksystem.api.audit`):

```java
// once, when your mod starts; on master and slave servers alike
AuditExport.register("mymod", ctx -> {
    Path data = server.getWorldPath(LevelResource.ROOT).resolve("data/MyMod");
    ctx.copyFile(data.resolve("settings.json"), "data/MyMod/settings.json");
    ctx.copyDir(data.resolve("orders"), "data/MyMod/orders");
    ctx.addDatabase("data/MyMod/Database/mymod.db",
            target -> myDb.vacuumInto(target)); // returns a CompletableFuture<Void>
});
```

Registering the same mod id again replaces the earlier participant. For every export, BankSystem calls each participant on the server thread with a `Context`. The context is only valid during that call.

| `Context` method | What it does |
|---|---|
| `packageRoot()` | The package folder (absolute path) |
| `isSlave()` | `true` on a slave |
| `copyFile(Path src, String relPath)` | Copies one file now, on the server thread, so it can't clash with your own saves. A missing file is skipped and marked `missing`. |
| `copyDir(Path src, String relPath)` | Copies a folder with everything in it. A missing folder is skipped. |
| `addDatabase(String relPath, Function<Path, CompletableFuture<Void>>)` | BankSystem passes the target file (folders already created). Write a consistent copy of your database there on your own database thread, for example with SQLite's `VACUUM INTO`, and complete the future. |

`relPath` is relative to the package, with `/`. Use the same layout as the world's `data/` folder, for example `data/MyMod/...`. A path that leads outside the package throws `IllegalArgumentException`.

BankSystem waits for all database copies without blocking the server thread, at most 5 minutes. A failed or late future fails the export.

`manifest.json` at the package root lists the server (`server_uid`, `role` master, slave or single, Minecraft version, loader, mods) and, per mod id, every file with its path, method (`file_copy`, `vacuum_into` or `missing`), size and SHA-256.

## Related pages

- [Events and signals](events.md): react to rows and flags.
- [BankSystem API](api.md): the bank calls that write rows.
- [Alerts and suspicion flags](../../admin/audit/alerts.md): what admins see.
- [Audit Tool](../../admin/audit/audit-tool.md): where the export package is read.
