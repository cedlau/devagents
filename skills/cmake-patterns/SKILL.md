---
name: cmake-patterns
description: Standards pour le "Modern CMake" (Target-based), gestion des dépendances, et évolution des fichiers CMakeLists.txt.
---

# Skill: CMake Patterns & Evolution

Ce guide définit les standards pour la création et la maintenance des configurations CMake du projet.

## Principes du "Modern CMake"

### 1. Target-based Architecture
Ne jamais utiliser de fonctions globales comme `include_directories()` ou `add_definitions()`. Toujours raisonner en termes de cibles (targets).

```cmake
# BIEN
target_include_directories(my_target PUBLIC include/)
target_compile_options(my_target PRIVATE -Wall -Wextra)
target_link_libraries(my_target PRIVATE dependency_target)
```

### 2. Visibilité des Dépendances
- **PRIVATE** : La dépendance est nécessaire pour construire la cible, mais pas pour ceux qui l'utilisent.
- **INTERFACE** : La dépendance n'est pas nécessaire pour la cible elle-même, mais pour ceux qui l'utilisent (ex: header-only).
- **PUBLIC** : Nécessaire pour les deux.

### 3. Gestion des Fichiers
- Utiliser explicitement la liste des fichiers sources au lieu de `file(GLOB)`.
- Séparer la logique de build des tests via `if(BUILD_TESTING)`.

## Évolution et Maintenance

### Ajout d'une Dépendance
1. Utiliser `find_package()` avec `REQUIRED`.
2. Si la dépendance n'est pas système, utiliser `FetchContent` ou un gestionnaire de paquets (`vcpkg`, `conan`).
3. Lier via `target_link_libraries`.

### Structure Recommandée
- `CMakeLists.txt` racine : Définition du projet, options globales, inclusion des sous-répertoires.
- `src/CMakeLists.txt` : Définition des bibliothèques et exécutables.
- `tests/CMakeLists.txt` : Configuration des tests unitaires et intégration.

## Commandes de Diagnostic
- `cmake -B build -S .` : Génération et vérification de la configuration.
- `cmake --build build --target help` : Liste toutes les cibles disponibles.
- `cmake --graphviz=graph.dot .` : Générer un graphe des dépendances.
