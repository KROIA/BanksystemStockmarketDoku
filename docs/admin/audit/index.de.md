---
title: "Audit und Anti-Cheat"
description: "Was beide Mods über Geld, Items und Handel aufzeichnen, wo es gespeichert wird und wie du es liest."
---

# Audit und Anti-Cheat { #audit-and-anti-cheat }

Beide Mods zeichnen jede Änderung eines Kontostands und jeden Handel auf. Wenn etwas schiefgeht, zum Beispiel bei einem Duplizier-Exploit oder gestohlenem Geld, zeigen diese Aufzeichnungen, wer was gewonnen hat und wie. Diese Seite sagt, was aufgezeichnet wird und wo du es liest.

Alle Aufzeichnungen schreibt der Master-Server. In einem Netzwerk zeichnet er auch auf, was auf den Slave-Servern passiert, zusammen mit dem Server, von dem es kam.

## Was aufgezeichnet wird { #what-is-recorded }

| Aufzeichnung | Enthält | Lesen mit |
|---|---|---|
| **Transaktionsbuch** | Jede Änderung des Kontostands jedes Kontos: Einzahlungen, Abhebungen, Überweisungen, Auszahlungen, Dividenden, Handel, Admin-Änderungen, Einfrieren. Jeder Eintrag enthält die Zeit, den Betrag, wer ihn verursacht hat und den Kontostand danach. | Das [Audit-Fenster](investigating.md#the-audit-screen) |
| **Kontoverlauf** | Die Kontostände aller Konten über die Zeit. | Das [Kontostandsdiagramm](investigating.md#balance-history-with-flags) und der [Serververlauf](investigating.md#the-whole-server) |
| **Verdachtsmarkierungen** | Muster, die oft auf Cheating hindeuten, etwa große Abhebungen oder plötzlicher Reichtum. | [Chat-Alarme](alerts.md), Marker im Kontostandsdiagramm, das Audit-Log |
| **Audit-Log** | Jede Admin-Aktion und jede Markierung, eine einfache Textdatei pro Tag. | Jeder Texteditor, siehe [Täglicher Bericht und Berichte](reports.md) |
| **Täglicher Bericht** | Eine Zusammenfassung jedes Tages: Geldmenge, größte Gewinner, Markierungen, Admin-Aktionen. | Jeder Markdown-Betrachter, siehe [Täglicher Bericht und Berichte](reports.md) |
| **Banknotenfluss** | Banknoten, die außerhalb der Bank in die Welt kommen oder sie verlassen, zum Beispiel über `/give` oder das Kreativinventar. | Das [Audit Tool](audit-tool.md) |
| **Handelsalarme und Order-Herkunft** | Die Alarme von StockMarket und auf welchem Server jede Order platziert wurde. | Das Server-Log und das [Audit Tool](audit-tool.md) |

Die Aufzeichnungen liegen in SQLite-Datenbanken und Textdateien im Weltordner, siehe [Datendateien und Backups](../backups.md). Sie werden nie automatisch aufgeräumt. Nur alter Kontoverlauf wird ausgedünnt.

## Wo du anfängst { #where-to-start }

- **Ein Alarm ist eingegangen:** Lies in [Alarme und Verdachtsmarkierungen](alerts.md), was er bedeutet. Öffne dann das Konto, wie in [Im Spiel untersuchen](investigating.md) beschrieben.
- **Ein Spieler meldet fehlendes Geld:** Öffne sein Konto im [Audit-Fenster](investigating.md#the-audit-screen) und verfolge das Geld.
- **Ein großer Fall über mehrere Server:** Exportiere die Speicherstände und lade sie in das [Audit Tool](audit-tool.md).
- **Ein täglicher Blick auf die Wirtschaft:** Lies den [täglichen Bericht](reports.md#the-daily-digest).

!!! tip "Erst einfrieren, dann untersuchen"
    Während du ein Konto untersuchst, [friere es ein](../banksystem/accounts.md#freezing-an-account). Dann kann nichts hinein oder hinaus, und nichts geht verloren.

## Verwandte Seiten { #related-pages }

- [Alarme und Verdachtsmarkierungen](alerts.md): wovor beide Mods warnen.
- [Im Spiel untersuchen](investigating.md): das Audit-Fenster und die Kontostandsdiagramme.
- [Audit Tool](audit-tool.md): das Offline-Programm für große Fälle.
