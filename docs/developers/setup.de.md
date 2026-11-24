---
title: "Dein Projekt einrichten"
description: "StockMarket und BankSystem über JitPack zu deinem Gradle-Build hinzufügen und die Abhängigkeit für Fabric und NeoForge deklarieren."
---

# Dein Projekt einrichten { #setting-up-your-project }

BankSystem und StockMarket sind Architectury-Mods für Minecraft 1.21.1 und Java 21. Deine Mod kompiliert gegen ihr Common-Modul und deklariert sie als Abhängigkeiten, sodass Spieler sie neben deiner Mod installieren. Du packst sie nie in dein Jar.

Beide Mods brauchen **ModUtilities**, und StockMarket braucht außerdem **BankSystem**. Füge alle Mods, die du nutzt, zu deinem Build hinzu.

## Der schnellste Start: das Beispiel-Plugin { #the-quickest-start-the-example-plugin }

Das [StockMarket-Beispiel-Plugin](https://github.com/KROIA/StockMarketExamplePlugin) ist ein vollständiges Architectury-Projekt für Fabric und NeoForge mit einem funktionierenden StockMarket-Plugin. Kopiere es, benenne das Package und die Mod-ID um, und du hast ein Projekt, in dem jede Einstellung dieser Seite schon erledigt ist. [Dein erstes Plugin](stockmarket/plugins/getting-started.md) geht seinen Code Schritt für Schritt durch.

## Das Repository hinzufügen { #adding-the-repository }

JitPack baut die Mods direkt aus ihren GitHub-Tags. Füge das Repository in jedem Modul hinzu, das sie nutzt (`common`, `fabric`, `neoforge`):

```groovy
repositories {
    maven { url 'https://jitpack.io' }
}
```

Der erste Build einer neuen Version kann ein paar Minuten dauern, während JitPack sie kompiliert. Danach liegt sie im Cache.

## Die Version wählen { #choosing-the-version }

Jede Mod hat ihren eigenen Versions-Tag in der Form `<Minecraft version>-<mod version>`, zum Beispiel `1.21.1-2.2.0`. Trage die Tags in `gradle.properties` ein:

```properties
stockmarket_tag = 1.21.1-2.2.0
banksystem_tag = 1.21.1-2.2.0
modutilities_tag = 1.21.1-2.2.0
```

Nutze die Versionen, die deine Spieler verwenden werden. Die drei Mods erscheinen zusammen, daher passen ihre Tags meistens zueinander.

## Die Abhängigkeiten hinzufügen { #adding-the-dependencies }

**Common-Modul:** Kompiliere nur gegen die API.

```groovy
dependencies {
    modCompileOnly("com.github.KROIA.StockMarket:stockmarket-common:$rootProject.stockmarket_tag")
    modCompileOnly("com.github.KROIA.BankSystem:banksystem-common:$rootProject.banksystem_tag")
    modCompileOnly("com.github.KROIA.MC_ModUtilities:modutilities-common:$rootProject.modutilities_tag")
}
```

**Loader-Module:** Füge die vollständigen Mods hinzu, damit sie in deinem Entwicklungs-Client und -Server laufen.

=== "Fabric"

    ```groovy
    dependencies {
        modImplementation("com.github.KROIA.StockMarket:stockmarket-fabric:$rootProject.stockmarket_tag")
        modImplementation("com.github.KROIA.BankSystem:banksystem-fabric:$rootProject.banksystem_tag")
        modImplementation("com.github.KROIA.MC_ModUtilities:modutilities-fabric:$rootProject.modutilities_tag")
    }
    ```

=== "NeoForge"

    ```groovy
    dependencies {
        modImplementation("com.github.KROIA.StockMarket:stockmarket-neoforge:$rootProject.stockmarket_tag")
        modImplementation("com.github.KROIA.BankSystem:banksystem-neoforge:$rootProject.banksystem_tag")
        modImplementation("com.github.KROIA.MC_ModUtilities:modutilities-neoforge:$rootProject.modutilities_tag")
    }
    ```

Eine Mod, die nur BankSystem nutzt, lässt die StockMarket-Zeilen weg.

Das Beispielprojekt sucht außerdem zuerst nach lokal gebauten Jars (`flatDir`). Entferne diesen Block, wenn du die Mods nicht selbst baust.

## Die Abhängigkeit deklarieren { #declaring-the-dependency }

Sag dem Loader, dass deine Mod StockMarket (oder BankSystem) braucht. Dann bekommen Spieler eine klare Meldung, wenn sie fehlt oder die falsche Version hat:

=== "Fabric (fabric.mod.json)"

    ```json
    "depends": {
      "stockmarket": ">=1.21.1-2.2.0 <1.21.1-2.3.0"
    }
    ```

=== "NeoForge (neoforge.mods.toml)"

    ```toml
    [[dependencies.yourmodid]]
    modId = "stockmarket"
    type = "required"
    versionRange = "[1.21.1-2.2.0, 1.21.1-2.3.0)"
    ordering = "AFTER"
    side = "BOTH"
    ```

Das Beispiel akzeptiert jede 2.2-Version. Erweitere den Bereich erst, nachdem du deine Mod mit der neueren Version getestet hast. Für BankSystem nimmst du die Mod-ID `banksystem`.

### Optionale Integration { #optional-integration }

Wenn deine Mod auch ohne die andere Mod funktioniert, deklariere sie als optional (Fabric `suggests`, NeoForge `type = "optional"`). Greif dann nur auf ihre Klassen zu, nachdem du geprüft hast, dass sie geladen ist, zum Beispiel mit `Platform.isModLoaded("stockmarket")` von Architectury. Halte diese Aufrufe in einer eigenen Klasse. Sonst stürzt deine Mod ab, wenn die Klasse nicht gefunden wird.

## Verwandte Seiten { #related-pages }

- [Entwickler](index.md): welche API für welche Aufgabe.
- [Dein erstes Plugin](stockmarket/plugins/getting-started.md): das Beispielprojekt Schritt für Schritt.
- [BankSystem-API](banksystem/api.md): die ersten Aufrufe an die Bank.
