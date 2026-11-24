---
title: "Companies, payouts and dividends API"
description: "Scheduling payouts, paying dividends and reading share visuals from another mod."
---

# Companies, payouts and dividends API

A company in BankSystem owns one bank account and issues shares. Players set up [payouts and dividends](../../banksystem/payouts.md) in the company screen. Your mod can do the same through two master-only interfaces, and draw a company's share icon on the client:

| Interface | From | Runs on |
|---|---|---|
| `IPayoutManager` | `api.getPayoutManager()` | Master |
| `IDividendPayer` | `api.getDividendPayer()` | Master |
| `IBankSystemVisualLookup` | `api.getVisualLookup()` | Client |
| `IShareIconRenderer` | `api.getShareIconRenderer()` | Client |

The API has no call to list companies. Each company has a number, shown as **Company ID** in the company screen (see [Founding and running a company](../../banksystem/companies.md#overview)). All methods below take that number as `companyId`.

## Payouts

A payout schedule moves an amount from the company account at a fixed interval.

```java
IPayoutManager payouts = api.getPayoutManager();
```

On a slave, every change returns `NOT_MASTER` and every read returns an empty list or a future of an empty list or `0`. There is no async variant: call it from code that runs on the master.

### Creating a schedule

```java
CreateOutcome created = payouts.createSchedule(
        companyId,
        workerUuid,                        // target player
        2500L,                             // raw amount: 25.00
        20L * 60 * 20,                     // interval in ticks: 20 minutes
        PayoutExecutor.getLastObservedTick(), // now, on the payout clock
        managerUuid,                       // who created it, or null
        PayoutSchedule.NO_TARGET_ACCOUNT,  // -1 = the target's personal account
        "Worker", "",                      // names shown in the screen
        PayoutSchedule.Mode.FIXED_PAYOUT,
        PayoutSchedule.MONEY_CURRENCY);    // 0 = money
if (created.result() == IPayoutManager.OpResult.OK) {
    long scheduleId = created.scheduleId();
}
```

| Parameter | Meaning |
|---|---|
| `target` | The player who gets the payout. Required for `FIXED_PAYOUT`. Set it for `ONE_TIME` too: a `ONE_TIME` without target isn't refused, but each run fails and it tries again every second. May be `null` for `DIVIDEND`. |
| `amount` | Raw amount per run (100 = 1.00), more than `0`. |
| `intervalTicks` | Ticks between runs, at least `20` (one second). |
| `nowTick` | The current tick of the payout clock: pass `PayoutExecutor.getLastObservedTick()` (in `net.kroia.banksystem.banking.company`). The first run is `intervalTicks` after it. Don't pass `server.getTickCount()`: schedules run on BankSystem's own counter, which can differ. |
| `createdBy` | Who created the schedule, or `null`. |
| `targetAccountNr` | A specific account of the target, or `-1` (`NO_TARGET_ACCOUNT`) for their personal account. A specific account needs the target to have the deposit right on it. |
| `targetPlayerName`, `targetAccountName` | Names shown in the company screen while the player or account can't be looked up. |
| `mode` | See below. |
| `currencyItem` | Short id of the paid item; `0` (`MONEY_CURRENCY`) = money. The company account needs a bank for that item. |

The short form `createSchedule(companyId, target, amount, intervalTicks, nowTick, createdBy)` creates a `FIXED_PAYOUT` in money to the target's personal account.

| `PayoutSchedule.Mode` | What a run does |
|---|---|
| `FIXED_PAYOUT` | Pays `amount` to the target. The default. |
| `DIVIDEND` | Splits `amount` as a total among all shareholders, by the shares they hold at that moment. |
| `ONE_TIME` | Pays `amount` to the target once, then removes itself. A failed run tries again one second later. |

Payouts are checked once per second. After a server restart, every schedule starts a full interval from that moment.

### Changing and removing schedules

| Method | Returns | What it does |
|---|---|---|
| `updateSchedule(companyId, scheduleId, newAmount, newIntervalTicks)` | `OpResult` | Changes amount and interval. Same limits as on creation. |
| `updateScheduleEx(companyId, scheduleId, newAmount, newIntervalTicks, nowTick, newTarget, newTargetAccountNr, newTargetPlayerName, newTargetAccountName, newMode, newCurrencyItem)` | `OpResult` | Changes everything. |
| `pauseSchedule(companyId, scheduleId, boolean paused)` | `OpResult` | Pauses or resumes. A paused schedule doesn't run and doesn't save up missed runs. |
| `deleteSchedule(companyId, scheduleId)` | `OpResult` | Removes the schedule. |
| `listSchedulesFor(companyId)` | `List<PayoutSchedule>` | A snapshot of the company's schedules. |
| `getHistory(scheduleId, limit)` | `CompletableFuture<List<PayoutHistoryRecord>>` | The last runs, newest first. |
| `getTotalPaidForSchedule(scheduleId)` | `CompletableFuture<Long>` | The raw total of all successful runs. |

`OpResult`: `OK`, `COMPANY_MISSING`, `SCHEDULE_MISSING`, `INVALID_INPUT` (amount `0` or less, interval under 20 ticks, or a `FIXED_PAYOUT` without target) or `NOT_MASTER`.

`PayoutSchedule` (in `net.kroia.banksystem.banking.company`) has getters for each field: `getScheduleId()`, `getTargetUUID()`, `getAmount()`, `getIntervalTicks()`, `getNextRunTick()`, `isPaused()`, `getMode()`, `getCurrencyItem()`, `getTargetAccountNr()`, `getMissedAmount()` and `getMissedCount()` (failed runs not paid yet), `isPausedByCurrencyBan()` (paused because an admin disallowed its item; allowing the item again resumes it) and more.

### Results of a run

Each run writes a `PayoutHistoryRecord` and fires [`getPayoutExecutedEvent()`](events.md#payouts-and-dividends) with the status, also when it fails. A successful run writes a `PAYOUT` (or, for dividend schedules, `DIVIDEND`) pair of ledger rows with the company id. The statuses are listed on [Events and signals](events.md#payouts-and-dividends).

## Paying a dividend

`IDividendPayer` pays one dividend right away, like **Pay Dividend** in the company screen.

```java
PayDividendResult result = api.getDividendPayer().payDividend(
        companyId,
        50L,                             // raw amount per share: 0.50
        false,                           // includeCompanyAccount, see below
        playerUuid,                      // who paid it, or null
        PayoutSchedule.MONEY_CURRENCY);  // 0 = money, or the short id of an item
if (result.success()) {
    long total = result.totalPaid();     // raw
    int holders = result.holderCount();
}
```

The rules:

- **Checked all or nothing.** If the company's free balance can't pay every holder in full, nobody gets anything and nothing changes. If a single transfer still fails after this check (rare), that holder is skipped and the others are paid. `totalPaid()` and `holderCount()` show what was really paid.
- **Only whole shares in bank accounts count**, free and locked, of every share item of the company. Each holder gets their number of whole shares × `amountPerShare`; a holder with less than one share gets nothing.
- **The company never pays itself.** Its own account is always left out; `includeCompanyAccount` has no effect.
- **Only the company's free balance pays.** Locked money doesn't count.
- **`actor` isn't checked.** It is written on the `DIVIDEND` ledger rows. If a player triggers the dividend in your mod, check their rights on the company yourself.

A successful dividend fires [`getDividendPaidEvent()`](events.md#payouts-and-dividends).

| `PayDividendResult.Reason` | Meaning |
|---|---|
| `OK` | Paid. |
| `NOT_MASTER` | Called on a slave. |
| `COMPANY_MISSING` | No company with this id. |
| `INVALID_INPUT` | `amountPerShare` is `0` or less, or the total is too large. |
| `NO_SHARES` | Nobody else holds shares in a bank account. |
| `INSUFFICIENT_FUNDS` | The free balance doesn't cover the total. For money also when the company account has no money bank. |
| `CURRENCY_ITEM_MISSING` | The company account has no bank for the item, or `currencyItem` is `Company.CURRENCY_UNSET` (no currency set). |
| `ACCOUNT_FROZEN` | The company account is frozen. |
| `SHARES_UNDER_REVIEW` | More shares are in bank accounts than the company stamped. Dividends stop until an admin acknowledges it, see [Share integrity](../../admin/banksystem/companies.md#share-integrity). |
| `INTERNAL` | Something else went wrong; see the server log. |
| `NO_PERMISSION` | Not returned by `payDividend`. |

## Share visuals on the client

Each company designs its share: a background and a foreground symbol, each with a colour (see [Designing the share](../../banksystem/shares.md#designing-the-share)). Two client interfaces let your mod show them.

### Reading the visuals

```java
ShareVisuals v = api.getVisualLookup().getShareVisuals(itemId);
if (v != null) {
    Component name = v.displayName();
    long issued = v.totalSharesIssued();
}
```

Call it on the client thread. It never blocks. It returns `null` when the item isn't a company share, or when the visuals haven't reached this client yet. In that case it asks the server and you get them on a later call, so ask again next frame. On a dedicated server it always returns `null`.

| `ShareVisuals` | Meaning |
|---|---|
| `bgSymbolId()`, `bgTint()` | Background symbol id and its ARGB colour. The id is empty when unset. |
| `fgSymbolId()`, `fgTint()` | Foreground symbol id and its ARGB colour. |
| `displayName()` | The company name; empty when unset. |
| `description()` | The company description; empty when unset. |
| `totalSharesIssued()` | Shares issued right now. |
| `maxSupply()` | The share limit set when the company was founded; `0` = no limit. |

### Drawing the icon

```java
IShareIconRenderer renderer = api.getShareIconRenderer();
if (renderer != null) renderer.renderInto(guiGraphics, x, y, 16, 16, itemId);
else guiGraphics.renderItem(stack, x, y); // fall back to the normal item icon
```

`renderInto(gfx, x, y, w, h, itemId)` draws the coloured share icon into any rectangle on the screen. Call it on the render thread. If the item isn't a company share, it draws nothing. If the visuals aren't there yet, it draws a placeholder until they arrive, so keep calling it every frame. `getShareIconRenderer()` returns `null` on a dedicated server, and when no renderer is ready yet.

## Related pages

- [Events and signals](events.md): payout and dividend events.
- [BankSystem API](api.md): accounts and banks of a company.
- [Payouts and dividends](../../banksystem/payouts.md): the same features for players.
- [Transaction ledger](transaction-ledger.md): the `PAYOUT` and `DIVIDEND` rows.
