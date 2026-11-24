---
title: "Glossar"
description: "Kurze Erklärungen der Bank- und Marktbegriffe auf dieser Website, von Bankkonto bis virtuelles Orderbuch."
---

# Glossar { #glossary }

Kurze Erklärungen der Begriffe, die diese Website verwendet. Jeder Eintrag verlinkt auf die Seite, die ihn ausführlich erklärt.

## Bankbegriffe { #bank-words }

### Bankkonto { #bank-account }

Verwahrt dein Geld und deine Items. Du bekommst ein persönliches Konto, wenn du zum ersten Mal auf den Server kommst. Du kannst auch gemeinsame Konten eröffnen und anderen Spielern Rechte darauf geben. Ein Unternehmen hat ein eigenes Konto. Siehe [Bankkonten](banksystem/bank-accounts.md).

### Kontorechte { #account-rights }

Was ein Spieler mit einem Konto tun darf: **Erlaubt einzuzahlen**, **Erlaubt abzuheben** und **Erlaubt zu verwalten** (Benutzer hinzufügen, Rechte ändern). Um mit einem Konto zu handeln, brauchst du sowohl das Recht zum Einzahlen als auch das Recht zum Abheben.

### Itembank { #item-bank }

Eine Zeile in deinem Konto für ein Item, zum Beispiel für dein Eisen oder dein Geld. Sie zeigt, wie viel du von diesem Item besitzt. **Leere Banken entfernen** im Bank Terminal räumt die Zeilen auf, in denen nichts ist.

### Bankfähiges Item { #bankable-item }

Ein Item, das in der Bank erlaubt ist. Standardmäßig sind das Geld, Eisenbarren, Goldbarren, Diamanten, Smaragde, Kohle und jedes Item mit einem Markt. Der Server-Admin kann weitere erlauben.

### Reservierter Betrag { #locked-balance }

