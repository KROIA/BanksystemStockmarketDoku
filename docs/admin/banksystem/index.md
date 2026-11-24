---
title: "BankSystem for admins"
description: "The BankSystem admin tools at a glance."
---

# BankSystem for admins

Most BankSystem admin work happens in two places: the **Bank Settings** screen (`/banksystem manage`) and the management screen of an account (`/bank <player> manage`). Both need the BankSystem admin flag. Give it with `/banksystem op <player>`, see [Admins and permissions](../permissions.md).

## What you can do

| I want to | Read |
|---|---|
| Change the starting balance, account limits or autosave | [Mod Settings](settings.md) |
| Choose which items players can bank | [Bankable items](bankable-items.md) |
| Fix a player's balance, release a locked amount or freeze an account | [Managing accounts](accounts.md) |
| Add share symbols or deal with copied shares | [Companies and shares](companies.md) |
| See who moved which money, and get alerts | [Audit and anti-cheat](../audit/index.md) |
| Run BankSystem on several servers | [Master and slave servers](../multi-server.md) |
| Back up the bank data | [Data files and backups](../backups.md) |

## Good to know

- **The admin flag is not operator status.** An operator still needs `/banksystem op` to open other players' accounts. A server with LuckPerms can tie the flag to a permission node instead.
- **Every admin change is recorded.** Balance edits, freezes and closed banks go into the transaction ledger with your name.
- **On a network, the master decides.** Settings, admins and bankable items live on the master server. A slave that isn't trusted can't make admin changes.

## Related pages

- [Server Admin overview](../index.md): setup, integrations and both mods.
- [Admin commands](../commands.md): every admin command of both mods.
- [Features you can turn on and off](../features.md): every switch in one place.
