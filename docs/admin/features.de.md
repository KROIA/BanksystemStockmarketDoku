---
title: "Funktionen ein- und ausschalten"
description: "Jeder Ein-/Aus-Schalter beider Mods in einer Liste, mit Standardwert und dem Ort, an dem du ihn änderst."
---

# Funktionen ein- und ausschalten { #features-you-can-turn-on-and-off }

Diese Seite listet jede Funktion auf, die du ein- oder ausschalten kannst, mit ihrem Standardwert. Die meisten Schalter liegen im Bildschirm **Mod Settings** bzw. **Mod-Einstellungen** der jeweiligen Mod, der nur auf dem Master-Server erscheint:

- BankSystem: `/banksystem manage` → **Mod Settings**, siehe [Mod-Einstellungen von BankSystem](banksystem/settings.md).
- StockMarket: `/stockmarket manage` → **Mod-Einstellungen**, siehe [Mod-Einstellungen von StockMarket](stockmarket/mod-settings.md).

Schalter mit dem Hinweis „Neustart“ wirken erst nach einem Neustart des Servers.

## Beide Mods { #both-mods }

| Funktion | Einstellung in BankSystem | Einstellung in StockMarket | Standard |
|---|---|---|---|
| [Platzhalter](placeholders.md) für TAB und Placeholder API | **Platzhalter aktiviert** (Neustart) | **Platzhalter (TAB / Placeholder API)** (Neustart) | an |
| [Discord-Feed](discord.md) | **Discord-Feed** | **Discord-Feed (Trades und Warnungen)** | aus |
| [LuckPerms-Synchronisierung](permissions.md#syncing-the-admin-flag-with-luckperms) des Admin-Flags | **Admin-Flag mit LuckPerms synchronisieren** | **Admin-Flag mit LuckPerms synchronisieren** (Neustart) | aus |
| Alarme im Chat für Admins, die nie eine Wahl getroffen haben | **Admin-Benachrichtigungen standardmäßig an** | **Alarm-Chat standardmäßig an** | an |
| Debug-Meldungen im Log | **Enable debug logging** | **Debug-Meldungen loggen** | aus |

## BankSystem { #banksystem }

| Funktion | Einstellung | Standard |
|---|---|---|
| Jedes Item einzahlen außer denen auf einer Sperrliste | **Allow all items** | aus |
| Bindungen an [Numismatics](../banksystem/currency-bindings.md) | **Numismatics-Integration** | an |
| Bindungen an [Lightman's Currency](../banksystem/currency-bindings.md) | **Lightman's-Currency-Integration** | an |
| Verlauf der Kontostände | **Balance snapshot interval (minutes)**, `0` = aus | an (jede Minute) |
| Alten Verlauf ausdünnen | **History retention sweep (minutes)**, `0` = nur beim Serverstart | an |
| [Verdachtsmarkierungen](audit/alerts.md#banksystem-flags) 1 bis 5 | Je ein Schalter **… markieren** | an |
| [Täglicher Bericht](audit/reports.md#the-daily-digest) | **Täglicher Audit-Bericht** | an |

Eine Währungs-Mod, die du ausschaltest, verhält sich, als wäre sie nicht installiert: Geld, das an sie gebunden ist, bleibt dort eingefroren, bis du sie wieder einschaltest.

## StockMarket { #stockmarket }

| Funktion | Einstellung | Standard |
|---|---|---|
| [Dorfbewohner-Handel](stockmarket/villager-trading.md) zu Marktpreisen | **Dorfbewohner-Handel aktiviert** | an |
| Dorfbewohner-Handel mit Items ohne Markt verwendet auch Geld, mit Preisen aus dem Smaragd-Markt | **Smaragde bei nicht gelisteten Items ersetzen** | aus |
| Dieser Handel verwendet stattdessen den Standardpreis der Voreinstellung | **Preset-Preise für Dorfbewohner verwenden** | aus |
| [Gewinnalarm](audit/alerts.md#stockmarket-alerts) | **Gewinnalarm-Schwelle**, `0` = aus | an |
| [Pump-and-Dump-Erkennung](audit/alerts.md#stockmarket-alerts) | **Pump-and-Dump-Erkennung** | an |
| [Web-Oberfläche](web-interface.md), nur lesend | **Web-Oberfläche (nur lesen)** | aus |
| Kerzen folgen der Spielzeit statt der echten Zeit | **Kerzen: Spielzeit verwenden** (Neustart) | aus |
| Handelszeiten folgen der echten Zeit statt der Spielzeit | **Handelszeiten: Echtzeit** | aus |

### Pro Markt { #per-market }

Diese Schalter liegen in den Einstellungen des Markts im Verwaltungsbildschirm (`/stockmarket manage`), siehe [Märkte](stockmarket/markets.md).

| Funktion | Einstellung | Standard |
|---|---|---|
| Spieler können keine Orders aufgeben; ihre offenen Orders werden storniert und erstattet | **Wartungsmodus** | aus |
| Bots liefern Liquidität und lenken den Preis | **Virtuelles Orderbuch aktiv** | an |
| [Handelszeiten](stockmarket/trading-hours.md) | **Handelszeiten** | |
| [Preis-Plugins](stockmarket/plugins/index.md) und [News-Ereignisse](stockmarket/news/index.md) | Der eigene Bildschirm jedes Plugins | |

## Verwandte Seiten { #related-pages }

- [Mod-Einstellungen von BankSystem](banksystem/settings.md): jede Einstellung von BankSystem.
- [Mod-Einstellungen von StockMarket](stockmarket/mod-settings.md): jede Einstellung von StockMarket.
- [Admins und Berechtigungen](permissions.md): wer die Einstellungen ändern darf.