Geld oder Items auf deinem Konto, die eine offene Order reserviert hat. Du kannst sie nicht ausgeben oder abheben, bis die Order ausgeführt ist oder du sie stornierst. Siehe [Grundlagen des Handels](stockmarket/trading.md#where-the-money-and-items-come-from).

### Eingefrorenes Konto { #frozen-account }

Ein Konto, das ein Admin gesperrt hat. Es kann nicht handeln, bis der Admin es wieder auftaut.

### Geld { #money }

Die Währung der Bank, angezeigt in Dollar und Cent. In der Bank ist es eine Zahl. In der Hand sind es Banknoten und Münzen, die der **Geldautomat** ausgibt. Siehe [Geld und der Geldautomat](banksystem/money.md).

### Unternehmen { #company }

Eine Gruppe mit eigenem Bankkonto, eigenen Mitarbeitern und eigenen Aktien. Siehe [Ein Unternehmen gründen und führen](banksystem/companies.md).

### Aktie { #share }

Ein Item **Unternehmensaktie**, das für einen Teil eines Unternehmens steht. Aktien können einen eigenen Markt haben. Siehe [Aktien und die Aktien-Prägestation](banksystem/shares.md).

### Angebot { #supply }

Wie viele Aktien eines Unternehmens es gibt, verglichen mit der Höchstzahl, die es ausgeben darf.

### Dividende { #dividend }

Geld, das ein Unternehmen an die Spieler zahlt, die seine Aktien halten. Siehe [Auszahlungen und Dividenden](banksystem/payouts.md).

## Marktbegriffe { #market-words }

### Markt { #market }

Der Ort, an dem ein Item gegen Geld gehandelt wird. Jedes Item hat höchstens einen Markt. Nur Admins erstellen Märkte, außer für Unternehmensaktien. Siehe [Grundlagen des Handels](stockmarket/trading.md).

### Order { #order }

Dein Auftrag, eine Menge eines Items zu kaufen oder zu verkaufen. Der Markt führt ihn mit Orders anderer Spieler oder von Bots zusammen.

### Market-Order { #market-order }

Eine Order, die sofort zu den besten angebotenen Preisen handelt. Du wählst die Menge, nicht den Preis.

### Limit-Order { #limit-order }

Eine Order mit deinem eigenen Preis. Sie handelt nur zu diesem Preis oder einem besseren und wartet bis dahin im Orderbuch.

### Orderbuch { #order-book }

Die Liste aller Limit-Orders, die warten: Kauforders unter dem aktuellen Preis, Verkaufsorders darüber. Der Handelsbildschirm zeigt es am rechten Rand des Charts. Siehe [Preischart und Orderbuch](stockmarket/price-chart.md).

### Spread { #spread }

Der Abstand zwischen der höchsten Kauforder und der niedrigsten Verkaufsorder. Ein kleiner Spread bedeutet, dass du wenig verlierst, wenn du kaufst und gleich wieder verkaufst.

### Volumen { #volume }

Eine Menge an Items: entweder wartend im Orderbuch oder gehandelt in einer Zeitspanne.

### Liquidität { #liquidity }

Wie viel Volumen nahe am aktuellen Preis wartet. Auf einem liquiden Markt bewegt eine große Order den Preis kaum. Auf einem Markt mit wenig Liquidität kann sie den Preis stark bewegen.

### Sweep { #sweep }

Das passiert, wenn eine große Market-Order die Orders zum besten Preis aufbraucht und zu immer schlechteren Preisen weiter ausgeführt wird. Der Preis springt, und dein Durchschnittspreis ist schlechter als der Preis, den du gesehen hast. Siehe [Grundlagen des Handels](stockmarket/trading.md#market-order-trade-now).

### Kerze { #candle }

Ein Balken im Preischart. Er zeigt den Preis zu Beginn (Eröffnung), den höchsten und den niedrigsten Preis und den Preis am Ende (Schluss) einer Zeitspanne.

### Zeitrahmen { #timeframe }

Die Zeitspanne einer Kerze, zum Beispiel eine Minute oder eine Stunde. Du wechselst ihn mit den Knöpfen am Chart.

### Modus Item / Item { #item-item-mode }

Ein Item direkt gegen ein anderes handeln, zum Beispiel Eisen gegen Diamanten, ohne selbst mit Geld umzugehen. Siehe [Item gegen Item handeln](stockmarket/pair-trading.md).

### Handelszeiten { #trading-hours }

Die Zeiten, in denen ein Markt geöffnet ist. Außerhalb davon kannst du keine neuen Orders platzieren, und deine offenen Orders warten, bis der Markt öffnet. Siehe [Wenn ein Markt geschlossen ist](stockmarket/trading.md#when-a-market-is-closed).

### Wartung { #maintenance }

Eine Pause auf einem Markt, die ein Admin einlegt. Offene Orders darauf werden storniert und erstattet.

### Handels-Cooldown { #trade-cooldown }

Eine kurze Wartezeit nach jeder angenommenen Order, bevor du die nächste platzieren kannst. Standardmäßig eine halbe Sekunde.

### Maximale Ordergröße { #max-order-size }

Die größte Menge an Items, die eine Order auf einem Markt kaufen oder verkaufen darf. Teile größere Geschäfte auf mehrere Orders auf.

## Serverbegriffe { #server-words }

Diese Begriffe kommen auf den Seiten unter [Server-Admin](admin/index.md) vor.

### Häufigkeit { #abundance }

Eine Markteinstellung, die angibt, wie verbreitet ein Item ist. Eine höhere Häufigkeit gibt dem Markt mehr Volumen und eine größere voreingestellte max. Ordergröße.

### Virtuelles Orderbuch { #virtual-order-book }

Orders, die Markt-Plugins hinzufügen, nicht Spieler. Sie geben einem Markt Volumen, sodass du handeln kannst, auch wenn kein anderer Spieler online ist. Siehe [Einen Marktstil wählen](admin/stockmarket/setup-use-cases.md).

### Plugin { #plugin }

Eine Erweiterung, die auf Märkten läuft: Sie fügt Volumen hinzu, bewegt den Preis, handelt als Bot oder reagiert auf News. Siehe [Plugins](admin/stockmarket/plugins/index.md).

### Voreinstellung { #preset }

Eine Vorlage für neue Märkte mit Startpreis, Häufigkeit und weiteren Einstellungen. Siehe [Voreinstellungen](admin/stockmarket/presets.md).

### Master und Slave { #master-and-slave }

Wenn mehrere Server eine Wirtschaft teilen, verwaltet der **master** alle Bankkonten und Märkte. Die **slaves** geben jede Bank- und Marktaktion an ihn weiter. Siehe [Mehrere Server, eine Wirtschaft](admin/multi-server.md).
