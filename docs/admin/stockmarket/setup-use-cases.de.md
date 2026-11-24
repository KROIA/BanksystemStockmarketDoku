---
title: "Ein Markt-Setup wählen"
description: "Ein Markt mit Bots und virtuellem Orderbuch oder ein reiner Spielermarkt, mit den Vor- und Nachteilen beider Arten."
---

# Ein Markt-Setup wählen { #choosing-a-market-setup }

Ein Markt kann seine Orders von Bots und Spielern bekommen oder nur von Spielern. Du wählst das pro Markt, daher können beide Arten nebeneinander laufen: zum Beispiel Bots für häufige Items und ein reiner Spielermarkt für seltene.

## Bots und Spieler (der Standard) { #bots-and-players-the-default }

Jeder neue Markt startet mit dem **virtuellen Orderbuch**: Bot-Orders rund um den aktuellen Preis, die die [Preis-Plugins](plugins/index.md) aufrechterhalten. Spieler können jederzeit sofort kaufen und verkaufen, und der Preis bewegt sich mit dem Handel der Spieler plus ein wenig natürlicher Bewegung.

Du musst nichts einrichten: Erstelle die Märkte, und du bist fertig. Märkte aus den Standard-Voreinstellungen starten mit dem virtuellen Orderbuch und bekommen die Standard-Plugins.

**Gut für:** öffentliche Survival-Server, Server mit wenigen Spielern und Server, auf denen Spieler erwarten, dass ein Handel sofort durchgeht.

**Bedenke:** Die Preise entstehen zum Teil durch die Bots. Sie folgen dem, was Spieler tun, aber nicht nur dem.

## Nur Spieler { #players-only }

Der Markt hat keine Bot-Orders. Jeder Handel findet zwischen zwei Spielern statt, und der Preis bewegt sich nur, wenn sie handeln. Das kommt einer echten Börse am nächsten.

**Für neue Märkte** stellst du es in der Voreinstellung ein:

1. Führe `/stockmarket manage` aus und öffne den Tab **Voreinstellungen**.
2. Schalte für das Item **Virtuelles Orderbuch** aus und **Kein Plugin-Autosubscribe** ein.
3. Klicke auf **Änderungen speichern**. Märkte, die du daraus erstellst, starten jetzt ohne Bots.

Für einen einzelnen Markt kannst du auch auf dem Tab **Märkte erstellen** **Orderbuch aktiv** ausschalten.

**Für einen bestehenden Markt:**

1. Wähle den Markt auf dem Tab **Übersicht** und klicke auf **Markt-Einstellungen**.
2. Schalte **Virtuelles Orderbuch aktiv** aus und klicke auf **Anwenden**.
3. Wenn du möchtest, entferne den Markt unter **Plugins verwalten** aus seinen Plugins. Die Preis-Plugins lassen ihn ohnehin aus.

**Gut für:** Rollenspiel- und Wirtschaftsserver, Fraktionsserver, auf denen Knappheit zählt, und kleine Handelsgruppen.

**Bedenke:**

- Das Orderbuch ist leer, bis ein Spieler eine Limit-Order platziert.
- Ein neuer Markt hat keinen echten Preis, bis Spieler auf beiden Seiten handeln.
- Käufer und Verkäufer können weit auseinanderliegen. Market-Orders werden dann zu schlechten Preisen oder nur teilweise ausgeführt. Der Rest wird storniert und erstattet.
- Ohne Handel bewegt sich der Preis überhaupt nicht.
- Spieler, die Bot-Märkte gewohnt sind, können verwirrt sein. Sag ihnen, welche Märkte reine Spielermärkte sind.

## Unser Rat { #our-advice }

Starte überall mit Bots und Spielern. Sobald du eine aktive Spielerschaft hast, stelle einige wertvolle Items auf „nur Spieler“ um, dort, wo echte Preise mehr zählen als schneller Handel.

## Verwandte Seiten { #related-pages }

- [Märkte erstellen und verwalten](markets.md): die Markt-Einstellungen.
- [Markt-Voreinstellungen](presets.md): Einstellungen für neue Märkte.
- [Preis-Plugins](plugins/index.md): was die Bots tun.
