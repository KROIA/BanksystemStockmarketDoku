---
title: "BankSystem API"
description: "Entry point, bank accounts, sync and async access, money formatting and payouts."
---

# BankSystem API

This page shows how another mod reads and changes BankSystem bank accounts. Everything starts at `BankSystemAPI`. All public types are in the package `net.kroia.banksystem.api` and its sub-packages. How to add BankSystem to your build is on [Setting up your project](../setup.md).

## The entry point

```java
BankSystemAPI api = BankSystemMod.getAPI();
```

| Method | Returns | What it gives you |
|---|---|---|
| `getModID()` / `getModVersion()` | `String` | BankSystem's mod id and the loaded version. |
| `getServerBankManager()` | `IBankManager` | Bank accounts on this server, sync and async. `null` before the server has started and after it has stopped, so check it. See [Sync or async](#sync-or-async). |
| `getClientBankManager()` | `IClientBankManager` | Bank data from the client side. See [On the client](#on-the-client). |
| `getEvents()` | `IBankSystemEvents` | Events and signals. See [Events and signals](events.md). |
| `getDataHandler()` | `IBankSystemDataHandler` | Saves and loads BankSystem's data (`saveAll`, `loadAll`, `save_bank`, `load_bank`, `save_globalSettings`, `load_globalSettings`; each returns `true` on success). Call it on the server thread. BankSystem saves on its own timer and on shutdown, so you rarely need it. |
| `isSlave()` | `boolean` | Whether this server is a slave on a network. |
| `getLedger()` | `ITransactionLedger` | Writes transaction ledger rows. Master only. See [Transaction ledger](transaction-ledger.md). |
| `getNoteFlowLog()` | `INoteFlowLog` | Records money items made or destroyed outside the bank. See [Note flow log](#note-flow-log). |
| `setItemPriceProvider(…)` / `getItemPriceProvider()` | `void` / `ItemPriceProvider` (nullable) | Item prices for total wealth. See [Item price provider](item-price-provider.md). |
| `setPriceCurrencyItem(short)` / `getPriceCurrencyItem()` | `void` / `short` | The item those prices are in. |
| `registerCurrencyProvider(…)` / `unregisterCurrencyProvider(String)` | `void` / `boolean` | Adds or removes a currency mod adapter. See [Currency integration](currency-integration.md). |
| `getCurrencyProviders()` / `getCurrencyProvider(String)` | `Collection<…>` / nullable | The registered currency adapters. Built-in adapters that the admin switched off are left out. |
| `getPayoutManager()` / `getDividendPayer()` | `IPayoutManager` / `IDividendPayer` | Company payouts and dividends. Master only. See [Companies, payouts and dividends API](companies-api.md). |
| `getVisualLookup()` / `getShareIconRenderer()` | `IBankSystemVisualLookup` / `IShareIconRenderer` (nullable) | Share visuals on the client. See [Companies, payouts and dividends API](companies-api.md#share-visuals-on-the-client). |

## How the data is organised

```text
Bank manager                      all accounts on the server
 └─ Bank account                  one account number, a name, an icon
     ├─ Users                     players with rights on the account
     └─ Banks                     one per item: money, diamonds, ...
         ├─ money    balance 1500, locked 200
         └─ diamond  balance 64,   locked 0
```

- A **bank account** has a unique account number. Every player gets a personal account. Players can create more accounts and share them with other players.
- Each user of an account has rights, stored as bit flags from `BankPermission`: `DEPOSIT` (1), `WITHDRAW` (2) and `MANAGE` (4).
- A **bank** holds the balance of one item in one account. You get the account first, then the bank for the item.
- Items are identified by `ItemID` (`net.kroia.banksystem.util`). `MoneyItem.getItemID()` gives the money item.

## Sync or async

`IBankManager` gives two ways in:

```java
IBankManager bankManager = api.getServerBankManager();

bankManager.hasSyncAccess();   // true on the master and on a single server
bankManager.hasAsyncAccess();  // true on the master, and on a slave while it is connected

IServerBankManager sync = bankManager.getSync();  // null on a slave
IAsyncBankManager async = bankManager.getAsync(); // always there
```

| | Sync (`getSync()`) | Async (`getAsync()`) |
|---|---|---|
| Works on | The master and single servers | The master and connected slaves |
| Returns | Values directly | `CompletableFuture<T>` |
| Use it when | Your code only runs on the master | Your code may run on a slave |
| Can fail | No, it returns a status | On a slave, yes. See [When an async call fails](#when-an-async-call-fails) |

**Use async unless you know you're on the master.** It works everywhere. On the master, async calls run locally and complete at once.

`getSync()` returns an `IServerBankManager`, which has both the sync and the async methods. Don't call either from the client side.

### Who may read what

Async reads of account data go to account members, BankSystem admins and server-internal calls (calls without a player sender). A request that comes through an untrusted slave only gets member data, because a slave could fake the sender. A refused read of account data completes with `null`, an empty list or a copy with names only. A refused balance read on a bank (`getBalanceAsync`, `getLockedBalanceAsync`, `getTotalBalanceAsync` and their `Real` variants) completes with `0` or `0.0`, so it looks like an empty bank. Other refused bank reads, such as formatted balances or JSON, complete with `null`. Clients can never change balances: deposits, withdrawals and transfers must come from server code on the master or a trusted slave.

### When an async call fails

On a slave, async calls go to the master, and the answer can get lost. BankSystem switches on request failures in ModUtilities for the whole game instance (`RequestManager.ENABLE_REQUEST_FAILURES = true`). This affects every mod's requests, not only BankSystem's: a request without an answer fails its future instead of waiting forever.

| What happened | What you get |
|---|---|
| The slave isn't connected to the master | The future completes at once with a fallback: `FAILED_NO_MASTER_CONNECTION` for `BankStatus` calls, otherwise `false`, `0`, `""`, an empty list or `null`. Nothing was sent. |
| The request couldn't be sent | Fails with `RequestNotSentException`. Nothing reached the master, so **refunding is safe**. |
| No answer in time, or the connection dropped | Fails with `RequestOutcomeUnknownException` (a `TimeoutException`). The master **may have applied** the call. Don't refund or retry blindly. |
| The master refused the request | Usually completes with `null`. Treat `null` as a failure. |

Both exceptions are in `net.kroia.modutilities.networking.client_server.arrs`. The timeout is 30 seconds (`RequestManager.DEFAULT_TIMEOUT_MS`). Slow reads, such as audit pages and balance history, wait 150 seconds.

**Deposits and withdrawals from a slave** (`deposit*Async`, `withdraw*Async`) carry a transfer id. If their answer is lost, the slave asks the master whether the call was applied:

- applied: completes with `SUCCESS`;
- not applied, or never sent: completes with `FAILED_NO_MASTER_CONNECTION`. This status always means nothing changed, so rolling back is safe;
- still unknown: fails with `RequestOutcomeUnknownException`. Don't refund.

The master applies each transfer id at most once. Transfers, locks, unlocks and set-balance calls don't get this check: when their answer is lost, they fail with `RequestOutcomeUnknownException`.

```java
// The player's items were already taken out of the world; put them in the bank.
bank.depositAsync(amount).whenComplete((status, ex) -> {
    if (ex != null) {
        Throwable cause = ex instanceof CompletionException && ex.getCause() != null ? ex.getCause() : ex;
        if (cause instanceof RequestNotSentException) giveItemsBack(); // never reached the master
        else log("deposit outcome unknown, items kept: " + cause);    // may have been applied
        return;
    }
    if (status != BankStatus.SUCCESS) giveItemsBack();                // any other status: nothing changed
});
```

## Getting an account and a bank

```java
IAsyncBankManager manager = api.getServerBankManager().getAsync();

manager.getBankAccountAsync(accountNumber).thenCompose(account -> {
    if (account == null)                       // no such account
        return CompletableFuture.completedFuture(null);
    return account.getBankAsync(itemID);       // null if the account has no bank for this item
}).thenAccept(bank -> {
    if (bank != null) { /* use the IAsyncBank */ }
});
```

Useful lookups on `IAsyncBankManager` (each has a sync twin without `Async` on `ISyncServerBankManager`):

| Method | Returns |
|---|---|
| `getBankAccountAsync(int accountNumber)` | The account, or `null` |
| `getPersonalBankAccountAsync(UUID)` / `(String name)` | A player's personal account, or `null` |
| `getOrCreatePersonalBankAccountAsync(UUID)` | The personal account, created if missing |
| `getBankAccountsAsync(UUID)` | Every account the player is a member of |
| `getPersonalBankAsync(UUID owner, ItemID)` / `getOrCreatePersonalBankAsync(…)` | One bank of the personal account |
| `bankAccountExistsAsync(int)` / `isAccountFrozenAsync(int)` | Whether the account exists, or is frozen |
| `isItemIDAllowedAsync(ItemID)` / `getAllowedItemsAsync()` | Which items may be banked |
| `getItemFractionScaleFactorAsync()` | Raw units per item, `100` |
| `isSlaveServerTrustedAsync(String slaveID)` | Whether a slave is trusted. See [Is this slave trusted?](#is-this-slave-trusted) |

## Working with a bank (`IAsyncBank`)

Every method returns a `CompletableFuture` and works the same on the master and on slaves.

### Raw and real amounts

Banks store amounts as `long` **raw** units. One item is 100 raw units, so money keeps two decimals: `150` raw is `1.50`. Methods with `Real` in the name take or return the `double` value instead.

```java
bank.depositAsync(150L);       // deposits 1.50
bank.depositRealAsync(1.50);   // the same
```

### Balances

| Method | Returns |
|---|---|
| `getBalanceAsync()` / `getRealBalanceAsync()` | The free balance |
| `getLockedBalanceAsync()` / `getRealLockedBalanceAsync()` | The locked balance |
| `getTotalBalanceAsync()` / `getRealTotalBalanceAsync()` | Free plus locked |
| `hasSufficientFundsAsync(long)` | Whether the free balance covers the amount |
| `getMinimalDataAsync()` | Item id, balance and locked balance in one `BankData` |
| `getItemIDAsync()` | The item (returned directly, not as a future) |

### Changing the balance

| Method | What it does |
|---|---|
| `depositAsync(long)` / `depositRealAsync(double)` | Adds to the free balance |
| `withdrawAsync(long)` / `withdrawRealAsync(double)` | Takes from the free balance |
| `withdrawLockedAsync(long)` / `withdrawLockedRealAsync(double)` | Takes from the locked balance only |
| `withdrawLockedPreferedAsync(long)` / `withdrawLockedPreferedRealAsync(double)` | Takes from the locked balance first, then the free one |
| `transferAsync(long, int toAccount)` / `transferRealAsync(…)` | Moves free balance to the same item's bank in another account |
| `transferFromLockedAsync(…)` / `transferFromLockedPreferedAsync(…)` | The same from the locked balance (with `Real` variants) |
| `setBalanceAsync(long)` / `setRealBalanceAsync(double)` | Sets the balance; returns `Boolean`. For admin tools. |

### Locking

Locking reserves an amount for something that isn't finished yet, for example an open market order. Locked money can't be spent twice.

```java
bank.lockAmountAsync(amount);              // 1. reserve it when the order is placed
bank.withdrawLockedPreferedAsync(amount);  // 2a. take it when the order fills
bank.unlockAmountAsync(amount);            // 2b. or release it when the order is cancelled
```

Use `withdrawLockedPreferedAsync` rather than `withdrawLockedAsync`: it still works when an admin released part of the locked amount in the meantime. `unlockAllAsync()` releases everything. Lock and unlock calls have `Real` variants too.

### Formatting

| Method | Returns |
|---|---|
| `getNormalizedBalanceAsync()` (also `…Locked…`, `…Total…`) | The balance with a short suffix: `1.5k`, `2M` |
| `getFormattedBalanceAsync()` (also `…Locked…`, `…Total…`) | The balance with thousands separators: `15'649'864` |
| `getNormalizedAmountAsync(…)` / `getFormattedAmountAsync(…)` | Any amount, raw (`long`) or real (`double`) |
| `convertToRawAmountAsync(double)` / `convertToRealAmountAsync(long)` | Converts between raw and real |
| `getItemNameAsync()` | The item's display name |
| `toJsonAsync()` / `toJsonStringAsync()` | The bank as JSON |

### Bank status

Every change returns a `BankStatus`. Anything other than `SUCCESS` means nothing changed.

| Value | Meaning |
|---|---|
| `SUCCESS` | Done. |
| `FAILED_NOT_ENOUGH_FUNDS` | The free or locked balance doesn't cover the amount. |
| `FAILED_OVERFLOW` | The new balance would overflow. |
| `FAILED_NEGATIVE_VALUE` | A negative amount was passed. |
| `FAILED_WRONG_INSTANCE_TYPE` | Internal: the target bank isn't a server bank. |
| `FAILED_INVALID_ITEM_ID` | The item id isn't valid. |
| `FAILED_NO_BANK` | The account has no bank for this item, for example the transfer target. |
| `FAILED_NO_MASTER_CONNECTION` | Slave only: the master wasn't reached, or it says the call wasn't applied. Nothing changed. |
| `FAILED_EXTERNAL_UNAVAILABLE` | The bank is bound to a currency mod that isn't available right now. |
| `FAILED_ACCOUNT_FROZEN` | The account is frozen and the call was a player action. |

## Working with an account (`IAsyncBankAccount`)

| Method | What it does |
|---|---|
| `getAccountNumberAsync()` | The account number (returned directly) |
| `getAccountNameAsync()` / `setAccountNameAsync(String)` | The account name |
| `getAccountIconAsync()` / `setAccountIconAsync(ItemID)` | The icon, or `null` |
| `getAccountDataAsync()` | A `BankAccountData` snapshot of the whole account |
| `addUserAsync(User, int permission)` / `removeUserAsync(UUID)` / `setUsersAsync(Map<User, Integer>)` | Members and their rights |
| `getPermissionAsync(UUID)` / `setPermissionAsync(UUID, int)` | A member's right flags |
| `hasPermissionAsync(UUID, BankPermission)` | Whether a member has one right |
| `getPersonalBankOwnerAsync()` | The owner of a personal account, or `null` |
| `getBankAsync(ItemID)` / `getOrCreateBankAsync(ItemID)` | One bank |
| `createBankAsync(ItemID, long startBalance)` | Creates a bank, or returns the existing one |
| `getAllBanksAsync()` | All banks as `Map<ItemID, IAsyncBank>` |
| `removeBankAsync(ItemID)` / `removeAllBanksAsync()` | Deletes banks. **The balance is lost.** |
| `removeEmptyBanksAsync()` | Deletes banks with a zero balance and returns their items |

### Watching an account (master)

```java
// ISyncServerBankAccount
void subscribeBankChanges(Consumer<BankAccountData> callback);
void unsubscribeBankChanges(Consumer<BankAccountData> callback);
// ISyncServerBankManager: the same by account number (does nothing if the account doesn't exist)
void subscribeBankChanges(int accountNr, Consumer<BankAccountData> callback);
void unsubscribeBankChanges(int accountNr, Consumer<BankAccountData> callback);
```

After the account changes, the callback gets a snapshot on the server thread, at most once per tick. Subscribing the same instance twice does nothing; unsubscribe with the same instance. Subscriptions aren't saved, so subscribe again after a restart.

### Frozen accounts

Admins can freeze an account. While it is frozen, the master refuses player actions on it (deposits, withdrawals, transfers, converter, upload and download blocks, crafting, share trades) with `FAILED_ACCOUNT_FROZEN`.

```java
// ISyncServerBankManager (master)
boolean isAccountFrozen(int accountNumber);
boolean setAccountFrozen(int accountNumber, boolean frozen, LedgerActor actor); // false = no such account
// IAsyncBankManager (master and slaves)
CompletableFuture<Boolean> isAccountFrozenAsync(int accountNumber);
```

A real change writes one `ACCOUNT_FREEZE` ledger row and fires [`getAccountFreezeChangedEvent()`](events.md#account-freezes). Setting the current state again does nothing.

!!! warning "Raw bank calls ignore the freeze"
    Plain `deposit`, `withdraw`, lock and unlock calls without a ledger type, and admin changes, still go through on a frozen account. If your mod moves a player's funds, check `isAccountFrozen(Async)` first.

### Removing a user

`removeUser(UUID)` (sync) and `removeUserAsync(UUID)` delete the user, their personal account and any account left without users. Company accounts are kept. The balances are handed to the player as items: on this server first, then on each slave. What can't be delivered is destroyed and logged as `ACCOUNT_DELETE_LOSS`; the rest is logged as `ACCOUNT_DELETE_PAYOUT`.

Both return before the delivery is known. `true` only means the user existed and was removed.

## On the client

`api.getClientBankManager()` reads bank data from the server the player is connected to. That server may pass the request on to the master. Account data goes to account members and BankSystem admins only: a refused read completes with `null` or an empty list, a refused change with `false`.

| Method | Returns |
|---|---|
| `getBankAccountDataAsync(int)` | One account, or `null` |
| `getPersonalBankAccountDataAsync(UUID)` | A player's personal account, or `null` |
| `getBankAccountsDataAsync(UUID)` | The player's accounts the viewer may read |
| `getBankManagerDataAsync()` | Users and accounts: full data for admins, names only for others |
| `getItemInfoDataAsync(ItemID)` | Server-wide totals and holders of one item |
| `allowItemIDAsync(ItemID)` / `disallowItemIDAsync(ItemID)` | Admins only. Disallowing clears every holder's balance of the item, without refund. |
| `deleteBankAccountAsync(int)` | Admins or members with `MANAGE` |
| `isServerTrustedAsync()` | `false` if this server is a slave the master doesn't trust |
| `requestUpdateBankAccount(…)` | Changes name, icon, members or rights (needs `MANAGE`); `null` if refused |
| `requestRemoveEmptyBanks(int)` | Removes empty banks and returns their items |
| `requestBalanceHistory(int[, long fromMs, long toMs, int maxPoints])` | Balance history; members and admins only |
| `requestAllowdItems()` | Every item that may be banked |
| `getUserCustomData()` / `updateUserCustomData(CompoundTag)` | The player's own UI settings, stored on the server |
| `getItemFractionScaleFactor()` / `convertToRawAmount(double)` / `convertToRealAmount(long)` | Conversions with the cached scale (ask once with `getItemFractionScaleFactorAsync()`) |

## Is this slave trusted?

The master refuses changes that come through an untrusted slave. To check from code:

- on a client: `getClientBankManager().isServerTrustedAsync()`;
- on a server: `getServerBankManager().getAsync().isSlaveServerTrustedAsync("")`. The empty id asks about the server the request comes through: `true` on the master and on a single server, the master's answer on a slave. A non-empty id asks about that slave.

A slave that isn't connected answers `false` at once. To react to trust changes, use [`getTrustChangedSignal()`](events.md#trust-changes). Admins manage trust as described in [Master and slave servers](../../admin/multi-server.md#trusted-slaves).

## Money formatting

`MoneyFormat` formats money the same way BankSystem's placeholders do, so your mod shows money in the same style. All methods are static and thread-safe.

| Method | Returns |
|---|---|
| `formatMoney(long raw)` | With the server's money format (default `$%s`): `123456` → `"$1'234.56"` |
| `formatMoney(long raw, String pattern)` | With your own pattern; `%s` is the number. Without `%s`, just the number. |
| `formatMoneyRaw(long raw)` | Plain number: `123456` → `"1234.56"` |
| `getPattern()` | The current pattern |

The number always uses `'` as thousands separator and two decimals, rounded down. A negative amount gets its minus inside the pattern: `"$-1'234.56"`. BankSystem sets the pattern when the server starts; on a client connected to a remote server, `formatMoney(long)` uses the default `$%s`. Don't call `setPattern` yourself.

```java
long raw = 123456;                                   // 1234.56
String shown = MoneyFormat.formatMoney(raw);         // "$1'234.56"
String euro  = MoneyFormat.formatMoney(raw, "%s €"); // "1'234.56 €"
String plain = MoneyFormat.formatMoneyRaw(raw);      // "1234.56"
```

## Note flow log

`api.getNoteFlowLog()` records money items that are made or destroyed outside the bank, for example money a villager pays out. Rows go to this server's own diagnostics database, so it works on every server, slaves included. It never blocks and never throws; it does nothing when the diagnostics database is off.

```java
INoteFlowLog flow = api.getNoteFlowLog();
// call on the server thread
flow.record("mymod:villager_pay", player.getUUID(), moneyItemId, +count, villager, "trade #12");
flow.record("mymod:burn", player.getUUID(), moneyItemId, -count, null); // without a villager
```

| Parameter | Meaning |
|---|---|
| `source` | What happened, with your mod id: `mymod:villager_pay` |
| `player` | The player involved, or `null` |
| `item` | The money `ItemID` |
| `amount` | Signed **item count**: positive = made, negative = destroyed |
| `villager` | The trading villager, or `null`. BankSystem stores its UUID, dimension and position. |
| `context` | Any other text, or `null` |

BankSystem writes these sources itself: `banksystem:converter_in` and `banksystem:converter_out` (notes into or out of the converter), `banksystem:give` (`/give` of a money item) and `banksystem:creative_create` / `banksystem:creative_destroy` (notes taken from or deleted in the creative inventory).

## Related pages

- [Events and signals](events.md): react to account, network and ledger changes.
- [Transaction ledger](transaction-ledger.md): write your own ledger rows.
- [Companies, payouts and dividends API](companies-api.md): payouts, dividends and share visuals.
- [Developers](../index.md): which API to use for which job.
