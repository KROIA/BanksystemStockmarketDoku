---
title: "Admin-Befehle"
description: "Jeder Admin-Befehl beider Mods in einer Tabelle, mit der Berechtigung, die er braucht."
---

# Admin-Befehle { #admin-commands }

Diese Seite listet jeden Admin-Befehl beider Mods auf. Die Spielerbefehle stehen auf der Spielerseite von [BankSystem](../banksystem/commands.md).

**Benötigt** sagt, was ein Spieler haben muss:

- **Flag**: das Admin-Flag der Mod (`/banksystem op` oder `/stockmarket op`). Jeder Spieler sieht diese Befehle.
- **Op 2** oder **Op 3**: Operator-Level 2 oder 3 oder den Berechtigungs-Node in Klammern.

Die Flags und die Nodes erklärt [Admins und Berechtigungen](permissions.md). Befehle mit dem Hinweis „Master“ funktionieren nur auf dem Master-Server eines [Netzwerks](multi-server.md).

## BankSystem { #banksystem }

### Admins und Server { #admins-and-servers }

| Befehl | Benötigt | Was er tut |
|---|---|---|
| `/banksystem op [player]` | Op 2 (`banksystem.admin.command.op`) | Gibt das Admin-Flag von BankSystem. Master. |
| `/banksystem deop [player]` | Op 2 (`banksystem.admin.command.op`) | Nimmt das Flag weg. Master. |
| `/banksystem trust <slave id>` | Op 2 (`banksystem.admin.command.trust`) | Stuft einen Slave-Server als vertrauenswürdig ein. Master. Siehe [Master- und Slave-Server](multi-server.md#trusted-slaves). |
| `/banksystem untrust <slave id>` | Op 2 (`banksystem.admin.command.trust`) | Nimmt das Vertrauen wieder weg. Master. |
| `/banksystem serverInfo` | Alle | Zeigt die Rolle dieses Servers und, auf einem Slave, ob er vertrauenswürdig ist. |
| `/banksystem serverNetworkInfo` | Flag | Listet alle verbundenen Server und ihren Vertrauensstatus auf. |

`op`, `deop`, `trust` und `untrust` muss ein Spieler im Spiel eingeben. In der Serverkonsole funktionieren sie nicht.

### Items und Konten { #items-and-accounts }

| Befehl | Benötigt | Was er tut |
|---|---|---|
| `/banksystem manage` | Flag | Öffnet den Bildschirm Bank Einstellungen. |
| `/banksystem allowItem <item id>` | Flag | Lässt ein Item in der Bank zu. |
| `/banksystem allowItemInHand` | Flag | Lässt das Item in deiner Hand zu. |
| `/banksystem disallowItem <item id>` | Flag | Entfernt ein Item aus der Bank und aus jedem Konto. |
| `/banksystem disallowItemInHand` | Flag | Dasselbe für das Item in deiner Hand. |
| `/bank <player> manage` | Flag | Öffnet das Konto eines Spielers. |
| `/bank <player> show` | Flag | Zeigt die Kontostände eines Spielers im Chat. |
| `/money add [player] <amount>` | Flag | Fügt Geld hinzu. |
| `/money remove [player] <amount>` | Flag | Entfernt Geld. |
| `/money set [player] <amount>` | Flag | Setzt den Geld-Kontostand. |
| `/banksystem freeze <account> [on\|off]` | Flag | Friert ein Konto ein oder hebt das Einfrieren auf. Von der Konsole aus: Master. |
| `/company manage "<name>"` | Flag | Öffnet den Verwaltungsbildschirm eines beliebigen Unternehmens. |
| `/company shares acknowledge "<name>"` | Flag | Akzeptiert einen Aktienüberschuss und setzt die Dividenden fort. |
| `/banksystem symbols list\|add\|remove\|reload` | Flag | Verwaltet die Aktiensymbole. Master. Siehe [Unternehmen und Aktien](banksystem/companies.md#share-symbols). |
| `/banksystem restorebinding <account> [item]` | Flag | Stellt eine gesperrte Währungsbindung wieder her. Master. |

### Audit { #audit }

| Befehl | Benötigt | Was er tut |
|---|---|---|
| `/banksystem audit <player or account>` | Flag | Öffnet den Audit-Bildschirm. |
| `/banksystem history <player or account>` | Flag | Öffnet den Kontostandverlauf mit den Verdachtsmarkierungen. |
| `/banksystem alerts on\|off` | Flag | Schaltet die Chat-Alarme für dich ein oder aus. |
| `/banksystem auditreport <hours>` | Flag | Schreibt einen Bericht über die letzten 1 bis 720 Stunden. |

### Backups und Discord { #backups-and-discord }

| Befehl | Benötigt | Was er tut |
|---|---|---|
| `/banksystem backup snapshot <path>` | Op 2 (`banksystem.admin.command.backup`) | Schreibt eine sichere Kopie der Datenbank. Master. |
| `/banksystem backup pause\|resume\|status` | Op 2 (`banksystem.admin.command.backup`) | Pausiert die Schreibzugriffe auf die Datenbank für ein Datei-Backup. Master. |
| `/banksystem backup export [name]` | Op 2 (`banksystem.admin.command.backup`) | Schreibt das Exportpaket. Jeder Server. |
| `/banksystem discord status\|reload` | Op 3 (`modutilities.command.discord`) | Zeigt die Einrichtung des Discord-Feeds oder lädt sie neu. |

Siehe [Datendateien und Backups](backups.md) und [Discord-Feed](discord.md).

## StockMarket { #stockmarket }

| Befehl | Benötigt | Was er tut |
|---|---|---|
| `/stockmarket op [player]` | Op 2 (`stockmarket.admin.command.op`) | Gibt das Admin-Flag von StockMarket. Master. |
| `/stockmarket deop [player]` | Op 2 (`stockmarket.admin.command.op`) | Nimmt das Flag weg. Master. |
| `/stockmarket manage` | Flag | Öffnet die Marktverwaltung. Siehe [Märkte](stockmarket/markets.md). |
| `/stockmarket preset add <category> [name]` | Flag | Speichert das Item in deiner Hand als Markt-Voreinstellung. Siehe [Voreinstellungen](stockmarket/presets.md). |
| `/stockmarket open "<market>"` | Flag | Öffnet einen Markt bis zu seiner nächsten geplanten Änderung. Siehe [Handelszeiten](stockmarket/trading-hours.md). |
| `/stockmarket close "<market>"` | Flag | Schließt einen Markt bis zu seiner nächsten geplanten Änderung. |
| `/stockmarket "<market>" remove` | Flag | Entfernt einen Markt, auch einen, dessen Item es nicht mehr gibt. |
| `/stockmarket news …` | Flag | Steuert die News-Ereignisse. Siehe [News-Befehle](stockmarket/news/commands.md). |
| `/stockmarket alerts on\|off` | `stockmarket.admin.notify` | Schaltet die Handelsalarme im Chat für dich ein oder aus. Master. |
| `/stockmarket backup pause\|resume\|status` | Op 2 (`stockmarket.admin.command.backup`) | Pausiert die Schreibzugriffe auf die Datenbank für ein Datei-Backup. Master. |
| `/stockmarket discord status\|reload` | Op 3 (`modutilities.command.discord`) | Zeigt die Einrichtung des Discord-Feeds oder lädt sie neu. |

Ein Markt wird über seine Item-ID in Anführungszeichen angegeben, zum Beispiel `"minecraft:iron_ingot"`, oder über seine Nummer.

## Verwandte Seiten { #related-pages }

- [Admins und Berechtigungen](permissions.md): die Flags und die Nodes.
- [Spielerbefehle](../banksystem/commands.md): was Spieler eingeben können.
- [News-Befehle](stockmarket/news/commands.md): alle Unterbefehle von `/stockmarket news`.
