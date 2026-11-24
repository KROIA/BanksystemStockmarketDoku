---
title: "Server-Admin"
description: "Eine Checkliste für die erste Einrichtung beider Mods und wo jede Konfigurations- und Datendatei liegt."
---

# Server-Admin { #server-admin }

Dieser Teil ist für alle, die einen Server mit BankSystem und StockMarket betreiben. Die Bank funktioniert sofort: Jeder Spieler bekommt ein Konto, und ein paar gängige Items lassen sich einzahlen. Die Märkte legst du selbst an. Mit der Checkliste unten machst du einen Server für die Spieler bereit.

## Erste Einrichtung { #first-setup }

1. **Installiere** BankSystem, StockMarket und die benötigten Mods auf dem Server und auf jedem Client. Siehe [Installation und Updates](install.md).
2. **Mach dich zum Admin** beider Mods: `/banksystem op` und `/stockmarket op`. Siehe [Admins und Berechtigungen](permissions.md).
3. **Wähle die bankfähigen Items** mit `/banksystem manage` aus, oder schalte **Allow all items** ein. Siehe [Bankfähige Items](banksystem/bankable-items.md).
4. **Lege Startgeld und Grenzen fest** in den [Mod-Einstellungen](banksystem/settings.md) von BankSystem: **Starting balance** sowie Konten und Unternehmen pro Spieler.
5. **Richte die Märkte ein** mit `/stockmarket manage`: welche Items gehandelt werden können, ihre Preise und Bots. Siehe [StockMarket für Admins](stockmarket/index.md).
6. **Plane deine Backups**. Siehe [Datendateien und Backups](backups.md).
7. **Optional:** Verbinde weitere Server ([Master- und Slave-Server](multi-server.md)), zeige Kontostände in der Tab-Liste an ([Platzhalter](placeholders.md)) oder poste nach Discord ([Discord-Feed](discord.md)).

## Wo die Dateien liegen { #where-the-files-are }

| Was | Wo |
|---|---|
| Daten und Einstellungen von BankSystem | `<world>/data/BankSystem/` |
| Daten und Einstellungen von StockMarket | `<world>/data/StockMarket/` |
| Netzwerkverbindung | `config/modutilities/MultiServerConfig.json` |
| Discord-Webhooks | `config/modutilities/discord/` |
| News-Ereignisse | `config/StockMarket/news/` |

Die Einstellungen liegen im Weltordner, also hat jede Welt ihre eigenen. [Datendateien und Backups](backups.md) listet jede Datei auf.

## Finde dein Thema { #find-your-topic }

| Ich möchte | Lies |
|---|---|
| jeden Schalter beider Mods sehen | [Funktionen ein- und ausschalten](features.md) |
| einen Befehl nachschlagen | [Admin-Befehle](commands.md) |
| den Kontostand eines Spielers korrigieren oder ein Konto einfrieren | [Konten verwalten](banksystem/accounts.md) |
| herausfinden, wer geschummelt hat | [Audit und Anti-Cheat](audit/index.md) |
| ein Problem lösen | [Fehlerbehebung](troubleshooting.md) |

## Verwandte Seiten { #related-pages }

- [BankSystem für Admins](banksystem/index.md): die Admin-Werkzeuge der Bank.
- [StockMarket für Admins](stockmarket/index.md): Märkte, Plugins und News.
- [Wie die beiden Mods zusammenarbeiten](../together.md): das große Ganze.
