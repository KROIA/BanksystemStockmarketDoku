---
title: "Installation and updates"
description: "Required and optional mods, matching versions, Fabric and NeoForge, and updating to a new version."
---

# Installation and updates

Both mods run on **Fabric** and **NeoForge**, for Minecraft 1.21.1 to 1.21.11, 26.1.2, 26.2 and 26.3. Install them on the server **and** on every player's client.

## Required mods

| Mod | BankSystem only | BankSystem + StockMarket |
|---|---|---|
| [BankSystem](https://www.curseforge.com/minecraft/mc-mods/banksystem) | ✓ | ✓ |
| [StockMarket](https://www.curseforge.com/minecraft/mc-mods/stockmarket) | | ✓ |
| [Architectury API](https://www.curseforge.com/minecraft/mc-mods/architectury-api) | ✓ | ✓ |
| [Fabric API](https://www.curseforge.com/minecraft/mc-mods/fabric-api) | Fabric only | Fabric only |

BankSystem also needs ModUtilities, but ModUtilities is already inside the BankSystem jar. You don't have to install it.

Pick the files for your Minecraft version and loader. StockMarket needs BankSystem of the same version line: StockMarket `2.2.x` runs with BankSystem `2.2.x`.

## Optional mods

| Mod | What it adds | See |
|---|---|---|
| JEI | Recipes of all blocks, and filling the Bank Terminal's crafting grid from the bank. | [Bank Terminal](../banksystem/bank-terminal.md) |
| LuckPerms | Permission nodes for every command, and tying admin mode to a group. | [Admins and permissions](permissions.md) |
| Numismatics | Players can link a bank account to their Numismatics money. | [Currency bindings](../banksystem/currency-bindings.md) |
| Lightman's Currency | The same for Lightman's Currency. NeoForge only. | [Currency bindings](../banksystem/currency-bindings.md) |
| TAB, Placeholder API | Balances and prices in the tab list, scoreboard or chat. | [Placeholders](placeholders.md) |

### LuckPerms versions

Use a LuckPerms build made for your Minecraft version and loader. A build for another version can crash the server at start. These builds are known to work:

| Minecraft | Fabric | NeoForge |
|---|---|---|
| 1.21.1 | 5.4.140 | 5.4.149 or newer (older builds kick joining players) |
| 1.21.2, 1.21.3 | 5.4.145 | 5.4.149 |
| 1.21.4 | 5.4.150 | 5.4.158 |
| 1.21.5 | 5.5.4 | none, see below |
| 1.21.6 to 1.21.8 | 5.5.10 | 5.5.10 |
| 1.21.9, 1.21.10 | 5.5.17 | 5.5.17 |
| 1.21.11 | 5.5.21 | 5.5.21 |
| 26.1.2, 26.2 | 5.5.85 | 5.5.85 |
| 26.3 | 5.5.85 | 5.5.87 |

No LuckPerms build starts on NeoForge for 1.21.5, even without these mods. Run that server without LuckPerms; the mods then use the normal operator levels.

## First start

1. Put the jars into the `mods/` folder of the server and of every client.
2. Start the server once. Both mods create their files in the world folder, see [Data files and backups](backups.md).
3. Join and make yourself admin of both mods, see [Admins and permissions](permissions.md).
4. Follow the [first-setup checklist](index.md#first-setup).

## Updating

1. **Back up the world**, see [Data files and backups](backups.md).
2. Replace the jars of all mods on the server and on every client. Update BankSystem and StockMarket together.
3. On a network, update the master and every slave server to the same versions.
4. Start the server.

On the first start, each mod brings its data up to the new version. Before it changes anything, it saves a zip of its old data to `<world>/data/BankSystem_backups/` or `<world>/data/StockMarket_backups/`.

!!! warning "There is no way back"
    After an update, an older version of the mods can't open the world any more. To go back, restore the backup from before the update.

If an update fails, the world doesn't load and the log says why. See [Troubleshooting](troubleshooting.md#the-world-doesnt-load).

## Related pages

- [Server Admin](index.md): the first-setup checklist.
- [Admins and permissions](permissions.md): make yourself admin.
- [Master and slave servers](multi-server.md): one economy across several servers.
