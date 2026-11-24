---
title: "Currency integration"
description: "Writing an ExternalCurrencyProvider so your currency mod shows up in Currency Bindings."
---

# Currency integration

This page is for authors of currency mods. With an adapter, players can bind a BankSystem bank slot to an account in your mod (see [Currency bindings](../../banksystem/currency-bindings.md)). After that, deposits, withdrawals and stock market trades on that slot move money in your mod's account. BankSystem ships adapters for Numismatics and Lightman's Currency; this page shows how to write your own.

All types are in `net.kroia.banksystem.api.currency`.

## How a binding works

- **Your mod holds the balance.** Balance reads, deposits and withdrawals on the bound slot go to your account.
- **BankSystem keeps the rest:** account members, rights and the **locked** balance (money reserved for open orders). Locking and unlocking never reach your mod; spending a locked amount withdraws it from your account.
- **Binding moves the money once.** The slot's free balance moves into your account when the player binds it. The locked part stays in BankSystem.
- **One slot, one account.** Each bank slot can be bound on its own. Other slots of the same account stay normal.

Write an adapter if your mod keeps balances in accounts that survive logouts and restarts. If your currency is only coins in inventories, you don't need one: players can bank the coins like any other item.

## The four types

| Type | What it is |
|---|---|
| `ExternalCurrencyProvider` | Your mod's entry point. One instance, registered once. Lists a player's bindable accounts and opens an account from a saved reference. |
| `ExternalAccount` | A short-lived handle to one account. BankSystem opens one when it needs it and doesn't keep it. |
| `ExternalAccountRef` | The saved pointer to an account: `providerId`, `accountKey`, `label`, `shared`. |
| `ProviderFeature` | Flags for what your provider supports. |

`ExternalAccountRef` is a record. `providerId` and `accountKey` must not be empty, and no field may be `null`; otherwise the constructor throws. `providerId` + `accountKey` identify the account for good. `label` is the name shown in the account picker, and `shared` says whether several players own the account in your mod. BankSystem saves and sends the reference itself; you only create and read it.

## Rules for every adapter

- **Server thread only.** BankSystem calls every method on the server thread. Your adapter doesn't need to be thread-safe. Don't change adapter state from your own background threads.
- **Amounts are BankSystem raw units** (`long`). Convert to your mod's units inside the adapter. See [Units](#units).
- **Read live, don't cache.** `getBalance()` is called for every read. Your mod's own machines and commands change balances behind BankSystem's back, and BankSystem relies on a live value to keep its locked balance correct. If a lookup in your mod is slow, cache inside your mod and update that cache on every change.
- **Don't throw for expected failures.** `deposit` and `withdraw` return `false` with no change when the money doesn't fit, isn't there, or your mod refuses for its own reasons.

## Writing a provider

### Name and features

```java
public final class MyMoneyProvider implements ExternalCurrencyProvider {
    public static final String PROVIDER_ID = "my_money";

    @Override public @NotNull String providerId() { return PROVIDER_ID; }

    @Override public boolean isAvailable() {
        return Platform.isModLoaded("my_money") && MyMoneyApi.isReady(); // cheap, no file or network access
    }

    @Override public @NotNull Set<ProviderFeature> features() {
        return EnumSet.of(ProviderFeature.PERSONAL_ACCOUNTS, ProviderFeature.SUFFICIENT_FUNDS_CHECK);
    }
    // listBindableAccounts and open follow below
}
```

`providerId()` is saved with every binding. **Never change it after a release**, or every existing binding loses its account. Use your mod id.

`isAvailable()` is checked before the binding screen lists your provider and before every balance operation on a bound slot. Keep it cheap.

### Listing a player's accounts

```java
@Override
public @NotNull List<ExternalAccountRef> listBindableAccounts(@NotNull UUID player) {
    List<ExternalAccountRef> out = new ArrayList<>();
    MyAccount personal = MyMoneyApi.getPersonalAccount(player);
    if (personal != null)
        out.add(new ExternalAccountRef(PROVIDER_ID, personal.uuid().toString(), personal.displayName(), false));
    for (MyAccount team : MyMoneyApi.getSharedAccountsForPlayer(player))
        out.add(new ExternalAccountRef(PROVIDER_ID, team.uuid().toString(), team.displayName(), true));
    return out; // personal first, then shared
}
```

