---
description: Enchaîne en une commande l'état de l'art puis l'analyse de faisabilité sur le code pour une feature algorithmique.
argument-hint: <ALGORITHME> [périmètre/module] [fichier de sortie]
---

# Commande : SOTA + faisabilité

Enchaîner, en **une seule commande**, **état de l'art → analyse de faisabilité sur le
code** pour une feature algorithmique. Commande **orchestratrice** : elle ne réinvente
rien, elle enchaîne les deux commandes atomiques. Pour n'en vouloir qu'une seule, les
invoquer directement : `/sota` (état de l'art seul, sous-agent `researcher`) ou
`/feasibility-analysis` (faisabilité seule, sous-agent `architect`).

## Entrée

`$ARGUMENTS`

- `<ALGORITHME>` (1er argument) : la notion à étudier (ex. épaisseur, courbures).
- `<PÉRIMÈTRE>` (optionnel, défaut à demander) : bibliothèque/module cible
  (ex. `src/cgmesh`).
- `<FICHIER_SORTIE>` (optionnel) : convention `src/<lib>/docs/<sujet>.md`. Le SOTA et
  la faisabilité y sont assemblés en « Partie 1 » et « Partie 2 ».

## Pipeline opérationnel

### 1. État de l'art

Exécuter le pipeline de `/sota` (voir `${CLAUDE_PLUGIN_ROOT}/commands/sota.md`) avec
`<ALGORITHME>` (+ méthodes pressenties éventuelles) et `<FICHIER_SORTIE>`. Le livrable
produit **doit** contenir la section « Méthodes retenues » (contrat d'interface).

### 2. Analyse de faisabilité

Exécuter le pipeline de `/feasibility-analysis` (voir
`${CLAUDE_PLUGIN_ROOT}/commands/feasibility-analysis.md`) avec `<PÉRIMÈTRE>` et, en
`<MÉTHODES>`, le **chemin du livrable SOTA produit en étape 1** (sa section
« Méthodes retenues »). La faisabilité est ajoutée comme « Partie 2 » du même
`<FICHIER_SORTIE>`.

### 3. Assemblage

Vérifier la cohérence des deux parties (les méthodes retenues en Partie 1 sont bien
celles instruites en Partie 2) et lier les sections. Le handoff aval (phase
d'implémentation, revue de code, reproduction des bugs par exécution) est porté par
`/feasibility-analysis`.

## Note

Chaque commande atomique porte sa propre checklist anti-biais (couverture temporelle,
hiérarchie des sources et citation pour `/sota` ; vérifié-vs-hypothèse, non-troncature,
exploration de **toutes** les pistes d'intégration et validation utilisateur — avec
solution recommandée par défaut — pour `/feasibility-analysis`). L'orchestrateur
n'ajoute que le chaînage et la cohérence Partie 1 ↔ Partie 2.
