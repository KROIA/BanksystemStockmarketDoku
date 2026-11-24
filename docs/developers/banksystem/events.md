---
title: "Events and signals"
description: "Every event a dependent mod can subscribe to, with threading rules."
---

# Events and signals

BankSystem tells other mods when something changes: users and accounts, items, the network connection, slave trust, payouts, freezes, ledger rows and suspicion flags. Subscribe instead of polling.

```java
IBankSystemEvents events = BankSystemMod.getAPI().getEvents();
```

`getEvents()` returns the same object for the whole game session, across worlds. BankSystem never clears its listeners: a listener you add stays registered when a player leaves a singleplayer world and opens another one. Add your listeners once, when your mod starts, not each time a world loads.

## Two kinds of events

BankSystem uses two types from ModUtilities (`net.kroia.modutilities.event`):

| Type | Payload | Subscribe with |
|---|---|---|
| `Signal` | none | `addListener(Runnable)` |
| `DataEvent<T>` | one value of type `T` | `addListener(Consumer<T>)` |

Both also take `addListener(listener, maxCalls)`: the listener removes itself after `maxCalls` calls (`-1` = no limit). `removeListener(listener)` removes it earlier and returns `true` if it was registered.

```java
// Signal: no payload
events.getBanksystemSetupCompleteSignal().addListener(() -> loadMyData());

// DataEvent: one value
events.getTrustChangedSignal().addListener(info -> onTrust(info.slaveID(), info.trusted()));

// Only the next call, then the listener removes itself
events.getBanksystemSetupCompleteSignal().addListener(this::onReady, 1);
```

A listener may add or remove listeners while it runs. The change counts from the next call on.

To remove a listener, keep the exact instance you added, for example in a field. A new lambda with the same body is a different instance. `events.removeListeners()` clears every listener of every event, other mods' listeners included, so don't call it.

## Threads

Each event fires on one side (master, slave or both) and on one thread:

- **Server thread.** Most events. You may touch game state directly.
- **Network thread.** The four connection events fire on a network thread. Don't block in the listener, and don't touch game state there: pass the work to the server thread first, for example with `server.execute(() -> …)`.
- **Writer's thread.** Ledger rows and suspicion flags fire on whichever thread wrote the row: the server thread, a request handler thread (calls forwarded from a slave) or the database thread (periodic checks). Keep these listeners fast and thread-safe, and pass game-state work to the server thread.
- **Caller's thread.** `getAccountFreezeChangedEvent()` fires on the thread that froze or unfroze the account. Pass game-state work to the server thread.

When in doubt, pass the work to the server thread.

## All events

