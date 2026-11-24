---
title: "Setting up your project"
description: "Adding StockMarket and BankSystem to your Gradle build from JitPack, and declaring the dependency for Fabric and NeoForge."
---

# Setting up your project

BankSystem and StockMarket are Architectury mods for Minecraft 1.21.1 and Java 21. Your mod compiles against their common module and declares them as dependencies, so players install them next to your mod. You never bundle them into your jar.

Both mods need **ModUtilities**, and StockMarket also needs **BankSystem**. Add all the mods you use to your build.

## The quickest start: the example plugin

The [StockMarket example plugin](https://github.com/KROIA/StockMarketExamplePlugin) is a complete Architectury project for Fabric and NeoForge with a working StockMarket plugin. Copy it, rename the package and the mod id, and you have a project with every setting on this page already done. [Your first plugin](stockmarket/plugins/getting-started.md) walks through its code.

## Adding the repository

The mods are built by JitPack straight from their GitHub tags. Add the repository in every module that uses them (`common`, `fabric`, `neoforge`):

```groovy
repositories {
    maven { url 'https://jitpack.io' }
}
```

The first build of a new version can take a few minutes while JitPack compiles it. After that it's cached.

## Choosing the version

Each mod has its own version tag in the form `<Minecraft version>-<mod version>`, for example `1.21.1-2.2.0`. Put the tags into `gradle.properties`:

```properties
stockmarket_tag = 1.21.1-2.2.0
banksystem_tag = 1.21.1-2.2.0
modutilities_tag = 1.21.1-2.2.0
```

Use the versions your players will run. The three mods are released together, so their tags usually match.

## Adding the dependencies

**Common module:** compile against the API only.

```groovy
dependencies {
    modCompileOnly("com.github.KROIA.StockMarket:stockmarket-common:$rootProject.stockmarket_tag")
    modCompileOnly("com.github.KROIA.BankSystem:banksystem-common:$rootProject.banksystem_tag")
    modCompileOnly("com.github.KROIA.MC_ModUtilities:modutilities-common:$rootProject.modutilities_tag")
}
```

**Loader modules:** add the full mods, so they run in your development client and server.

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

A mod that only uses BankSystem leaves out the StockMarket lines.

The example project also looks for locally built jars first (`flatDir`). Remove that block if you don't build the mods yourself.

## Declaring the dependency

Tell the loader that your mod needs StockMarket (or BankSystem), so players get a clear message when it's missing or the wrong version:

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

The example accepts every 2.2 version. Widen the range only after you've tested your mod with the newer version. For BankSystem, use the mod id `banksystem`.

### Optional integration

If your mod also works without the other mod, declare it as optional (Fabric `suggests`, NeoForge `type = "optional"`). Then only touch its classes after checking that it's loaded, for example with Architectury's `Platform.isModLoaded("stockmarket")`, and keep those calls in a separate class. Otherwise your mod crashes when the class can't be found.

## Related pages

- [Developers](index.md): which API to use for which job.
- [Your first plugin](stockmarket/plugins/getting-started.md): the example project step by step.
- [BankSystem API](banksystem/api.md): the first calls to the bank.
