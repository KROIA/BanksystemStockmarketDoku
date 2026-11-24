---
title: "Unternehmen und Aktien"
description: "Limits für Unternehmen, Aktiensymbole, Aktien-Alarme und Admin-Aktionen für Firmenkonten und Märkte."
---

# Unternehmen und Aktien { #companies-and-shares }

Spieler gründen und führen ihre Unternehmen selbst, siehe [Ein Unternehmen gründen und führen](../../banksystem/companies.md). Diese Seite behandelt, was du als Admin tun kannst. Du brauchst das BankSystem-Admin-Flag, siehe [Admins und Berechtigungen](../permissions.md).

## Limits { #limits }

**Max. Firmen pro Spieler** in den [Mod Settings](settings.md#player) legt fest, wie viele Unternehmen ein Spieler gründen darf (Standard 3). Ein Unternehmen belegt außerdem eines der Bankkonten des Spielers. **Max. Bankkonten pro Spieler** muss also Platz dafür lassen.

## Jedes Unternehmen verwalten { #managing-any-company }

`/company manage "<name>"` öffnet dir das Verwaltungsfenster jedes Unternehmens, als hättest du das Recht **Verwalten** auf seinem Konto. Du kannst Mitarbeiter, Auszahlungen, das Aktien-Design und die Beschreibung bearbeiten und den Markt des Unternehmens pausieren oder fortsetzen.

Manche Aktionen bleiben den Gründern vorbehalten, auch für Admins:

- **Gründerrolle übertragen** und **Unternehmen auflösen**
- **Markt schließen**

Das Geld des Unternehmens liegt auf einem normalen Bankkonto. Öffne es wie jedes andere, siehe [Konten verwalten](accounts.md).

## Aktien-Integrität { #share-integrity }

Jedes Unternehmen weiß, wie viele Aktien es geprägt hat. Der Master-Server vergleicht diese Zahl mit den Aktien in allen Bankkonten. Liegen mehr Aktien in den Banken, als je geprägt wurden, dann wurden irgendwo Aktien kopiert.

Wenn das passiert, entfernt BankSystem nichts. Stattdessen:

- Auf dem Konto des Unternehmens wird eine Markierung **Aktienüberschuss** gesetzt. Sie zeigt die geprägte und die eingelagerte Anzahl, die Aktien-Einzahlungen seit der letzten Übereinstimmung der Zahlen und pro Spieler, wie viele Aktien er herausgenommen oder eingezahlt hat. Der letzte Teil ist ein Hinweis, kein Beweis: Aktien können als Items den Besitzer wechseln, ohne dass etwas aufgezeichnet wird.
- Die **Dividenden des Unternehmens werden pausiert**. **Dividende auszahlen** und Dividendenpläne werden mit dem Status *Pausiert* übersprungen. Normale Auszahlungen laufen weiter.

Die Prüfung läuft nach jeder Aktien-Einzahlung und einmal am Tag. Pro Unternehmen gibt es nur einen offenen Alarm. Ein neuer kommt nur, wenn der Überschuss wächst.

Wenn du die Sache untersucht hast, akzeptiere die aktuellen Zahlen:

```text
/company shares acknowledge "<name>"
```

Damit gilt die Markierung als geprüft, und die Dividenden laufen wieder. Die eigenen Admins des Unternehmens (Gründer und Spieler mit **Verwalten**) können den Befehl für ihr Unternehmen ebenfalls ausführen. Wenn die überzähligen Aktien vernichtet werden und die Zahlen wieder übereinstimmen, schließt sich der Alarm, und die Dividenden laufen von selbst wieder.

Aktien, die endgültig verschwinden, senken die geprägte Anzahl: Aktien in einem gelöschten Konto oder einer geschlossenen Bank und Aktien, die du im [Kontofenster](accounts.md#what-you-can-change) entfernst.

!!! warning "Aktien aus /give oder dem Kreativinventar"
    Geprägte Aktien aus `/give` oder dem Kreativinventar setzen sofort eine Markierung **Aktie erzeugt**, mit dem Namen des Spielers. Gib Aktien nur über eine Aktien-Prägestation aus.

Wie Markierungen bei dir ankommen, steht in [Alarme und Verdachtsmarkierungen](../audit/alerts.md).

## Aktiensymbole { #share-symbols }

Die Symbole, die Spieler im Editor **Aktien-Design** wählen können, sind PNG-Bilder auf dem Master-Server. BankSystem bringt 45 mit. Du kannst eigene hinzufügen, bis zu 256 insgesamt.

So fügst du ein Symbol hinzu:

1. Erstelle ein quadratisches PNG, 64 × 64 Pixel oder kleiner, mit einer Zweierpotenz als Größe (16, 32 oder 64) und höchstens 128 KB.
2. Lege es auf dem Master-Server in `<world>/data/BankSystem/share_symbols/inbox/` ab. Der Dateiname ist die Symbol-ID: Kleinbuchstaben, Ziffern und `_`, höchstens 32 Zeichen, zum Beispiel `rocket.png`.
3. Führe `/banksystem symbols add rocket` aus.

Eine vorhandene ID wird ersetzt. Das neue Symbol erreicht sofort alle Spieler und Slave-Server.

| Befehl | Was er bewirkt |
|---|---|
| `/banksystem symbols list` | Listet alle Symbole auf. |
| `/banksystem symbols add <id>` | Fügt ein Symbol aus dem Inbox-Ordner hinzu oder ersetzt es. |
| `/banksystem symbols remove <id>` | Entfernt ein Symbol. |
| `/banksystem symbols reload` | Liest die Dateien der vorhandenen Symbole neu ein, nachdem du eines von Hand ersetzt hast. Neue Dateien werden ignoriert: Füge sie mit `/banksystem symbols add` hinzu. |

Alle vier Befehle funktionieren nur auf dem Master-Server.

## Verwandte Seiten { #related-pages }

- [Ein Unternehmen gründen und führen](../../banksystem/companies.md): die Sicht der Spieler.
- [Dein Unternehmen an der Börse](../../banksystem/company-market.md): einen Aktienmarkt pausieren und schließen.
- [Alarme und Verdachtsmarkierungen](../audit/alerts.md): alle Markierungen in einer Tabelle.