| Getter | Type | Side | Thread | Fires when |
|---|---|---|---|---|
| `getUserAddedEvent()` | `DataEvent<User>` | master | server | A user is added to the bank manager. |
| `getUserRemovedEvent()` | `DataEvent<User>` | master | server | A user is removed. |
| `getBankAccountCreatedEvent()` | `DataEvent<ISyncServerBankAccount>` | master | server | A bank account is created. |
| `getBankAccountDeletedEvent()` | `DataEvent<ISyncServerBankAccount>` | master | server | A bank account is deleted. |
| `getItemIDsMergedEvent()` | `DataEvent<Map<ItemID, ItemID>>` | master | server | Item ids were merged. See [Merged and removed items](#merged-and-removed-items). |
| `getItemIDsRemovedEvent()` | `DataEvent<Set<ItemID>>` | master | server | An admin removed the items of missing mods. |
| `getBankDataSavedToFileSignal()` | `Signal` | master | server | Bank data was saved. |
| `getBankDataLoadedFromFileSignal()` | `Signal` | both | server | Bank data was loaded. |
| `getSettingsSavedToFileSignal()` | `Signal` | both | server | Settings were saved. |
| `getSettingsLoadedFromFileSignal()` | `Signal` | both | server | Settings were loaded. |
| `getBanksystemSetupCompleteSignal()` | `Signal` | both | server | BankSystem finished setting up the world. |
| `getMasterServerSlaveConnected()` | `Signal` | master | network | A slave finished connecting. |
| `getMasterServerSlaveDisconnected()` | `DataEvent<String>` | master | network | A slave disconnected; the payload is its slave id. |
| `getSlaveConnectionAcceptedSignal()` | `Signal` | slave | network | This slave connected to its master. |
| `getSlaveConnectionLostSignal()` | `Signal` | slave | network | This slave lost its master. |
| `getTrustChangedSignal()` | `DataEvent<TrustChangeInfo>` | master | server | A slave was trusted or untrusted. |
| `getPayoutExecutedEvent()` | `DataEvent<PayoutExecutedInfo>` | master | server | A payout schedule ran, paid or failed. |
| `getDividendPaidEvent()` | `DataEvent<DividendPaidEvent>` | master | server | `payDividend` paid a dividend. |
| `getAccountFreezeChangedEvent()` | `DataEvent<AccountFreezeChangedEvent>` | master | caller's | An account was frozen or unfrozen. |
| `getTransactionLoggedEvent()` | `DataEvent<TransactionLoggedEvent>` | master | writer's | A ledger row was written. |
| `getSuspicionFlaggedEvent()` | `DataEvent<SuspicionFlaggedEvent>` | master | writer's | A suspicion flag was raised. |

## When to subscribe

1. Subscribe when your mod starts.
2. Load anything that needs BankSystem's world data in `getBanksystemSetupCompleteSignal()`.
3. On a slave, wait for `getSlaveConnectionAcceptedSignal()` before you ask the master anything. Until then, async calls answer at once with their fallback value (see [BankSystem API](api.md#when-an-async-call-fails)).

## Master and slave connections

Two events fire on the master and describe slaves; two fire on a slave and describe its own link to the master. Pick them by where your code runs.

```text
        master                               slave
  getMasterServerSlaveConnected     <-->   getSlaveConnectionAcceptedSignal
  getMasterServerSlaveDisconnected  <-->   getSlaveConnectionLostSignal
          (payload: slave id)
```

- **`getSlaveConnectionAcceptedSignal()`** fires on the slave once the connection to the master is ready for async calls. It fires again after every reconnect. Use it to build caches that come from the master.
- **`getSlaveConnectionLostSignal()`** fires on the slave once when a working connection drops, also on a clean shutdown. It doesn't fire again for each failed reconnect attempt, only after the next successful connection. Use it to drop those caches.
- **`getMasterServerSlaveConnected()`** fires on the master after a slave finished connecting. It has no payload.
- **`getMasterServerSlaveDisconnected()`** fires on the master when a slave disconnects. The payload is the slave id, so you can drop what you kept for that slave.

All four fire on a network thread. See [Threads](#threads).

## Trust changes

`getTrustChangedSignal()` fires on the master when an admin trusts or untrusts a slave. The payload `TrustChangeInfo(String slaveID, boolean trusted)` holds the new state, so you can pass it on without asking again.

```java
events.getTrustChangedSignal().addListener(info -> {
    // info.slaveID(): the slave; info.trusted(): true if it is trusted now
    sendTrustStateToSlave(info.slaveID(), info.trusted());
});
```

It never fires on a slave. A slave doesn't learn which other slaves the master trusts. If your mod needs the trust state on a slave, send it from the master yourself, or ask with [`isSlaveServerTrustedAsync`](api.md#is-this-slave-trusted).

## Merged and removed items

**`getItemIDsMergedEvent()`** fires on the master after BankSystem merged item ids that turned out to be the same item and moved its own data (balances, locked balances, allowed items, account icons) to the remaining id. The payload maps each old id to the id it was merged into. Move your own data keyed by item id (markets, orders, price history) the same way.

**`getItemIDsRemovedEvent()`** fires on the master after an admin agreed to remove the items of mods that are no longer installed. BankSystem has already removed their balances. The event fires once per server start, right after `getBanksystemSetupCompleteSignal()`, and not at all when nothing was removed. The payload is the set of removed ids. Delete your own data keyed by them:

```java
events.getItemIDsRemovedEvent().addListener(removed -> {
    for (ItemID id : removed) myMarkets.remove(id);
});
```

Both payloads can't be changed.

## Payouts and dividends

Both fire on the master only, on the server thread.

**`getPayoutExecutedEvent()`** fires each time a payout schedule runs, dividend schedules included, **also when it fails**. A paused schedule doesn't run and fires nothing. Use it for badges, statistics or warnings to the company's managers.

| Field of `PayoutExecutedInfo` | Meaning |
|---|---|
| `companyId` | The company |
| `scheduleId` | The schedule |
| `sourceAccount` | The company's bank account |
| `targetUuid` | The target player; may be `null` for a dividend schedule |
| `amount` | Raw amount in the schedule's currency (100 = 1.00) |
| `status` | The result, see below |
| `time` | Time in epoch milliseconds |

| `status` | Meaning |
|---|---|
| `OK` | Paid. |
| `INSUFFICIENT_FUNDS` | A money schedule: the company account's free balance couldn't cover the amount. |
| `TARGET_MISSING` | The target player or account no longer exists. For a dividend schedule: nobody holds shares. |
| `TARGET_NO_DEPOSIT_RIGHT` | The target player has no deposit right on the chosen target account. |
| `CURRENCY_ITEM_MISSING` | An item schedule: the company account has no bank for the item or not enough of it, or the schedule has no item set. |
| `PAUSED` | A dividend schedule was held back: the company's share check found more shares in bank accounts than were stamped, and no admin has acknowledged it yet. |
| `ACCOUNT_FROZEN` | The company account is frozen. |
| `UNKNOWN` | Any other failure. |

`status` is a `PayoutHistoryRecord.Status` from `net.kroia.banksystem.data.table.record`, outside the API package. Compare by name; new values may be added.

**`getDividendPaidEvent()`** fires once each time [`payDividend`](companies-api.md#paying-a-dividend) paid a dividend: called by a mod, or by **Pay Dividend** in the company screen. A refused dividend doesn't fire it. `totalPaid` and `holderCount` say what was really paid: only whole shares count, and in rare cases a single transfer fails after the funds check, so that holder is skipped. Dividend schedules report through `getPayoutExecutedEvent()` instead.

| Field of `DividendPaidEvent` | Meaning |
|---|---|
| `companyId` | The company |
| `perShareAmount` | Raw amount per share |
| `totalPaid` | Raw total paid |
| `holderCount` | Number of accounts paid |
| `time` | Time in epoch milliseconds |

## Account freezes

`getAccountFreezeChangedEvent()` fires on the master once for each real change, on the thread that froze or unfroze the account. Setting the same state again doesn't fire it.

| Field of `AccountFreezeChangedEvent` | Meaning |
|---|---|
| `accountNumber` | The account |
| `frozen` | `true` = now frozen |
| `actor` | The `LedgerActor` who changed it |

How freezing works is on [BankSystem API](api.md#frozen-accounts).

## Ledger rows

`getTransactionLoggedEvent()` fires on the master once per [transaction ledger](transaction-ledger.md) row, right after the row was queued for saving and before the audit and suspicion checks run on it. Rows written by other mods fire it too. It fires on the writer's thread. If your listener throws, BankSystem logs a warning and the row is still written.

Rows are only written while BankSystem runs on the master, from server start to server stop. A change outside that time writes no row, so this event doesn't fire. Suspicion flags are raised from these rows, so none are raised either.

| Field of `TransactionLoggedEvent` | Meaning |
|---|---|
| `accountNumber` | The account the row belongs to |
| `type` | The `LedgerType` |
| `itemId` | Short id of the item; `0` for rows without an item (freeze, account edit) |
| `amount` | Raw amount; `0` if none. Signed for some types, for example transfers: `-x` on the sender, `+x` on the receiver. See [Type codes](transaction-ledger.md#type-codes). |
| `actor` | The `LedgerActor` who caused it |
| `otherAccount` | The other account of a transfer or payout, or `null` |
| `companyId` | The company of a payout, dividend or share row, or `null` |
| `timeMs` | Time in epoch milliseconds |
| `note` | Free text, or `null` |

```java
events.getTransactionLoggedEvent().addListener(row -> {
    if (row.type() == LedgerType.TRANSFER && row.amount() > 0)
        server.execute(() -> notifyReceiver(row.accountNumber(), row.amount())); // to the server thread
});
```

## Suspicion flags

`getSuspicionFlaggedEvent()` fires on the master once per flag, after the flag was saved and the admins were alerted. It fires on the thread that raised the flag.

| Field of `SuspicionFlaggedEvent` | Meaning |
|---|---|
| `accountNumber` | The flagged account; `0` for flags about the whole server |
| `flagType` | The flag code, see [Transaction ledger](transaction-ledger.md#suspicion-flags) |
| `flagName` | The code's name, for example `WEALTH_JUMP`, or `FLAG_<code>` for an unknown code |
| `severity` | Higher is worse |
| `amount` | Raw amount that raised the flag; `0` if none |
| `ref` | A reference such as a transfer id, or `null` |
| `details` | The reason as text, or `null` |
| `timeMs` | Time in epoch milliseconds |

## Related pages

- [BankSystem API](api.md): accounts, banks and the async calls.
- [Transaction ledger](transaction-ledger.md): the rows behind `getTransactionLoggedEvent()`.
- [Companies, payouts and dividends API](companies-api.md): schedules and dividends.
- [Master and slave servers](../../admin/multi-server.md): how the network is set up.