BankSystem calls it when a player opens the account picker, and checks the chosen account against it when the player binds (BankSystem admins skip that check). Return live results.

**An empty list is an answer**: the player may bind none of your accounts. BankSystem also calls this method at server start for the managers of every bank account that has a binding. If none of them may bind the bound account any more, the binding is **suspended** and admins get an alert. An admin lifts it with `/banksystem restorebinding`. So:

- Return an empty list only when the player really may bind nothing.
- When you can't give the complete list (your mod isn't ready, an error, only part could be read), **throw** a `RuntimeException`. The bind is then refused, the picker shows nothing, and the start-up check leaves existing bindings alone.

### Opening an account

```java
@Override
public @Nullable ExternalAccount open(@NotNull ExternalAccountRef ref) {
    if (!PROVIDER_ID.equals(ref.providerId())) return null;
    try {
        MyAccount account = MyMoneyApi.getAccount(UUID.fromString(ref.accountKey()));
        return account == null ? null : new MyExternalAccount(ref, account);
    } catch (IllegalArgumentException e) {
        return null; // not a key of ours
    }
}
```

Return `null` when the account can't be reached right now: deleted, not ready, or a key you don't recognise. BankSystem then treats the binding as unavailable (see [When your mod is missing](#when-your-mod-is-missing)).

### The account handle

```java
final class MyExternalAccount implements ExternalAccount {
    private final ExternalAccountRef ref;
    private final MyAccount account;

    MyExternalAccount(ExternalAccountRef ref, MyAccount account) { this.ref = ref; this.account = account; }

    @Override public @NotNull ExternalAccountRef ref() { return ref; }
    @Override public long getBalance() { return account.getBalance(); }          // live, >= 0
    @Override public boolean deposit(long amount) {                              // false on overflow, no change
        return amount >= 0 && account.tryDeposit(amount);
    }
    @Override public boolean withdraw(long amount) {                             // false if not enough, no change
        return amount >= 0 && account.tryWithdraw(amount);
    }
    @Override public boolean canWithdraw(long amount) { return amount >= 0 && account.getBalance() >= amount; }
    @Override public boolean isSharedAccount() { return ref.shared(); }
    @Override public @NotNull Set<UUID> currentMembers() { return new HashSet<>(account.members()); } // a copy
    @Override public void syncMembership(@NotNull Set<UUID> withdrawers) { account.setMembers(withdrawers); }
}
```

Every method goes straight to your mod. `deposit` and `withdraw` must be all-or-nothing.

### Units

BankSystem stores 100 raw units per item, so money has two decimals. Three methods tell BankSystem how your units fit:

| Method | Default | Meaning |
|---|---|---|
| `ExternalAccount.nativeScale()` | `1` | Raw units per smallest unit of your mod. If your mod only stores whole coins and one coin is 100 raw units, return `100`. BankSystem then only sends whole multiples of it to `deposit` and `withdraw`, and keeps the remainder in the binding itself, so no fraction is lost. |
| `ExternalCurrencyProvider.getBaseCurrencyItemId()` | `null` | The item id of your base coin, for example `"my_money:coin"`. Only a slot of this item can be bound to your mod. `null` allows any item. |
| `ExternalCurrencyProvider.baseUnitsPerItem(ItemStack)` | `0` | The value of one coin in raw units, for every coin of your mod. When a player pays in a coin with a non-zero value at a Bank Terminal, BankSystem credits count × value to the bound base-coin slot instead of a separate bank for that coin. For the base coin, this value also sets how many raw units one coin of the bound slot is worth; `0` means 100. |

In `baseUnitsPerItem`, read the coin values from your mod's configuration if it has one; don't hard-code them. Return `0` for damaged or enchanted stacks and for items that aren't your coins.

### Registering

```java
// when your mod starts
if (Platform.isModLoaded("banksystem")) {
    BankSystemMod.getAPI().registerCurrencyProvider(new MyMoneyProvider());
}
```

Registering the same `providerId` again replaces the earlier provider. `unregisterCurrencyProvider(providerId)` removes it again; a normal adapter stays registered for the whole game session. To avoid a hard dependency on BankSystem, put this call in a class that is only loaded when BankSystem is present.

## Feature flags

Return only the flags your provider really supports.

| Flag | Meaning |
|---|---|
| `PERSONAL_ACCOUNTS` | Each player has (or can create) a personal account. |
| `MULTI_ACCOUNT_PER_PLAYER` | `listBindableAccounts` can return more than one account per player. |
| `SHARED_ACCOUNTS` | Your mod has accounts with several owners. |
| `MEMBERSHIP_SYNC` | Your `syncMembership` really changes the members in your mod. |
| `SUFFICIENT_FUNDS_CHECK` | Your `canWithdraw` is exact and has no side effects. |

The flags are sent to the Currency Bindings screen. In this version BankSystem doesn't change its behaviour because of them, and it doesn't call `canWithdraw`, `isSharedAccount`, `currentMembers` or `syncMembership`. Implement them as described anyway:

- `canWithdraw(amount)`: whether a `withdraw(amount)` right after would succeed.
- `isSharedAccount()`: the same as `ref().shared()`.
- `currentMembers()`: a copy of the players who may spend from the account; for a personal account, the owner.
- `syncMembership(withdrawers)`: replaces the members who may spend with the given set: the users of the shared bank account with the withdraw right. Don't throw; log and return on errors.

## Personal and shared accounts

A binding only connects accounts of the same kind:

| Bank account | `ref.shared()` | Result |
|---|---|---|
| Personal | `false` | Allowed |
| Shared (any account that isn't personal) | `true` | Allowed |
| Personal | `true` | Refused with `FAILED_WRONG_INSTANCE_TYPE` |
| Shared | `false` | Refused with `FAILED_WRONG_INSTANCE_TYPE` |

So set `shared` correctly in every reference you return.

## What callers see

Other mods use the bound slot through the normal [BankSystem API](api.md). Your return values become a `BankStatus`:

| Your adapter | `BankStatus` |
|---|---|
| `deposit` returns `false` | `FAILED_OVERFLOW` |
| `withdraw` returns `false` | `FAILED_NOT_ENOUGH_FUNDS` |
| `open` returns `null`, or `isAvailable()` is `false` | `FAILED_EXTERNAL_UNAVAILABLE` |

## When your mod is missing

When your mod is removed, not ready, or an admin switched off a built-in adapter in the server's Integrations settings:

- Reads of the bound slot's free balance return `0`. The locked balance in BankSystem stays visible.
- Changes fail with `FAILED_EXTERNAL_UNAVAILABLE`; nothing changes on either side.
- BankSystem logs one warning per bound slot, not one per call.
- Unbinding is refused while the slot still holds locked money or a remainder below one of your units, because it would be lost.

When your mod is back, the bindings work again, as long as `providerId()` and each `accountKey` still lead to the same account.

## Keeping bindings working

- **Keep `providerId()` the same** in every release.
- **Keep each `accountKey` the same** for the life of the account. If you change its format, recognise the old format in `open` and translate it. A version prefix in the key, for example `v1:<uuid>`, makes that easier.
- **Bindings don't move between worlds.** If the same account has a different key on another server, players bind again there.
- **The Currency Bindings screen doesn't update by itself.** After a change in your mod's own machines, players click **Refresh**. Server-side reads are always live.

## On a network

Bindings exist only on the master, and only the master calls your adapter. A slave forwards every bank call to the master, including the binding screen. Your adapter needs no network code: treat every call as a call on one server. Install your mod on the master.

## Related pages

- [Currency bindings](../../banksystem/currency-bindings.md): what players see.
- [BankSystem API](api.md): `BankStatus` and the bank calls that reach your adapter.
- [Transaction ledger](transaction-ledger.md): the `EXTERNAL_BIND` and `EXTERNAL_UNBIND` rows.
- [Master and slave servers](../../admin/multi-server.md): where your mod must be installed.
