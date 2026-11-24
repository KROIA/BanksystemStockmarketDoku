---
title: "Installation und Updates"
description: "Benötigte und optionale Mods, passende Versionen, Fabric und NeoForge und das Update auf eine neue Version."
---

# Installation und Updates { #installation-and-updates }

Beide Mods laufen auf **Fabric** und **NeoForge**, für Minecraft 1.21.1 bis 1.21.11, 26.1.2, 26.2 und 26.3. Installiere sie auf dem Server **und** auf dem Client jedes Spielers.

## Benötigte Mods { #required-mods }

| Mod | Nur BankSystem | BankSystem + StockMarket |
|---|---|---|
| [BankSystem](https://www.curseforge.com/minecraft/mc-mods/banksystem) | ✓ | ✓ |
| [StockMarket](https://www.curseforge.com/minecraft/mc-mods/stockmarket) | | ✓ |
| [Architectury API](https://www.curseforge.com/minecraft/mc-mods/architectury-api) | ✓ | ✓ |
| [Fabric API](https://www.curseforge.com/minecraft/mc-mods/fabric-api) | Nur Fabric | Nur Fabric |

BankSystem braucht außerdem ModUtilities, aber ModUtilities steckt schon in der BankSystem-Jar. Du musst es nicht installieren.

Wähle die Dateien für deine Minecraft-Version und deinen Loader. StockMarket braucht BankSystem aus derselben Versionslinie: StockMarket `2.2.x` läuft mit BankSystem `2.2.x`.

## Optionale Mods { #optional-mods }

| Mod | Was sie hinzufügt | Siehe |
|---|---|---|
| JEI | Rezepte aller Blöcke und das Füllen des Crafting-Rasters im Bank Terminal aus der Bank. | [Bank Terminal](../banksystem/bank-terminal.md) |
| LuckPerms | Berechtigungs-Nodes für jeden Befehl und die Kopplung des Admin-Modus an eine Gruppe. | [Admins und Berechtigungen](permissions.md) |
| Numismatics | Spieler können ein Bankkonto mit ihrem Numismatics-Geld verknüpfen. | [Währungsbindungen](../banksystem/currency-bindings.md) |
| Lightman's Currency | Dasselbe für Lightman's Currency. Nur NeoForge. | [Währungsbindungen](../banksystem/currency-bindings.md) |
| TAB, Placeholder API | Kontostände und Preise in der Tab-Liste, im Scoreboard oder im Chat. | [Platzhalter](placeholders.md) |

### LuckPerms-Versionen { #luckperms-versions }

Verwende einen LuckPerms-Build, der für deine Minecraft-Version und deinen Loader gemacht ist. Ein Build für eine andere Version kann den Server beim Start abstürzen lassen. Diese Builds funktionieren nachweislich:

| Minecraft | Fabric | NeoForge |
|---|---|---|
| 1.21.1 | 5.4.140 | 5.4.149 oder neuer (ältere Builds werfen beitretende Spieler raus) |
| 1.21.2, 1.21.3 | 5.4.145 | 5.4.149 |
| 1.21.4 | 5.4.150 | 5.4.158 |
| 1.21.5 | 5.5.4 | keiner, siehe unten |
| 1.21.6 bis 1.21.8 | 5.5.10 | 5.5.10 |
| 1.21.9, 1.21.10 | 5.5.17 | 5.5.17 |
| 1.21.11 | 5.5.21 | 5.5.21 |
| 26.1.2, 26.2 | 5.5.85 | 5.5.85 |
| 26.3 | 5.5.85 | 5.5.87 |

Auf NeoForge für 1.21.5 startet kein LuckPerms-Build, auch ohne diese Mods nicht. Betreibe diesen Server ohne LuckPerms; die Mods verwenden dann die normalen Operator-Level.

## Erster Start { #first-start }

1. Lege die Jars in den Ordner `mods/` des Servers und jedes Clients.
2. Starte den Server einmal. Beide Mods legen ihre Dateien im Weltordner an, siehe [Datendateien und Backups](backups.md).
3. Tritt bei und mach dich zum Admin beider Mods, siehe [Admins und Berechtigungen](permissions.md).
4. Folge der [Checkliste für die erste Einrichtung](index.md#first-setup).

## Aktualisieren { #updating }

1. **Sichere die Welt**, siehe [Datendateien und Backups](backups.md).
2. Ersetze die Jars aller Mods auf dem Server und auf jedem Client. Aktualisiere BankSystem und StockMarket gemeinsam.
3. In einem Netzwerk aktualisierst du den Master und jeden Slave-Server auf dieselben Versionen.
4. Starte den Server.

Beim ersten Start bringt jede Mod ihre Daten auf die neue Version. Bevor sie etwas ändert, speichert sie ein Zip ihrer alten Daten in `<world>/data/BankSystem_backups/` oder `<world>/data/StockMarket_backups/`.

!!! warning "Es gibt keinen Weg zurück"
    Nach einem Update kann eine ältere Version der Mods die Welt nicht mehr öffnen. Um zurückzugehen, stellst du das Backup von vor dem Update wieder her.

Wenn ein Update fehlschlägt, lädt die Welt nicht, und das Log sagt, warum. Siehe [Fehlerbehebung](troubleshooting.md#the-world-doesnt-load).

## Verwandte Seiten { #related-pages }

- [Server-Admin](index.md): die Checkliste für die erste Einrichtung.
- [Admins und Berechtigungen](permissions.md): mach dich zum Admin.
- [Master- und Slave-Server](multi-server.md): eine Wirtschaft über mehrere Server.
