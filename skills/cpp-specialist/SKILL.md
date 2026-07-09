---
name: cpp-specialist
description: Standards et bonnes pratiques C++ moderne (C++17/20) — gestion mémoire RAII, design, concurrence, idiomes, critères de revue. À charger dès qu'un fichier C++ est présent ou modifié.
---

# Standards et Bonnes Pratiques C++

## Standards de Langage
- Priorité au **C++20** (ou C++17 minimum).
- Utilisation systématique des fonctionnalités modernes : `auto`, `constexpr`, `concepts`, `ranges`.

## Gestion de la Mémoire et Ressources
- **RAII (Resource Acquisition Is Initialization)** est obligatoire.
- **Zéro pointeur brut (`*`) pour la possession** : utiliser `std::unique_ptr` ou `std::shared_ptr`.
- **Règle de Zéro** privilégiée : laisser le compilateur générer les constructeurs/destructeurs si possible.
- Utiliser `std::string_view` et `std::span` pour éviter les copies inutiles.

## Structure et Design
- Séparation stricte Déclaration (`.hpp`) / Définition (`.cpp`).
- Utilisation de `std::optional` et `std::expected` (ou `result`) pour la gestion d'erreurs au lieu des exceptions si la performance est critique.
- Préférence pour la composition sur l'héritage.

## Critères de Revue et Qualité

### Sécurité Mémoire (CRITIQUE)
- **RAII obligatoire** : Pas de `new`/`delete` nus. Utiliser `std::unique_ptr` ou `std::shared_ptr`.
- **Bornes** : Éviter les tableaux C, préférer `std::array`, `std::vector`, `std::span`.
- **Initialisation** : Toute variable doit être initialisée. Préférer l'initialisation uniforme `{}`.

### Concurrence (HAUTE)
- Pas de manipulation directe de mutex : utiliser `std::lock_guard` ou `std::scoped_lock`.
- Vérifier l'absence de "data races" sur les états partagés.

### Idiomes Modernes (HAUTE)
- **Règle de Zéro** privilégiée.
- Utilisation de `const` et `constexpr` par défaut.
- Passage par `const T&` pour les objets larges, `std::string_view` pour les chaînes.

### Performance (MOYENNE)
- Utiliser `std::move` pour les paramètres "sink".
- Utiliser `reserve()` sur les containers si la taille est connue.

## Tests (Critère de Qualité)
- Toute fonctionnalité C++ doit être couverte par des tests fiables et isolés.
- Approche TDD (RED → GREEN → REFACTOR) et structure AAA (Arrange / Act / Assert).
- Isolation par injection de dépendances + fakes/mocks ; jamais d'état global caché.
- Couvrir systématiquement les cas limites (entrées nulles, vides, hors bornes)
  et chaque branche logique (if/else, switch).
- **Pour la mise en œuvre** (GoogleTest/GoogleMock, CMake/CTest, coverage gcov/llvm-cov,
  sanitizers ASan/UBSan/TSan) → charger le skill `cpp-testing`.
