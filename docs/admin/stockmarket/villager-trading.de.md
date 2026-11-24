---
title: "Dorfbewohner-Handel"
description: "Die Datendatei der Dorfbewohner-Angebote und die Einstellungen der Gruppe Dorfbewohner-Handel."
---

# Dorfbewohner-Handel { #villager-trading }

StockMarket stellt die Angebote der Dorfbewohner von Smaragden auf Geld um und berechnet ihre Preise aus den Märkten. Diese Seite behandelt die Einstellungen. Was Spieler sehen, steht auf der Spielerseite [Dorfbewohner-Handel](../../stockmarket/villager-trading.md).

## Wie die Preise entstehen { #how-the-prices-are-made }

- Ein Angebot wechselt zu Geld, wenn sein Item einen Markt hat. Fahrende Händler funktionieren genauso.
- **Ein Dorfbewohner kauft** zum Marktpreis mal **Dorfbewohner-Kaufmarge** (Standard 0.8).
- **Ein Dorfbewohner verkauft** zum Marktpreis mal **Dorfbewohner-Verkaufsmarge** (Standard 1.2).
- Die Preise werden im Abstand von **Preisaktualisierung (Minuten)** aktualisiert, standardmäßig alle 20 echten Minuten, also etwa einmal pro Minecraft-Tag.
- Dorfbewohner-Angebote platzieren nie Orders. Sie ändern keinen Marktpreis.
- Rabatte (Ruf, Held des Dorfes, geheilte Zombiedorfbewohner) gelten auch für Angebote in Geld, bis zu 20%.
- Angebote mit einem zusätzlichen Item, etwa ein verzaubertes Buch (Buch plus Smaragde), behalten das Item. Nur die Smaragde werden zu Geld.

Wenn du einen Markt erstellst, wechseln die passenden Dorfbewohner-Angebote bei der nächsten Aktualisierung zu Geld. Wenn du ihn löschst, gehen sie zurück zu Smaragden.

## Items ohne Markt { #items-without-a-market }

Standardmäßig behalten Angebote für Items ohne Markt ihre Smaragde. Zwei Einstellungen ändern das:

| Einstellung | Wirkung |
|---|---|
| **Smaragde bei nicht gelisteten Items ersetzen** | Diese Angebote werden ebenfalls in Geld bezahlt: die Anzahl der Smaragde mal den Marktpreis von Smaragd, ohne Marge. Braucht einen Smaragd-Markt. Der Smaragdpreis wird auf zwei gültige Ziffern gerundet, etwa auf 12.00, damit sich die Preise nicht bei jeder kleinen Bewegung ändern. |
| **Preset-Preise für Dorfbewohner verwenden** | Nur zusammen mit der Einstellung darüber. Diese Angebote verwenden stattdessen den Preis aus der [Voreinstellung](presets.md) des Items, auch wenn es keinen Markt hat. Items ohne Preis in einer Voreinstellung fallen auf den Smaragdpreis zurück. |

Beide wirken, sobald ein Spieler das nächste Mal die Angebote eines Dorfbewohners öffnet.

## Abschalten { #turning-it-off }

Schalte **Dorfbewohner-Handel aktiviert** in den [Mod-Einstellungen](mod-settings.md#villager-trading) aus. Jeder Dorfbewohner bekommt seine ursprünglichen Smaragd-Angebote zurück, sobald ein Spieler das nächste Mal seine Angebote öffnet. Teilweise aufgebrauchte Angebote bleiben aufgebraucht.

## Die Datendatei { #the-data-file }

Die ursprünglichen Smaragd-Angebote werden in `<world>/data/StockMarket/villager_trades.nbt` gespeichert. Sie werden gebraucht, um die Angebote wiederherzustellen. Jeder Server hat seine eigene Datei, auch jeder Slave. Sie wird bei jedem Autosave gespeichert, wenn sie sich geändert hat.

## In einem Netzwerk { #on-a-network }

Die Einstellungen des Masters gelten für alle Server. Der Master schickt seine Preistabelle an jeden Slave. Wenn du die Funktion auf dem Master einschaltest, ist sie also überall an. Änderungen in der Gruppe **Dorfbewohner-Handel** erreichen die Slaves sofort.

## Verwandte Seiten { #related-pages }

- [Mod-Einstellungen](mod-settings.md#villager-trading): jede Dorfbewohner-Einstellung mit ihrem Bereich.
- [Markt-Voreinstellungen](presets.md): die Preise für Items ohne Markt.
- [Dorfbewohner-Handel](../../stockmarket/villager-trading.md): die Sicht der Spieler.
