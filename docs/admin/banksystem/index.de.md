---
title: "BankSystem für Admins"
description: "Die Admin-Werkzeuge von BankSystem auf einen Blick."
---

# BankSystem für Admins { #banksystem-for-admins }

Die meiste Admin-Arbeit in BankSystem findet an zwei Orten statt: im Fenster **Bank Einstellungen** (`/banksystem manage`) und im Verwaltungsfenster eines Kontos (`/bank <player> manage`). Für beide brauchst du das BankSystem-Admin-Flag. Du vergibst es mit `/banksystem op <player>`, siehe [Admins und Berechtigungen](../permissions.md).

## Was du tun kannst { #what-you-can-do }

| Ich möchte | Lies |
|---|---|
| Das Startguthaben, die Kontolimits oder das automatische Speichern ändern | [Mod Settings](settings.md) |
| Festlegen, welche Items Spieler in die Bank legen können | [Bankfähige Items](bankable-items.md) |
| Den Kontostand eines Spielers korrigieren, einen reservierten Betrag freigeben oder ein Konto einfrieren | [Konten verwalten](accounts.md) |
| Aktiensymbole hinzufügen oder mit kopierten Aktien umgehen | [Unternehmen und Aktien](companies.md) |
| Sehen, wer welches Geld bewegt hat, und Alarme bekommen | [Audit und Anti-Cheat](../audit/index.md) |
| BankSystem auf mehreren Servern betreiben | [Master- und Slave-Server](../multi-server.md) |
| Die Bankdaten sichern | [Datendateien und Backups](../backups.md) |

## Gut zu wissen { #good-to-know }

- **Das Admin-Flag ist nicht der Operator-Status.** Auch ein Operator braucht `/banksystem op`, um die Konten anderer Spieler zu öffnen. Ein Server mit LuckPerms kann das Flag stattdessen an einen Berechtigungs-Node binden.
- **Jede Admin-Änderung wird aufgezeichnet.** Geänderte Kontostände, eingefrorene Konten und geschlossene Banken landen mit deinem Namen im Transaktionsbuch.
- **In einem Netzwerk entscheidet der Master.** Einstellungen, Admins und bankfähige Items liegen auf dem Master-Server. Ein Slave, der nicht vertrauenswürdig ist, kann keine Admin-Änderungen vornehmen.

## Verwandte Seiten { #related-pages }

- [Server-Admin-Übersicht](../index.md): Einrichtung, Integrationen und beide Mods.
- [Admin-Befehle](../commands.md): jeder Admin-Befehl beider Mods.
- [Funktionen, die du ein- und ausschalten kannst](../features.md): jeder Schalter an einem Ort.
