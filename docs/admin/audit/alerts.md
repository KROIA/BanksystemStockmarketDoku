---
title: "Alerts and suspicion flags"
description: "BankSystem's suspicion flags and StockMarket's profit and pump-and-dump alerts: what triggers them, who gets them and their settings."
---

# Alerts and suspicion flags

Both mods watch for patterns that often mean cheating or an exploit, and warn the admins in chat. An alert is a hint to look closer, not proof. Neither mod blocks a player or takes anything back on its own.

<figure markdown="span">
  ![Chat with a BankSystem suspicion alert and a StockMarket profit alert](../../assets/images/placeholder.svg){ width="600" }
  <figcaption>Image missing: shared/alert-chat.png</figcaption>
</figure>

## BankSystem flags

The master server checks every deposit, withdrawal and transfer, also those made on slave servers. A hit raises a **flag** on the account. Flags 1 to 5 look at money only and can be tuned under **Suspicious activity** in the [Mod Settings](../banksystem/settings.md#suspicious-activity), with amounts in whole dollars. Flags 6 to 9 are always on.

| # | Flag | Raised when |
|---:|---|---|
| 1 | **Banknote laundering** | Someone deposits at least $1,000,000 in banknotes, but withdrew less than that themselves in the last 24 hours. Typical case: one player withdraws notes, another deposits them. |
| 2 | **Large withdrawal** | A player withdraws at least $10,000,000 from one account in one go. Withdrawals less than 30 seconds apart count as one go. |
| 3 | **Wealth jump** | An account's wealth more than doubles **and** grows by more than $1,000,000 within an hour. Checked every 10 minutes, at most once per account every 6 hours. Wealth counts items at market prices, so a price spike can cause it; the flag shows the cash change so you can tell. Needs StockMarket for the prices. |
| 4 | **Transfer to a new account** | At least $1,000,000 arrives in an account younger than 24 hours, by transfer, payout or dividend. |
| 5 | **Money supply growth** | All money on the server together grows by more than 10 % **and** more than $10,000,000 within an hour. This flag is for the whole server, not an account. It stays quiet in the first hour of a new world. |
| 6 | **Transfer outcome unknown** | On a network, value was sent to a slave server and no answer came back, so nobody knows whether it arrived. Nothing is refunded. Check with the player and correct the balance by hand if the items never arrived. |
| 7 | **Currency binding suspended** | A [currency binding](../../banksystem/currency-bindings.md) points to a Numismatics or Lightman's account that the account's owner or managers aren't allowed to bind. See below. |
| 8 | **More shares than stamped** | More shares of a company are in the banks than were ever stamped. The company's dividends pause. See [Share integrity](../banksystem/companies.md#share-integrity). |
| 9 | **Shares created without a stamper** | A player got stamped shares from `/give` or the creative inventory. |

The numbers in the table are the defaults. Each flag has a severity: LOW, MEDIUM or HIGH.

### Suspended currency bindings

Players can only bind a bank account to a currency account that belongs to them or, for a shared account, to one of its managers. Bindings made with older versions weren't checked, so the master checks each one once at every start. A binding that breaks the rule is **suspended**: it keeps its money, but nothing moves through it until you decide.

- **The binding is fine** (for example, the currency account belongs to a former manager): restore it on the master server with

    ```text
    /banksystem restorebinding <account number> [item]
    ```

    Without an item, all suspended bindings of the account are restored. A restored binding is not checked again.

- **The binding is not fine**: leave it suspended, or delete the bank or the account. The money BankSystem held for it is then recorded and not paid out.

## StockMarket alerts

The master server watches player trades. Bot orders are not checked.

| Alert | Raised when | Settings (default) |
|---|---|---|
| **Profit alert** | A player's realized trading profit (sales minus purchases over all markets) goes above the threshold within the window. Once per window. Selling items bought long ago counts too. | **Profit alert threshold** (1,000,000, `0` = off), **Profit alert window (min)** (60) |
| **Pump** | A player's market buy moved the price up by more than the set percent, while the same player has a sell order waiting above the old price. | **Pump-and-dump detection** (on), **Pump price move (%)** (20, `0` = off) |
| **Buy-sell cycle** | A player sells an item they bought on the same market within the window, at a profit above the threshold. | **Buy-sell cycle window (min)** (30), **Buy-sell cycle profit threshold** (100,000, `0` = off) |

All settings are in the Market group of the StockMarket [Mod Settings](../stockmarket/mod-settings.md) and take effect at once. The windows are kept in memory, so a restart starts new ones.

## Who gets the alerts

| | BankSystem | StockMarket |
|---|---|---|
| Chat | Every online BankSystem admin, on the master and on slaves | Online players on the master with the permission `stockmarket.admin.notify` (operator level 2 without a permission mod) |
| Turn chat off for yourself | `/banksystem alerts off` (`on` turns it back on) | `/stockmarket alerts off` (`on`), master only |
| Default for admins who never used the command | **Admin alerts on by default** (on) | **Alert chat on by default** (on) |
| Always written to | The daily audit file, see [Daily digest and reports](reports.md) | The server log, lines start with `[StockMarket Alert]` |

Your choice is saved and survives restarts. Turning chat off only mutes chat: files, logs and the [Discord feed](../discord.md) keep getting every alert.

BankSystem also sends every admin action in chat, for example *AdminName added $500.00 to Account #7*, so admins see each other's changes.

## Related pages

- [Investigating in game](investigating.md): look into a flagged account.
- [Managing accounts](../banksystem/accounts.md): freeze an account or correct a balance.
- [Daily digest and reports](reports.md): all flags of a day in one file.
