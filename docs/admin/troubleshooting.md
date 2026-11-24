---
title: "Troubleshooting"
description: "Common server problems with both mods: a world that won't load, missing items, untrusted slaves and screens that don't open."
---

# Troubleshooting

When something goes wrong, look at the server log first (`logs/latest.log`). Both mods write their messages with `[BankSystem]` or `[StockMarket]` at the start.

## The world doesn't load

Both mods check their data before a world loads. If something is wrong, they stop the world instead of risking your players' money. Nothing is changed. In singleplayer, a screen titled *BankSystem did not load this world* or *StockMarket did not load this world* explains why. On a server, the reason is in the log.

| Reason | What to do |
|---|---|
| *Saved bank items belong to mods that are not installed* | You removed a mod whose items were in the bank. Install the mod again. Or remove the items: in singleplayer click **Remove missing items and load**; on a server turn on **Remove items of missing mods (one-shot)** in `settings.json` and start again. Removing deletes those balances from every account, after a backup of the BankSystem data. |
| *These different items would become the same item* | A changed mod or a changed [component list](banksystem/bankable-items.md#changing-the-lists-on-a-world-in-use) would merge items that are different now. Undo the change, or confirm the merge: **Confirm merge and load** in singleplayer, **Confirm pending item merge (one-shot)** in `settings.json` on a server. Confirming adds their balances together. |
| A pending world repair in the log | The item list was damaged by a very old BankSystem version. Back up the world, turn on **Confirm pending world repair (one-shot)** in `settings.json` and start again. |
| *This world was saved by a newer version* | The world was opened with a newer version of the mod before. Update the mod, or restore a backup from before. |
| *Upgrading this world's data to the new version failed* | Read the reason in the log and fix it, then open the world again to continue the upgrade. Or restore the backup zip the message names. See [Installation and updates](install.md#updating). |

The one-shot settings switch themselves off after one start. Edit `settings.json` only while the server is stopped, see [Mod Settings](banksystem/settings.md#the-settings-file).

## Players can't put an item into the bank

| Cause | Fix |
|---|---|
| The item isn't allowed. | Allow it in the [Bank Settings](banksystem/bankable-items.md). |
| The item is damaged or enchanted. | Such items can't be banked. The player has to repair it or remove the enchantment. |
| The item is renamed or carries other extra data. | It is a different item from the plain one. Allow that exact item with `/banksystem allowItemInHand`. |
| *The condition of … prevents banking it* | A [deposit-gated](banksystem/bankable-items.md#items-whose-data-changes) item, for example old TerraFirmaCraft food, isn't fresh enough. |
| The account is frozen. | Unfreeze it, see [Managing accounts](banksystem/accounts.md#freezing-an-account). |
| The player is on an untrusted slave. | See below. |

## Problems on a slave server

| Problem | Fix |
|---|---|
| Players see *This server is not trusted by the master* and can only look | Run `/banksystem trust <slave id>` on the master. |
| Placeholders and Bank Displays are empty on one server | That slave is not trusted. |
| *Request to the master server failed or timed out* | The master was slow, restarting or unreachable. Check the result before trying again, so nothing happens twice. |
| The slave can't connect | Check `masterHost`, `masterTcpPort` and `sharedSecret`, and that the port is open. See [Master and slave servers](multi-server.md#troubleshooting). |

## Screens and commands

| Problem | Fix |
|---|---|
| An admin command answers "admin only" | You need the mod's admin flag: `/banksystem op` or `/stockmarket op`. Being operator is not enough. See [Admins and permissions](permissions.md). |
| A command doesn't show up after a permission change | Rejoin the server. |
| The **Mod Settings** button is missing | It only shows on the master server. |
| A player's amount stays locked | Read [Locked amounts](banksystem/accounts.md#locked-amounts) before you unlock it. |

## Related pages

- [Data files and backups](backups.md): restore a backup.
- [Master and slave servers](multi-server.md): network problems.
- [Bankable items](banksystem/bankable-items.md): which items the bank accepts.
