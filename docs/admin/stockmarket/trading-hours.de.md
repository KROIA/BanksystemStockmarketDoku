---
title: "Handelszeiten"
description: "Öffnungszeiten pro Markt festlegen, die verwendete Uhr, und der Unterschied zwischen geschlossen und Wartung."
---

# Handelszeiten { #trading-hours }

Jeder Markt kann tägliche Handelszeiten haben, wie eine echte Börse. Außerhalb davon ist der Markt **geschlossen**: Niemand kann Orders platzieren, und der Preis steht still, bis er wieder öffnet. Standardmäßig ist jeder Markt rund um die Uhr offen.

## Die Zeiten festlegen { #setting-the-hours }

1. Führe `/stockmarket manage` aus, wähle einen Markt und klicke auf **Markt-Einstellungen**.
2. Gib in der Zeile **Handelszeiten** die Öffnungs- und die Schließzeit als `HH:MM` ein.
3. Klicke auf **Anwenden**, oder auf **Auf alle anwenden**, um allen Märkten dieselben Zeiten zu geben.

Die Regeln für die Zeiten:

- `08:00`–`18:00` ist von 08:00 bis 17:59 offen.
- Liegt die Öffnungszeit nach der Schließzeit, läuft die Zeit über Mitternacht: `22:00`–`06:00` ist nachts offen.
- `00:00`–`24:00` bedeutet immer offen. Jedes andere Paar gleicher Zeiten ist ungültig.
- Eine ungültige Zeit färbt das Feld rot und zeigt *Ungültige Zeit (HH:MM, 00:00-24:00)*.

**Auf alle anwenden** fragt vorher nach, kopiert dann nur die Zeiten auf alle Märkte und meldet, wie viele es geändert hat.

Unter der Zeile zeigt das Fenster die echte Uhrzeit des Servers, seine Spielzeit und welcher von beiden die Märkte folgen. Prüfe das, wenn der Server in einer anderen Zeitzone steht als du.

## Welche Uhr { #which-clock }

Alle Märkte folgen einer Uhr. Du legst sie in den [Mod-Einstellungen](mod-settings.md) mit **Handelszeiten: Echtzeit** fest:

| Einstellung | Uhr |
|---|---|
| Aus (Standard) | Die Spielzeit in der Oberwelt des Masters. Tick 0 ist 06:00. `/time set` verstellt die Uhr. Ist der Tageszyklus angehalten, steht die Uhr still und mit ihr die Märkte. |
| An | Die echte Uhrzeit des Computers, auf dem der Master läuft, in dessen Zeitzone. |

Die Änderung wirkt sofort. Preiskerzen haben eine eigene Einstellung für ihre Uhr, siehe [Spielzeit-Kerzen](mod-settings.md#in-game-candles).

## Was „geschlossen“ bedeutet { #what-closed-means }

- **Keine neuen Orders** von Spielern, Bots oder Plugins. Spieler sehen *Markt geschlossen - außerhalb der Handelszeiten*.
- **Wartende Orders bleiben.** Spieler können sie weiterhin stornieren. Sobald der Markt wieder öffnet, können sie wieder ausgeführt werden.
- **Item-gegen-Item-Orders warten**, bis beide Märkte offen sind.
- **Der Preis ist eingefroren.** Das Chart zeigt flache Kerzen.
- **News zählen weiter.** Ein News-Ereignis kann den Basispreis des Markts ändern, während er geschlossen ist. Der Preis kann daher beim Öffnen springen.

Spieler sehen im Handelsfenster einen roten Hinweis **Markt geschlossen** und neben der Uhr die Handelszeiten. Wie das für Spieler aussieht, steht unter [Handel](../../stockmarket/trading.md).

## Märkte per Befehl öffnen und schließen { #opening-and-closing-by-command }

| Befehl | Was er bewirkt |
|---|---|
| `/stockmarket open "<market>"` | Öffnet den Markt sofort. |
| `/stockmarket close "<market>"` | Schließt den Markt sofort. |

`<market>` ist die Item-ID in Anführungszeichen, zum Beispiel `"minecraft:diamond"`, oder die Nummer des Markts. Teilen sich mehrere Märkte eine Item-ID, etwa verschiedene verzauberte Bücher, nimm die Nummer: Die Tab-Vervollständigung zeigt sie mit dem vollen Item-Namen.

Der Befehl gilt, bis die Zeiten des Markts ihn das nächste Mal öffnen oder schließen würden. Beispiel: Bei den Zeiten 08:00–18:00 hält `open` um 20:00 den Markt bis 08:00 offen. Auf einem immer offenen Markt gilt `close`, bis du `open` ausführst. Die Übersteuerung übersteht einen Neustart.

Die Befehle brauchen das StockMarket-Admin-Flag. Über die Konsole brauchen sie Operator-Level 2.

## Geschlossen oder Wartung? { #closed-or-maintenance }

Beides stoppt den Spielerhandel. Nutze die Handelszeiten für einen festen Zeitplan, und den [Wartungsmodus](markets.md#maintenance-mode), wenn du einen Markt änderst oder etwas schiefgeht.

| | Geschlossen | Wartung |
|---|---|---|
| Wartende Spieler-Orders | Bleiben | Storniert und erstattet |
| Bots und Plugins | Pausieren | Handeln weiter |
| Preis | Eingefroren | Bewegt sich weiter |
| Hinweis im Handelsfenster | **Markt geschlossen** | **In Wartung** |

Die Befehle zum Öffnen und Schließen beenden die Wartung nicht.

## In einem Netzwerk { #on-a-network }

Der Master entscheidet, nach seiner eigenen Uhr. Spieler auf Slaves sehen den Zustand und die Uhr des Masters. Du kannst die Zeiten auch auf einem Slave ändern und die Befehle dort nutzen; sie werden an den Master weitergegeben.

## Verwandte Seiten { #related-pages }

- [Märkte erstellen und verwalten](markets.md): die Markt-Einstellungen und der Wartungsmodus.
- [Mod-Einstellungen](mod-settings.md): die Einstellung für die Uhr.
- [Admin-Befehle](../commands.md): alle Befehle.
