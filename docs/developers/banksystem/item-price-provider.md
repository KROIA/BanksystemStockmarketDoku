---
title: "Item price provider"
description: "Supplying item prices for total-wealth tracking."
---

# Item price provider

BankSystem records the balance history of every bank account. If a mod tells it what items are worth, BankSystem also records each account's **total wealth**: money plus the value of all items, locked ones included. Players see it as the gold **Total Wealth** line in the [balance history](../../banksystem/bank-terminal.md#balance-history). StockMarket supplies these prices from its markets.

Without prices, there is no wealth line. Nothing else changes.

## The API

All four methods are on `BankSystemAPI`:

| Method | What it does |
|---|---|
| `setItemPriceProvider(ItemPriceProvider)` | Sets the price lookup. `null` removes it. |
| `setPriceCurrencyItem(short)` | Sets the item the prices are in, as its short id. |
| `getItemPriceProvider()` | The current lookup, or `null`. |
| `getPriceCurrencyItem()` | The current currency item, or `0`. |

There is only one provider. Setting a new one replaces the old one.

```java
@FunctionalInterface
public interface ItemPriceProvider {
    long getItemPrice(short itemId);
}
```

`getItemPrice` gets the short id of an item and returns the price of **one item** in raw money units (100 = 1.00), or `0` if the item has no price. Iron worth 2.50 returns `250`. BankSystem calls it on the master only, on the server thread, once per account and item at each snapshot, so keep it fast and don't block. On a slave, setting a provider has no effect.

## Registering

```java
BankSystemAPI api = BankSystemMod.getAPI();
api.getEvents().getBanksystemSetupCompleteSignal().addListener(() -> {
    api.setItemPriceProvider(itemId -> {
        Market market = findMarket(itemId);       // your lookup by BankSystem short id
        return market == null ? 0 : market.getPriceRaw();
    });
    api.setPriceCurrencyItem(MoneyItem.getItemID().getShort());
});
```

Register after BankSystem finished setting up, for example in `getBanksystemSetupCompleteSignal()`. **You must set both the provider and the currency item.** Without a currency item (`0`), BankSystem records no wealth.

To stop, call `api.setItemPriceProvider(null)`.

## How wealth is worked out

At each balance snapshot, for every account:

```text
for each bank in the account:
    total = free balance + locked balance
    if the item is money, or the currency item:
        wealth = wealth + total                                    (face value)
    else if price > 0:
        wealth = wealth + total × price / raw units per item
```

- **Money items always count as cash** at face value, whatever currency item you set.
- **Raw units per item** is `100` for a normal bank. For a slot bound to a [currency mod](currency-integration.md), it is the value of one coin of that mod in raw units.
- Items with price `0` add nothing.

How often snapshots are taken is set by **Balance snapshot interval (minutes)** in the [Mod Settings](../../admin/banksystem/settings.md#utilities), 1 minute by default. A row is only written when the value changed, or when the **Balance snapshot heartbeat (minutes)** has passed. The wealth rows are stored with the item id `32767` (`BalanceHistoryRecord.WEALTH_ITEM_ID`).

!!! note "Your prices feed a suspicion check"
    The wealth line is also used for the `WEALTH_JUMP` flag: when an account's wealth grows a lot in a short time, admins get an alert. A sudden price jump in your mod can raise it. Without a provider, this flag never fires. See [Transaction ledger](transaction-ledger.md#suspicion-flags).

## Item ids

BankSystem gives each item a `short` id. To match your own items to it:

```java
// From an ItemStack (master only; registers the item if it's new)
short id = ItemID.getOrRegisterFromItemStackServerSide_direct(stack).getShort();

// From a known short id
ItemStack stack = new ItemID(id).getStack(); // a copy, or ItemStack.EMPTY if unknown; never null
```

`ItemID` is in `net.kroia.banksystem.util`.

## Related pages

- [BankSystem API](api.md): raw amounts and the entry point.
- [Events and signals](events.md): the setup signal used above.
- [How the two mods work together](../../together.md#your-total-wealth-uses-market-prices): what players see.
