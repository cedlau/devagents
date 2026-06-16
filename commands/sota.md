---
description: État de l'art rigoureux des méthodes existantes sur un sujet algorithmique, indépendamment de toute analyse de code.
argument-hint: <ALGORITHME> [méthodes pressenties] [fichier de sortie]
---

# Commande : état de l'art (SOTA)

Produire un **état de l'art** réutilisable sur le sujet algorithmique fourni, sans
analyse de code. Recette **atomique** : pour enchaîner avec une analyse de
faisabilité, voir `/sota-and-feasibility-analysis`. L'**interface** vers l'aval est
la section « Méthodes retenues » du livrable (cf. §2).

## Entrée

`$ARGUMENTS`

- `<ALGORITHME>` (1er argument) : la notion à étudier (ex. épaisseur, courbures,
  comparaison de maillages).
- `<MÉTHODES PRESSENTIES>` (optionnel) : méthodes que l'utilisateur cite déjà et
  qu'il faut confirmer ou infirmer.
- `<FICHIER_SORTIE>` (optionnel) : chemin du livrable.

## Pipeline opérationnel

Déléguer au sous-agent **`researcher`** (outil Agent / Task), qui applique le skill
`global-context` et sa **Tâche 3 (SOTA)**.

### 0. Levée d'ambiguïté (étape BLOQUANTE, avant toute recherche)

Lister les **définitions opérationnelles** existantes de `<ALGORITHME>` (souvent
plusieurs : ex. épaisseur = diamètre local *vs* paroi entre deux bords ;
comparaison = déviation métrique *vs* similarité perceptuelle). **Si le choix de
définition change la suite, poser la question** au lieu de présupposer. Ne pas
démarrer l'état de l'art détaillé tant que la définition cible n'est pas fixée.

### 1. État de l'art — contraintes imposées

- **Cartographie par familles**, nommées avec les termes consacrés de la
  littérature ; chaque famille distingue ses références **fondatrices** et
  **récentes**.
- **Couverture temporelle active et datée** : ne pas se limiter aux travaux
  fondateurs. Lancer explicitement, pour **chaque** famille, au moins une recherche
  ciblant les **~7 dernières années** (preprints récents inclus). Pour chaque
  famille, citer au moins un représentant récent **ou** justifier son absence
  (« aucune publication récente trouvée sur <X> au <date> »). L'absence de travaux
  récents est un **constat argumenté**, jamais un silence. Indiquer la **date de
  consultation**.
- **Volume & hiérarchie des sources** : viser **≥ 12 publications académiques
  distinctes** (revues / conférences / preprints évalués). Les **documents d'outils
  industriels** (éditeurs, plugins, tutoriels) sont **explicitement étiquetés comme
  tels**, regroupés dans une **section séparée**, **ne comptent pas** dans le quota,
  et **ne fondent jamais** une affirmation théorique — ils n'illustrent que la
  pratique.
- **Discipline de citation** (Règle d'Or `researcher`) : chaque affirmation
  factuelle est rattachée à une **source primaire vérifiable** (lien fonctionnel,
  DOI/arXiv si disponible). Étiqueter explicitement « fait sourcé » /
  « extrapolation » / « opinion ». **Aucune citation, DOI ou lien inventé** ; à
  défaut de vérification, marquer « à vérifier » plutôt qu'affirmer.
- **Tableau comparatif** (critères : définition, robustesse au bruit, continuité,
  coût, pré-requis, implémentation de référence).
- **Confirmer ou infirmer explicitement** les `<MÉTHODES PRESSENTIES>`, preuve à
  l'appui.
- Clôturer par : **frontières** (consensus / débats / angles morts) + **limites de la
  revue** (langue, profondeur de lecture — intégrale vs notice/abstract —, date de
  consultation).

Acquisition : recherche web ; pour lire un paper en profondeur, enchaîner les skills
`paper-fetch` puis `pdf-extraction`.

### 2. Sortie (avec interface aval)

Écrire le livrable dans `<FICHIER_SORTIE>` (sinon inline), en français, avec une
section **Sources** organisée par famille (papers / outils séparés). Le livrable
**doit** contenir une section explicite :

```
## Méthodes retenues
- <famille/méthode 1> — pourquoi retenue, pré-requis
- <famille/méthode 2> — ...
```

Cette section est le **contrat d'interface** consommé par `/feasibility-analysis`.

## Limites connues

- Tributaire de l'accès aux sources : un paper paywallé non lu en intégralité est
  signalé comme tel (anti-fabrication `researcher`), jamais résumé « de confiance ».
