---
title: "Spielerbefehle"
description: "Jeder BankSystem-Befehl, den ein normaler Spieler nutzen kann, für Geld, Bankkonten und Unternehmen."
---

# Spielerbefehle { #player-commands }

Diese Befehle funktionieren für jeden Spieler. Befehle für Admins stehen auf der Seite [Admin-Befehle](../admin/commands.md).

Setze Namen mit Leerzeichen in Anführungszeichen, zum Beispiel `/company info "Iron Works"`. Drücke beim Tippen ++tab++, um Spieler- und Unternehmensnamen zu vervollständigen.

## Geld { #money }

| Befehl | Was er tut |
|---|---|
| `/money` | Zeigt deinen Geld-Kontostand. |
| `/money send <player> <amount>` | Sendet Geld von deinem persönlichen Konto auf das persönliche Konto des Spielers. |
| `/money circulation` | Zeigt, wie viel Geld alle Spieler zusammen haben. |

Siehe [Geld und Geldautomat](money.md).

## Bankkonten { #bank-accounts }

| Befehl | Was er tut |
|---|---|
| `/bank` | Zeigt die Kontostände deines persönlichen Kontos, Geld und Items. |
| `/bank manage` | Öffnet das Verwaltungsfenster deines persönlichen Kontos. |
| `/bank manage <name>` | Öffnet das Verwaltungsfenster eines anderen Kontos, auf das du Zugriff hast. |
| `/bank create <name>` | Eröffnet ein neues Bankkonto. Jeder Spieler kann standardmäßig 3 eröffnen. |

Siehe [Bankkonten](bank-accounts.md).

## Unternehmen { #companies }

| Befehl | Was er tut | Wer ihn nutzen kann |
|---|---|---|
| `/company create "<name>" <max supply>` | Gründet ein Unternehmen mit eigenem Bankkonto. Die maximale Ausgabe (1 bis 1'000'000'000) lässt sich später nicht ändern. | Alle |
| `/company info "<name>"` | Zeigt die Gründer des Unternehmens, die maximale Ausgabe, die ausgegebenen Aktien und die Beschreibung. | Alle |
| `/company manage "<name>"` | Öffnet das Fenster Unternehmensverwaltung. | Verwalter des Unternehmens |
| `/company shares acknowledge "<name>"` | Bestätigt die Anzahl der Aktien, nachdem mehr Aktien aufgetaucht sind, als geprägt wurden, damit wieder Dividenden laufen. | Verwalter und Gründer |

Siehe [Ein Unternehmen gründen und führen](companies.md) und [Auszahlungen und Dividenden](payouts.md#when-a-payout-fails).

## StockMarket { #stockmarket }

StockMarket hat einen Befehl für Spieler: `/stockmarket news` öffnet die [Markt-News](../stockmarket/newspaper.md).

## Verwandte Seiten { #related-pages }

- [Bankkonten](bank-accounts.md): was `/bank` verwaltet.
- [Ein Unternehmen gründen und führen](companies.md): die `/company`-Befehle im Zusammenhang.
- [Admin-Befehle](../admin/commands.md): Befehle für Server-Admins.
