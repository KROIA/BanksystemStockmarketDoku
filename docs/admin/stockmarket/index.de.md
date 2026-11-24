---
title: "StockMarket für Admins"
description: "Die Admin-Werkzeuge von StockMarket im Überblick und die empfohlene Reihenfolge beim Einrichten."
---

# StockMarket für Admins { #stockmarket-for-admins }

Die meiste Admin-Arbeit in StockMarket erledigst du in einem einzigen Fenster: `/stockmarket manage`. Dort erstellst du Märkte, bearbeitest Voreinstellungen, öffnest die Mod-Einstellungen und stellst die Plugins ein. Dafür brauchst du das StockMarket-Admin-Flag. Du vergibst es mit `/stockmarket op <player>`, siehe [Admins und Berechtigungen](../permissions.md).

## Einen neuen Server einrichten { #setting-up-a-new-server }

Eine neue Welt hat keine Märkte. In dieser Reihenfolge kommst du schnell zu einer funktionierenden Börse:

1. **Mach dich zum Admin** mit `/stockmarket op`.
2. **Wähle die Art des Markts**: mit Bot-Orders, damit Spieler immer handeln können, oder nur mit Spielern. Siehe [Ein Markt-Setup wählen](setup-use-cases.md). Im Zweifel bleibst du beim Standard mit Bots.
3. **Prüfe die Voreinstellungen.** Sie enthalten den Startpreis und die Einstellungen jedes Items. Siehe [Markt-Voreinstellungen](presets.md).
4. **Erstelle die Märkte** auf dem Tab **Märkte erstellen**. Siehe [Märkte erstellen und verwalten](markets.md#creating-markets).
5. **Sieh dir die Mod-Einstellungen an**, zum Beispiel die Kerzenlänge und wie schnell die Wirkung des Spielerhandels auf den Preis abklingt. Siehe [Mod-Einstellungen](mod-settings.md).
6. **Optional:** Lege [Handelszeiten](trading-hours.md) fest, schalte den [Dorfbewohner-Handel](villager-trading.md) ein oder aus und passe die [News](news/index.md) an.

Die Preis-Plugins funktionieren mit ihren Standardwerten. Stelle sie später ein, sobald du siehst, wie deine Spieler handeln.

## Was du tun kannst { #what-you-can-do }

| Ich möchte | Lies |
|---|---|
| Zwischen Bot-Märkten und reinen Spielermärkten wählen | [Ein Markt-Setup wählen](setup-use-cases.md) |
| Einen Markt erstellen, ändern, pausieren oder entfernen | [Märkte erstellen und verwalten](markets.md) |
| Den Startpreis von Items für neue Märkte ändern | [Markt-Voreinstellungen](presets.md) |
| Serverweite Einstellungen ändern | [Mod-Einstellungen](mod-settings.md) |
| Märkte zu festen Zeiten öffnen und schließen | [Handelszeiten](trading-hours.md) |
| Dorfbewohner zu Marktpreisen handeln lassen | [Dorfbewohner-Handel](villager-trading.md) |
| Ändern, wie sich Preise von selbst bewegen | [Plugins](plugins/index.md) |
| News-Ereignisse schreiben oder ändern | [News-System](news/index.md) |
| StockMarket auf mehreren Servern betreiben | [Master- und Slave-Server](../multi-server.md) |
| Die Marktdaten sichern | [Datendateien und Backups](../backups.md) |

## Gut zu wissen { #good-to-know }

- **Das Admin-Flag ist nicht der Operator-Status.** Auch ein Operator braucht `/stockmarket op`, um das Verwaltungsfenster zu öffnen. Ein Server mit LuckPerms kann das Flag stattdessen an einen Berechtigungs-Node koppeln.
- **Nutze den Wartungsmodus, während du etwas änderst.** Auf einem pausierten Markt kann niemand handeln, also profitiert niemand von einem Preissprung, während du ihn einstellst. Siehe [Wartungsmodus](markets.md#maintenance-mode).
- **In einem Netzwerk entscheidet der Master.** Märkte, Voreinstellungen, Plugins und News liegen auf dem Master-Server.

## Verwandte Seiten { #related-pages }

- [Server-Admin-Übersicht](../index.md): Einrichtung, Integrationen und beide Mods.
- [Admin-Befehle](../commands.md): alle Admin-Befehle beider Mods.
- [Funktionen zum Ein- und Ausschalten](../features.md): jeder Schalter an einem Ort.
