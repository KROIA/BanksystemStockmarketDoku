---
title: "Währungsintegration"
description: "Einen ExternalCurrencyProvider schreiben, damit deine Währungs-Mod in den Währungs-Verknüpfungen erscheint."
---

# Währungsintegration { #currency-integration }

Diese Seite ist für Autoren von Währungs-Mods. Mit einem Adapter können Spieler einen Bank-Slot von BankSystem an ein Konto in deiner Mod binden (siehe [Währungsbindungen](../../banksystem/currency-bindings.md)). Danach bewegen Einzahlungen, Abhebungen und Handel an der Börse auf diesem Slot Geld auf dem Konto deiner Mod. BankSystem bringt Adapter für Numismatics und Lightman's Currency mit; diese Seite zeigt, wie du einen eigenen schreibst.

Alle Typen liegen in `net.kroia.banksystem.api.currency`.

## Wie eine Bindung funktioniert { #how-a-binding-works }

- **Deine Mod hält den Kontostand.** Abfragen des Kontostands, Einzahlungen und Abhebungen auf dem gebundenen Slot gehen an dein Konto.
- **BankSystem behält den Rest:** Kontomitglieder, Rechte und den **reservierten** Kontostand (Geld, das für offene Orders zurückgehalten wird).
- **Reservieren bewegt Geld aus deinem Konto.** Eine Reservierung hebt den Betrag in ganzen Einheiten deiner Mod von deinem Konto ab (siehe [Einheiten](#units)), und BankSystem hält ihn in der Bindung. Beim Freigeben wird er wieder eingezahlt. Wird ein reservierter Betrag ausgegeben, zum Beispiel durch eine ausgeführte Order, sinkt nur der Zähler für reservierte Beträge in BankSystem: Deine Mod sieht keine zweite Abhebung.
- **Das Binden bewegt das Geld einmal.** Der freie Kontostand des Slots wandert auf dein Konto, wenn der Spieler den Slot bindet. Der reservierte Teil bleibt in BankSystem.
- **Ein Slot, ein Konto.** Jeder Bank-Slot lässt sich einzeln binden. Andere Slots desselben Kontos bleiben normal.

Schreib einen Adapter, wenn deine Mod Kontostände in Konten speichert, die Logouts und Neustarts überstehen. Besteht deine Währung nur aus Münzen im Inventar, brauchst du keinen: Spieler können die Münzen wie jedes andere Item in die Bank einzahlen.

## Die vier Typen { #the-four-types }

| Typ | Was er ist |
|---|---|
| `ExternalCurrencyProvider` | Der Einstiegspunkt deiner Mod. Eine Instanz, einmal registriert. Listet die bindbaren Konten eines Spielers auf und öffnet ein Konto über eine gespeicherte Referenz. |
| `ExternalAccount` | Ein kurzlebiges Handle auf ein Konto. BankSystem öffnet eines, wenn es eines braucht, und behält es nicht. |
| `ExternalAccountRef` | Der gespeicherte Verweis auf ein Konto: `providerId`, `accountKey`, `label`, `shared`. |
| `ProviderFeature` | Flags dafür, was dein Anbieter unterstützt. |

`ExternalAccountRef` ist ein Record. `providerId` und `accountKey` dürfen nicht leer sein, und kein Feld darf `null` sein; sonst wirft der Konstruktor eine Exception. `providerId` + `accountKey` kennzeichnen das Konto dauerhaft. `label` ist der Name, den die Kontoauswahl zeigt, und `shared` gibt an, ob in deiner Mod mehrere Spieler das Konto besitzen. BankSystem speichert und sendet die Referenz selbst; du legst sie nur an und liest sie.

## Regeln für jeden Adapter { #rules-for-every-adapter }

- **Nur auf dem Server-Thread.** BankSystem ruft jede Methode auf dem Server-Thread auf. Dein Adapter muss nicht threadsicher sein. Ändere den Zustand des Adapters nicht aus deinen eigenen Hintergrund-Threads.
- **Beträge sind Roh-Einheiten von BankSystem** (`long`). Rechne im Adapter in die Einheiten deiner Mod um. Siehe [Einheiten](#units).
- **Live lesen, nicht zwischenspeichern.** `getBalance()` wird bei jedem Lesezugriff aufgerufen und ist der freie Kontostand des Slots. Die eigenen Maschinen und Befehle deiner Mod ändern Kontostände an BankSystem vorbei, und BankSystem muss das sehen, zum Beispiel um zu prüfen, ob sich ein Spieler eine Order leisten kann. Der reservierte Kontostand ist nicht darin enthalten: Den hält BankSystem in der Bindung. Ist eine Abfrage in deiner Mod langsam, speichere in deiner Mod zwischen und aktualisiere diesen Zwischenspeicher bei jeder Änderung.
- **Wirf keine Exception bei erwarteten Fehlschlägen.** `deposit` und `withdraw` geben ohne Änderung `false` zurück, wenn das Geld nicht passt, nicht da ist oder deine Mod aus eigenen Gründen ablehnt.

## Einen Anbieter schreiben { #writing-a-provider }

### Name und Funktionen { #name-and-features }

```java
public final class MyMoneyProvider implements ExternalCurrencyProvider {
    public static final String PROVIDER_ID = "my_money";

    @Override public @NotNull String providerId() { return PROVIDER_ID; }

    @Override public boolean isAvailable() {
        return Platform.isModLoaded("my_money") && MyMoneyApi.isReady(); // cheap, no file or network access
    }

    @Override public @NotNull Set<ProviderFeature> features() {
        return EnumSet.of(ProviderFeature.PERSONAL_ACCOUNTS, ProviderFeature.SUFFICIENT_FUNDS_CHECK);
    }
    // listBindableAccounts and open follow below
}
```

`providerId()` wird mit jeder Bindung gespeichert. **Ändere sie nach einem Release nie**, sonst verliert jede bestehende Bindung ihr Konto. Nimm deine Mod-ID.

`isAvailable()` wird geprüft, bevor das Fenster Währungs-Verknüpfungen deinen Anbieter auflistet, und vor jeder Kontostandsoperation auf einem gebundenen Slot. Halte die Methode billig.

### Die Konten eines Spielers auflisten { #listing-a-players-accounts }

```java
@Override
public @NotNull List<ExternalAccountRef> listBindableAccounts(@NotNull UUID player) {
    List<ExternalAccountRef> out = new ArrayList<>();
    MyAccount personal = MyMoneyApi.getPersonalAccount(player);
    if (personal != null)
        out.add(new ExternalAccountRef(PROVIDER_ID, personal.uuid().toString(), personal.displayName(), false));
    for (MyAccount team : MyMoneyApi.getSharedAccountsForPlayer(player))
        out.add(new ExternalAccountRef(PROVIDER_ID, team.uuid().toString(), team.displayName(), true));
    return out; // personal first, then shared
}
```

BankSystem ruft sie auf, wenn ein Spieler die Kontoauswahl öffnet, und prüft beim Binden das gewählte Konto dagegen (BankSystem-Admins überspringen diese Prüfung). Gib aktuelle Ergebnisse zurück.

**Eine leere Liste ist eine Antwort**: Der Spieler darf keines deiner Konten binden. BankSystem ruft diese Methode auch beim Serverstart für die Verwalter jedes Bankkontos auf, das eine Bindung hat. Darf keiner von ihnen das gebundene Konto mehr binden, wird die Bindung **gesperrt**, und Admins bekommen einen Alarm. Ein Admin hebt die Sperre mit `/banksystem restorebinding` auf. Daher:

- Gib eine leere Liste nur zurück, wenn der Spieler wirklich nichts binden darf.
- Wenn du die vollständige Liste nicht liefern kannst (deine Mod ist nicht bereit, ein Fehler, nur ein Teil ließ sich lesen), **wirf** eine `RuntimeException`. Dann wird das Binden abgelehnt, die Kontoauswahl zeigt nichts, und die Prüfung beim Start lässt bestehende Bindungen in Ruhe.

### Ein Konto öffnen { #opening-an-account }

```java
@Override
public @Nullable ExternalAccount open(@NotNull ExternalAccountRef ref) {
    if (!PROVIDER_ID.equals(ref.providerId())) return null;
    try {
        MyAccount account = MyMoneyApi.getAccount(UUID.fromString(ref.accountKey()));
        return account == null ? null : new MyExternalAccount(ref, account);
    } catch (IllegalArgumentException e) {
        return null; // not a key of ours
    }
}
```

Gib `null` zurück, wenn das Konto gerade nicht erreichbar ist: gelöscht, nicht bereit oder ein Schlüssel, den du nicht kennst. BankSystem behandelt die Bindung dann als nicht verfügbar (siehe [Wenn deine Mod fehlt](#when-your-mod-is-missing)).

### Das Konto-Handle { #the-account-handle }

```java
final class MyExternalAccount implements ExternalAccount {
    private final ExternalAccountRef ref;
    private final MyAccount account;

    MyExternalAccount(ExternalAccountRef ref, MyAccount account) { this.ref = ref; this.account = account; }

    @Override public @NotNull ExternalAccountRef ref() { return ref; }
    @Override public long getBalance() { return account.getBalance(); }          // live, >= 0
    @Override public boolean deposit(long amount) {                              // false on overflow, no change
        return amount >= 0 && account.tryDeposit(amount);
    }
    @Override public boolean withdraw(long amount) {                             // false if not enough, no change
        return amount >= 0 && account.tryWithdraw(amount);
    }
    @Override public boolean canWithdraw(long amount) { return amount >= 0 && account.getBalance() >= amount; }
    @Override public boolean isSharedAccount() { return ref.shared(); }
    @Override public @NotNull Set<UUID> currentMembers() { return new HashSet<>(account.members()); } // a copy
    @Override public void syncMembership(@NotNull Set<UUID> withdrawers) { account.setMembers(withdrawers); }
}
```

Jede Methode geht direkt an deine Mod. `deposit` und `withdraw` müssen nach dem Alles-oder-nichts-Prinzip arbeiten.

### Einheiten { #units }

BankSystem speichert 100 Roh-Einheiten pro Item, Geld hat also zwei Nachkommastellen. Drei Methoden sagen BankSystem, wie deine Einheiten dazu passen:

| Methode | Standard | Bedeutung |
|---|---|---|
| `ExternalAccount.nativeScale()` | `1` | Roh-Einheiten pro kleinster Einheit deiner Mod. Speichert deine Mod nur ganze Münzen und ist eine Münze 100 Roh-Einheiten wert, gib `100` zurück. BankSystem schickt dann nur ganze Vielfache davon an `deposit` und `withdraw` und behält den Rest selbst in der Bindung, damit kein Bruchteil verloren geht. |
| `ExternalCurrencyProvider.getBaseCurrencyItemId()` | `null` | Die Item-ID deiner Basismünze, zum Beispiel `"my_money:coin"`. Nur ein Slot dieses Items lässt sich an deine Mod binden. `null` erlaubt jedes Item. |
| `ExternalCurrencyProvider.baseUnitsPerItem(ItemStack)` | `0` | Der Wert einer Münze in Roh-Einheiten, für jede Münze deiner Mod. Zahlt ein Spieler an einem Bank Terminal eine Münze mit einem Wert ungleich null ein, schreibt BankSystem Anzahl × Wert dem gebundenen Slot der Basismünze gut statt einer eigenen Bank für diese Münze. Für die Basismünze legt dieser Wert außerdem fest, wie viele Roh-Einheiten eine Münze des gebundenen Slots wert ist; `0` bedeutet 100. |

Lies die Münzwerte in `baseUnitsPerItem` aus der Konfiguration deiner Mod, wenn sie eine hat; schreib sie nicht fest in den Code. Gib `0` für beschädigte oder verzauberte Stacks zurück und für Items, die keine Münzen deiner Mod sind.

### Registrieren { #registering }

```java
// when your mod starts
if (Platform.isModLoaded("banksystem")) {
    BankSystemMod.getAPI().registerCurrencyProvider(new MyMoneyProvider());
}
```

Registrierst du dieselbe `providerId` erneut, ersetzt das den früheren Anbieter. `unregisterCurrencyProvider(providerId)` entfernt ihn wieder; ein normaler Adapter bleibt die ganze Spielsitzung lang registriert. Damit du keine harte Abhängigkeit von BankSystem bekommst, setz diesen Aufruf in eine Klasse, die nur geladen wird, wenn BankSystem vorhanden ist.

## Feature-Flags { #feature-flags }

Gib nur die Flags zurück, die dein Anbieter wirklich unterstützt.

| Flag | Bedeutung |
|---|---|
| `PERSONAL_ACCOUNTS` | Jeder Spieler hat ein persönliches Konto (oder kann eines anlegen). |
| `MULTI_ACCOUNT_PER_PLAYER` | `listBindableAccounts` kann mehr als ein Konto pro Spieler zurückgeben. |
| `SHARED_ACCOUNTS` | Deine Mod hat Konten mit mehreren Besitzern. |
| `MEMBERSHIP_SYNC` | Dein `syncMembership` ändert die Mitglieder in deiner Mod wirklich. |
| `SUFFICIENT_FUNDS_CHECK` | Dein `canWithdraw` ist exakt und hat keine Nebenwirkungen. |

Die Flags werden an das Fenster Währungs-Verknüpfungen geschickt. In dieser Version ändert BankSystem sein Verhalten nicht wegen ihnen, und es ruft `canWithdraw`, `isSharedAccount`, `currentMembers` und `syncMembership` nicht auf. Implementiere sie trotzdem wie beschrieben:

- `canWithdraw(amount)`: ob ein direkt danach aufgerufenes `withdraw(amount)` gelingen würde.
- `isSharedAccount()`: dasselbe wie `ref().shared()`.
- `currentMembers()`: eine Kopie der Spieler, die vom Konto ausgeben dürfen; bei einem persönlichen Konto der Besitzer.
- `syncMembership(withdrawers)`: ersetzt die Mitglieder, die ausgeben dürfen, durch die übergebene Menge: die Nutzer des gemeinsamen Bankkontos mit dem Recht zum Abheben. Wirf keine Exception; schreib Fehler ins Log und kehre zurück.

## Persönliche und gemeinsame Konten { #personal-and-shared-accounts }

Eine Bindung verbindet nur Konten derselben Art:

| Bankkonto | `ref.shared()` | Ergebnis |
|---|---|---|
| Persönlich | `false` | Erlaubt |
| Gemeinsam (jedes Konto, das nicht persönlich ist) | `true` | Erlaubt |
| Persönlich | `true` | Abgelehnt mit `FAILED_WRONG_INSTANCE_TYPE` |
| Gemeinsam | `false` | Abgelehnt mit `FAILED_WRONG_INSTANCE_TYPE` |

Setz `shared` also in jeder Referenz, die du zurückgibst, richtig.

Eine Bindung wird außerdem abgelehnt:

- mit `FAILED_WRONG_INSTANCE_TYPE`, wenn das Item des Bank-Slots nicht das Basiswährungs-Item deines Anbieters ist;
- mit `FAILED_INVALID_ITEM_ID`, wenn der Slot schon gebunden ist. Löse die Bindung zuerst;
- mit `FAILED_OVERFLOW`, wenn dein `deposit` den Wert `false` zurückgibt, während das Binden den freien Kontostand des Slots auf dein Konto bewegt. Es ändert sich nichts.

## Was Aufrufer sehen { #what-callers-see }

Andere Mods nutzen den gebundenen Slot über die normale [BankSystem-API](api.md). Deine Rückgabewerte werden zu einem `BankStatus`:

| Dein Adapter | `BankStatus` |
|---|---|
| `deposit` gibt `false` zurück | `FAILED_OVERFLOW`. Beim Freigeben: `FAILED_EXTERNAL_UNAVAILABLE`, und der Betrag bleibt reserviert, bis ein späteres Freigeben klappt. |
| `withdraw` gibt `false` zurück | `FAILED_NOT_ENOUGH_FUNDS` |
| `open` gibt `null` zurück, oder `isAvailable()` ist `false` | `FAILED_EXTERNAL_UNAVAILABLE` |

## Wenn deine Mod fehlt { #when-your-mod-is-missing }

Wenn deine Mod entfernt wurde oder nicht bereit ist, oder wenn ein Admin einen eingebauten Adapter in den Einstellungen des Servers unter Integrationen abgeschaltet hat:

- Abfragen des freien Kontostands des gebundenen Slots geben `0` zurück. Der reservierte Kontostand in BankSystem bleibt sichtbar.
- Änderungen schlagen mit `FAILED_EXTERNAL_UNAVAILABLE` fehl; auf keiner Seite ändert sich etwas.
- BankSystem schreibt eine Warnung pro gebundenem Slot ins Log, nicht eine pro Aufruf.
- Das Lösen der Bindung wird abgelehnt, solange der Slot noch reserviertes Geld oder einen Rest unter einer deiner Einheiten hält, weil das sonst verloren ginge.

Ist deine Mod wieder da, funktionieren die Bindungen wieder, solange `providerId()` und jeder `accountKey` noch zum selben Konto führen.

## Bindungen funktionsfähig halten { #keeping-bindings-working }

- **Lass `providerId()` gleich**, in jedem Release.
- **Lass jeden `accountKey` gleich**, solange das Konto existiert. Änderst du sein Format, erkenne das alte Format in `open` und übersetze es. Ein Versionspräfix im Schlüssel, zum Beispiel `v1:<uuid>`, macht das leichter.
- **Bindungen wandern nicht zwischen Welten.** Hat dasselbe Konto auf einem anderen Server einen anderen Schlüssel, binden die Spieler dort neu.
- **Das Fenster Währungs-Verknüpfungen aktualisiert sich nicht von selbst.** Nach einer Änderung in den eigenen Maschinen deiner Mod klicken die Spieler auf **Aktualisieren**. Serverseitige Lesezugriffe sind immer aktuell.

## In einem Netzwerk { #on-a-network }

Bindungen gibt es nur auf dem Master, und nur der Master ruft deinen Adapter auf. Ein Slave leitet jeden Bank-Aufruf an den Master weiter, auch die Aufrufe des Fensters Währungs-Verknüpfungen. Dein Adapter braucht keinen Netzwerkcode: Behandle jeden Aufruf wie einen Aufruf auf einem einzelnen Server. Installiere deine Mod auf dem Master.

## Verwandte Seiten { #related-pages }

- [Währungsbindungen](../../banksystem/currency-bindings.md): was Spieler sehen.
- [BankSystem-API](api.md): `BankStatus` und die Bank-Aufrufe, die deinen Adapter erreichen.
- [Transaktionsbuch](transaction-ledger.md): die `EXTERNAL_BIND`- und `EXTERNAL_UNBIND`-Einträge.
- [Master- und Slave-Server](../../admin/multi-server.md): wo deine Mod installiert sein muss.
