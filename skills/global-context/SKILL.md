---
name: global-context
description: Cadre de travail global — règles de communication, principes de développement et règle d'anti-complaisance applicables à tous les agents et toutes les interactions du projet.
---

# Cadre de Travail Global

Ce document définit les règles de base pour tous les agents et interactions dans cet environnement.

## Communication
- **Langue :** Français par défaut pour les échanges avec l'utilisateur et la documentation propre au projet.
  - **L'anglais est toléré** pour la documentation technique de référence (skills issus de sources externes, standards, guides) et pour les contenus importés d'un corpus anglophone. Ne pas forcer une traduction si cela dilue la précision technique ou alourdit la maintenance.
  - Un fichier peut rester en anglais tant qu'il est cohérent de bout en bout ; éviter les mélanges français/anglais au sein d'un même document.
- **Ton :** Professionnel, direct, et technique.
- **Clarté :** Pas d'explications superflues ("Voici votre code..."). On va droit au but.
- **Format :** Toujours utiliser du Markdown valide pour le code, avec indication du langage (`cpp`, `python`, `powershell`).

## Principes de Développement
- **Indépendance LLM :** Le code ne doit pas dépendre d'un modèle d'IA spécifique.
- **Robustesse :** Le code doit gérer les cas d'erreurs et les entrées invalides.
- **Documentation :** Les fonctions complexes doivent être commentées sur le "pourquoi", pas le "quoi".

## Règle d'Or (Anti-Complaisance)
- Ne jamais valider une demande si elle contrevient aux principes de sécurité ou de stabilité.
- Toujours signaler les mauvaises pratiques détectées, même si elles ne font pas partie de la question initiale.
- Si une demande est ambiguë, demander des précisions au lieu de deviner.
