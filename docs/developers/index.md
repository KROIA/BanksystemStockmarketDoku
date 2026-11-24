---
title: "Developers"
description: "Which API to use for which job, a first call for each mod, and the threading rules."
---

# Developers

These pages are for mod authors who want to use BankSystem or StockMarket from their own mod: read balances, pay players, open markets or write a plugin that moves prices. Both mods are Architectury mods for Fabric and NeoForge, and their APIs live in the common module.

Start with [Setting up your project](setup.md) to add the mods to your Gradle build.

## Which API for which job

| You want to | Use | Page |
|---|---|---|
| Read or change bank balances, create accounts, transfer money | `BankSystemMod.getAPI()` → `getServerBankManager()` | [BankSystem API](banksystem/api.md) |
| React to new accounts, logged transactions, payouts or slave connections | `BankSystemMod.getAPI().getEvents()` | [Events and signals](banksystem/events.md) |
| Write your own rows into the transaction history | `BankSystemMod.getAPI().getLedger()` | [Transaction ledger](banksystem/transaction-ledger.md) |
| Make your currency mod show up in **Currency Bindings** | `ExternalCurrencyProvider` | [Currency integration](banksystem/currency-integration.md) |
| Give items a price for the total-wealth ranking | `ItemPriceProvider` | [Item price provider](banksystem/item-price-provider.md) |
| Schedule company payouts or pay dividends | `getPayoutManager()`, `getDividendPayer()` | [Companies, payouts and dividends API](banksystem/companies-api.md) |
| Create, close or pause a market | `StockMarketMod.getAPI().getIntegration()` | [Market integration API](stockmarket/market-creation-api.md) |
| Open the trade screen or show a price chart in your own screen | `StockMarketClientIntegration` | [Market integration API](stockmarket/market-creation-api.md) |
| Read markets, prices and orders on the client | The StockMarket client managers | [Market access API](stockmarket/market-access-api.md) |
| Move prices, place bot orders or shape the order book | A StockMarket plugin | [Plugin system overview](stockmarket/plugins/index.md) |

## A first call to each mod

**BankSystem:** read a player's money balance. This works on every server, also on a slave:

```java
BankSystemAPI api = BankSystemMod.getAPI();
IAsyncBankManager bank = api.getServerBankManager().getAsync();

bank.getPersonalBankAccountAsync(player.getUUID())
    .thenCompose(account -> account == null ? CompletableFuture.completedFuture(null)
                                            : account.getBankAsync(MoneyItem.getItemID()))
    .thenCompose(moneyBank -> moneyBank == null ? CompletableFuture.completedFuture(null)
                                                : moneyBank.getRealBalanceAsync())
    .thenAccept(balance -> {
        // on a slave this runs on another thread: go back to the server thread first
        server.execute(() -> player.sendSystemMessage(Component.literal("Balance: " + balance)));
    });
```

**StockMarket:** check whether the diamond market is open. On the server thread:

```java
IStockMarketIntegration markets = StockMarketMod.getAPI().getIntegration();
if (markets != null) {   // null on a client without a running server
    ItemID diamond = ItemID.of(new ItemStack(Items.DIAMOND));
    boolean open = markets.marketExistsFor(diamond) && markets.isMarketOpen(diamond);
}
```

`ItemID` is BankSystem's item key (`net.kroia.banksystem.util.ItemID`). StockMarket uses it too.

## The rules that apply everywhere

- **Master and slave.** On a network, one server (the master) owns all bank and market data. The others (slaves) forward requests to it. See [Master and slave servers](../admin/multi-server.md).
- **Sync or async.** Every manager has a sync side and an async side. Sync calls return values at once but only exist on the master; `getSync()` returns `null` on a slave. Async calls return a `CompletableFuture` and work on every server. Use async unless your code only ever runs on the master.
- **Threads.** Call the APIs from the server thread. On the master, async calls complete at once. On a slave, the answer arrives on another thread: move back to the server thread (`server.execute(...)`) before you touch the world or players.
- **Failures.** On a slave, an async call can fail, for example when the connection to the master drops. Handle the exceptional completion. A request without an answer may still have been applied, so never refund or retry blindly. The [BankSystem API](banksystem/api.md) page explains which failure means what.
- **Raw and real amounts.** Money is stored as whole numbers (raw), with two decimals shown to players (real). Methods named `...Real...` take or return the shown value, for example `12.50`.

## Related pages

- [Setting up your project](setup.md): Gradle and the mod dependency.
- [BankSystem API](banksystem/api.md): the bank in detail.
- [Plugin system overview](stockmarket/plugins/index.md): writing a StockMarket plugin.
