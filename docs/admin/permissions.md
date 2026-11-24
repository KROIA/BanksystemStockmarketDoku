---
title: "Admins and permissions"
description: "StockMarket and BankSystem admin mode, operator levels, and the LuckPerms nodes and sync options."
---

# Admins and permissions

Each mod has its own **admin flag**, separate from Minecraft's operator status. The flag decides who can open the admin screens and edit other players' data. Operator levels and permission nodes decide who may give the flag out.

## Making someone admin

| Command | What it does |
|---|---|
| `/banksystem op [player]` | Gives the BankSystem admin flag to the player, or to you. |
| `/banksystem deop [player]` | Takes it away. |
| `/stockmarket op [player]` | Gives the StockMarket admin flag. |
| `/stockmarket deop [player]` | Takes it away. |

These commands need operator level 2, or the matching permission node below. They only work on the master server of a [network](multi-server.md). The flags are stored there, so they apply on every server.

An operator without the flag is not an admin: they can give themselves the flag, but until then they can't open other players' accounts or the market management.

## What each flag allows

**BankSystem admins** can:

- choose the bankable items and change the [Mod Settings](banksystem/settings.md);
- open, edit and freeze any account;
- manage any company;
- use the Audit screen, the balance histories and the reports;
- get the [chat alerts](audit/alerts.md).

**StockMarket admins** can:

- create, change and remove markets in the management screen (`/stockmarket manage`);
- use presets, open and close markets, and run the news admin commands;
- change the StockMarket [Mod Settings](stockmarket/mod-settings.md).

Most admin commands of both mods are visible to every player, but only run for a player with the flag. Others get an "admin only" message.

## Without a permission mod

Each permission node falls back to an operator level:

- Commands that set the flag, back up data or trust servers need **operator level 2**.
- Commands that only need the admin flag let every player through, and the flag decides.
- The console and command blocks always use operator level 2.

## Permission nodes

With LuckPerms (or another permission mod), you can grant or deny each node per player or group. Nodes are only checked for players on the server that runs the check.

### BankSystem

| Node | Grants |
|---|---|
| `banksystem.admin.command.op` | `/banksystem op` and `deop` |
| `banksystem.admin.adminmode` | Changing a player's admin flag |
| `banksystem.admin.command.trust` | `/banksystem trust` and `untrust` |
| `banksystem.admin.command.backup` | `/banksystem backup …` |
| `banksystem.admin.command.symbols` | `/banksystem symbols …` (also needs the admin flag) |
| `banksystem.admin.command.restorebinding` | `/banksystem restorebinding` (also needs the admin flag) |
| `banksystem.admin.software` | Using the Banking Software on another player (also needs the admin flag) |
| `banksystem.admin` | The admin flag itself, while the LuckPerms sync is on (see below) |

### StockMarket

| Node | Grants |
|---|---|
| `stockmarket.admin.command.op` | `/stockmarket op` and `deop` |
| `stockmarket.admin.command.manage` | `/stockmarket manage` (also needs the admin flag) |
| `stockmarket.admin.command.preset` | `/stockmarket preset …` (also needs the admin flag) |
| `stockmarket.admin.command.news` | The news admin commands (also needs the admin flag) |
| `stockmarket.admin.command.market` | `/stockmarket open`, `close` and `<market> remove` (also needs the admin flag) |
| `stockmarket.admin.command.backup` | `/stockmarket backup …` |
| `stockmarket.admin.notify` | StockMarket [alerts](audit/alerts.md) in chat, notices when another admin changes settings, and `/stockmarket alerts` |
| `stockmarket.admin` | The admin flag itself, while the LuckPerms sync is on (see below) |

Nodes marked "also needs the admin flag" are open to every player by default. You can only use them to take a command away: set the node to `false` to hide it, even from an admin.

The Discord commands of both mods use the node `modutilities.command.discord`, which needs operator level 3 without a permission mod.

To give a group every admin right of both mods:

```text
/lp group admin permission set banksystem.admin.* true
/lp group admin permission set stockmarket.admin.* true
```

A player whose nodes changed may need to rejoin before commands show up or disappear.

## Syncing the admin flag with LuckPerms

Turn on **Sync admin flag with LuckPerms** in the Integrations group of each mod's Mod Settings ([BankSystem](banksystem/settings.md#integrations), [StockMarket](stockmarket/mod-settings.md)). Then the admin flag and the node `banksystem.admin` (or `stockmarket.admin`) are kept in step, both ways:

- `/banksystem op <player>` also sets the node in LuckPerms, even for offline players. `deop` removes the player's own node.
- Granting or removing the node in LuckPerms, also through a group, changes the flag at once.
- A group grant wins: if a group still grants the node, the player stays admin after `deop`, and the command tells you so.
- When you first turn the sync on, every existing admin gets the node once. Nothing is removed.

!!! note "The wildcard doesn't include the flag"
    `banksystem.admin.*` doesn't grant `banksystem.admin` itself. Grant it on its own to make a group admin.

On a network, turn the sync on on the master. Slave servers pass LuckPerms changes on to the master only if the master [trusts](multi-server.md#trusted-slaves) them. The StockMarket sync needs a restart of the master after you turn it on.

## Related pages

- [Admin commands](commands.md): every command and the node it needs.
- [Master and slave servers](multi-server.md): trusting slave servers.
- [Installation and updates](install.md): LuckPerms versions that work.
