---
title: "Platzhalter"
description: "Preise, Kontostände und Ranglisten in TAB oder Placeholder API anzeigen, für beide Mods."
---

# Platzhalter { #placeholders }

Beide Mods bieten Platzhalter an: kurze Codes, die andere Mods durch Live-Werte ersetzen. Setze sie in eine Tab-Liste, ein Scoreboard oder ein Chatformat, um den Kontostand eines Spielers, die reichsten Spieler oder den Preis von Diamanten anzuzeigen.

## Was du brauchst { #what-you-need }

Installiere eine dieser Mods auf dem Server, siehe [Installation und Updates](install.md#optional-mods):

| Mod | Loader | So sieht ein Platzhalter aus |
|---|---|---|
| TAB | Fabric, NeoForge | `%banksystem_balance%`, `%stockmarket_price_diamond%` |
| Placeholder API | Fabric | `%banksystem:balance%`, `%stockmarket:price_diamond%` |

Das ist alles. Beide Mods registrieren ihre Platzhalter von selbst. Spieler brauchen weder TAB noch Placeholder API. Im Einzelspieler legst du die Mod in den eigenen `mods`-Ordner des Spiels.

!!! note "TAB 5.5.0 im Einzelspieler"
    Mit TAB 5.5.0 trennt dich das Öffnen einer zweiten Einzelspielerwelt in derselben Spielsitzung mit *An objective with the name TAB-PlayerList already exists*. Das ist ein Problem von TAB. Starte das Spiel zwischen zwei Welten neu. Server sind nicht betroffen.

Die Tabellen unten verwenden die Form von TAB. Für Placeholder API schreibst du `:` statt des ersten `_`.

## Formatierte und rohe Werte { #formatted-and-raw-values }

Jeder Platzhalter mit einer Zahl hat eine Variante mit `_raw`:

- `%banksystem_balance%` zeigt `$1'234.56`: Tausendertrennzeichen, zwei Nachkommastellen, Währungssymbol.
- `%banksystem_balance_raw%` zeigt `1234.56`: eine reine Zahl für Bedingungen und Berechnungen in anderen Mods.

Das Geldformat ist die Einstellung **Geldformat** von BankSystem (Standard `$%s`). Die Preise von StockMarket verwenden es auch, also sieht alles Geld gleich aus.

## Platzhalter von BankSystem { #banksystem-placeholders }

**Pro Spieler**, für den Spieler, der den Text sieht:

| Platzhalter | Beispiel | Zeigt |
|---|---|---|
| `%banksystem_balance%` | `$1'234.56` | Verfügbares Geld auf dem persönlichen Konto. |
| `%banksystem_locked%` | `$100.00` | Geld, das in offenen Orders reserviert ist. |
| `%banksystem_total%` | `$1'334.56` | Verfügbar plus reserviert. |
| `%banksystem_account_number%` | `12` | Die Nummer des persönlichen Kontos. |
| `%banksystem_rank%` | `3` | Platz in der Bestenliste der reichsten Spieler. |

**Für den ganzen Server:**

| Platzhalter | Beispiel | Zeigt |
|---|---|---|
| `%banksystem_circulation%` | `$1'250'000.00` | Alles Geld auf allen Konten, reserviertes Geld eingeschlossen. |
| `%banksystem_circulation_locked%` | `$20'000.00` | Alles reservierte Geld. |
| `%banksystem_account_count%` | `57` | Anzahl der Bankkonten. |
| `%banksystem_player_count%` | `42` | Anzahl der Spieler mit einem persönlichen Konto. |
| `%banksystem_average_balance%` | `$29'761.90` | Durchschnittliches Geld pro persönlichem Konto. |
| `%banksystem_top_1_name%` | `Steve` | Name des reichsten Spielers. |
| `%banksystem_top_1_balance%` | `$250'000.00` | Sein Geld. |

Die Bestenliste ordnet persönliche Konten nach verfügbarem plus reserviertem Geld. Ersetze `1` durch einen beliebigen Platz bis **Größe der Bestenliste** (Standard 10). Leere Plätze zeigen keinen Namen und einen Kontostand von null.

## Platzhalter von StockMarket { #stockmarket-placeholders }

**Pro Markt.** Ersetze `diamond` durch den Namen des Markts, siehe unten.

| Platzhalter | Beispiel | Zeigt |
|---|---|---|
| `%stockmarket_price_diamond%` | `$1'234.56` | Aktueller Preis. |
| `%stockmarket_change_diamond%` | `+3.21%` | Preisänderung in den letzten 24 Stunden. `0` ohne Preisverlauf. |
| `%stockmarket_volume_diamond%` | `12'500.00` | In den letzten 24 Stunden gehandelte Items. |

**Pro Spieler:**

| Platzhalter | Beispiel | Zeigt |
|---|---|---|
| `%stockmarket_open_orders%` | `3` | Offene Orders auf allen Märkten. |
| `%stockmarket_portfolio%` | `$8'420.00` | Marktwert der Items auf dem persönlichen Konto. Geld zählt nicht; Items ohne Markt zählen als null. |

### Marktnamen { #market-names }

Der Name kommt von der Item-ID:

| Item | Name |
|---|---|
| `minecraft:diamond` | `diamond` |
| `create:brass_ingot` | `create_brass_ingot` |
| Ein verzaubertes Buch | `enchanted_book_` plus ein Code aus 6 Zeichen, zum Beispiel `enchanted_book_3fa91c` |

Der Teil `minecraft:` fällt weg; andere Mod-Namen bleiben vorne stehen. Alles außer Buchstaben, Ziffern und `_` wird zu `_`. Items mit zusätzlichen Daten, etwa verzauberte Bücher und Tränke, bekommen einen Code für diese Daten. Dieser Code kann sich nach einem Minecraft-Update ändern. Prüfe diese Platzhalter also nach einem Update.

Wenn zwei Items denselben Namen bekommen, erhält nur eines davon Platzhalter. Das Server-Log nennt beide.

## Wie aktuell die Werte sind { #how-fresh-the-values-are }

Die Werte werden im Hintergrund aktualisiert, sie können also etwas hinterherhinken:

| Werte | Aktualisiert alle |
|---|---|
| BankSystem, pro Spieler | **Aktualisierung Spieler-Platzhalter (ms)**, Standard 1 Sekunde. `rank` verwendet die Server-Rate unten. |
| BankSystem, ganzer Server | **Aktualisierung Server-Platzhalter (ms)**, Standard 30 Sekunden |
| StockMarket, alle | 2 Sekunden |

Die Einstellungen von BankSystem stehen im Abschnitt **Integrationen** der [Mod-Einstellungen](banksystem/settings.md#integrations).

## In einem Netzwerk { #on-a-network }

Der Master berechnet alle Werte. Die Slaves holen sie sich, also sehen die Spieler überall dieselben Zahlen.

- Auf einem Slave, dem der Master nicht [vertraut](multi-server.md#trusted-slaves), bleiben alle Platzhalter von BankSystem mit Kontodaten und die Spieler-Platzhalter von StockMarket leer. Marktpreise funktionieren weiterhin.
- Solange ein Slave keine Verbindung hat, zeigt er die letzten Werte, die er bekommen hat.
- Ein Slave lässt Märkte für Items weg, die bei ihm nicht installiert sind.
- BankSystem: Jeder Server verwendet die Platzhalter-Einstellungen aus seiner eigenen `settings.json` (an oder aus, Aktualisierungsraten, Listengröße, Geldformat). Um sie auf einem Slave zu ändern, stoppst du ihn und bearbeitest seine Datei. Der Bildschirm Mod Settings ändert nur die Datei des Masters.
- StockMarket: Wenn du die Platzhalter auf dem Master ausschaltest, sind sie auch auf den Slaves aus.

## Platzhalter ausschalten { #turning-placeholders-off }

Jede Mod hat ihren eigenen Schalter, und beide brauchen einen Neustart:

- BankSystem: **Platzhalter aktiviert** in den [Mod-Einstellungen](banksystem/settings.md#integrations).
- StockMarket: **Platzhalter (TAB / Placeholder API)** in den [Mod-Einstellungen von StockMarket](stockmarket/mod-settings.md).

## Verwandte Seiten { #related-pages }

- [Discord-Feed](discord.md): Ereignisse an Discord senden.
- [Installation und Updates](install.md): TAB oder Placeholder API installieren.
- [Master- und Slave-Server](multi-server.md): einem Slave vertrauen.
