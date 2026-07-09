---
description: Audit de dette technique / optimisation C++ sur un périmètre borné, selon trois axes (extensibilité, maintenabilité, performances), analyse seule.
argument-hint: <PÉRIMÈTRE> [FICHIER_SORTIE]
---

# dev-technical-debt

Utiliser cette commande quand l'utilisateur veut un **audit de dette technique /
optimisation** sur un périmètre donné, selon trois axes : extensibilité,
maintenabilité long terme, performances.

Cette commande mène l'analyse **inline** (ce repo n'embarque pas le pipeline de
sous-agents de dev). Seul l'axe extensibilité peut être délégué au sous-agent
`architect` (présent). Les axes maintenabilité et performances sont conduits
directement, en s'appuyant sur les skills C++ présents. Elle impose le cadrage
qui évite deux travers : analyser « tout le projet » sans bornes, et affirmer un
problème de performance sans l'avoir mesuré.

Arguments fournis : $ARGUMENTS

## Périmètre supporté

Analyse **C++** (`.hpp`/`.cpp`/`.cc`/`.h` + CMake). Pour un autre langage, l'outillage
d'audit dédié n'est pas installé dans ce repo — le signaler plutôt que produire une
analyse générique.

## Objectif — trois axes prioritaires

1. **Extensibilité** : faciliter les prochaines évolutions et l'ajout de
   fonctionnalités sans casser l'existant (découplage, interfaces stables, points
   d'extension, inversion de dépendances).
2. **Maintenabilité long terme** : lisibilité, cohérence, réduction de la dette
   technique (duplication, complexité, couplage, code mort), et **testabilité &
   couverture par les tests**. Sur ce dernier point : repérer les zones critiques
   non couvertes et **mesurer** la couverture réelle (CTest/gcov/llvm-cov — c'est un
   fait mesurable, pas une hypothèse), tout en évaluant la **qualité** des tests
   (assertions pertinentes, cas limites). La couverture est un indicateur
   **nécessaire mais non suffisant** : ne pas en faire une cible chiffrée à
   maximiser aveuglément.
3. **Performances** : allocations/copies superflues, complexité algorithmique,
   layout mémoire/cache, temps de build — **pas** de vocabulaire web (« bundle »,
   « rendu », « requêtes réseau ») sauf si le périmètre est réellement une couche
   web. Tout claim de perf reste une **hypothèse jusqu'au profilage** (cf. §3).

## Paramètres attendus

- `<PÉRIMÈTRE>` (**obligatoire**) : chemin ou module à auditer (ex. `src/cgmesh`,
  `qmlviewer/src`). Refuser « tout le projet » sans bornes — scoper explicitement,
  quitte à enchaîner plusieurs passes.
- `<FICHIER_SORTIE>` (optionnel) : chemin du livrable si un rapport persistant est
  voulu (convention : `src/<lib>/docs/<sujet>-debt.md`). Le **format suit
  l'extension** :
  - `.md` (ou aucune extension) → Markdown ;
  - `.html` → HTML autonome **prêt à imprimer en PDF** (cf. §4). Choisir cette
    extension quand l'utilisateur demande un PDF : ce repo n'a pas de convertisseur
    Markdown→PDF installé, la voie retenue est HTML + *Imprimer → Enregistrer en PDF*.

## Pipeline opérationnel

### 0. Cadrage (avant analyse)

Confirmer le `<PÉRIMÈTRE>` et vérifier qu'il s'agit bien de C++. Activer le skill
`global-context` (communication, anti-complaisance) et le skill `cpp-specialist`.
Si le périmètre ou l'objectif prioritaire est ambigu, **demander** plutôt que
supposer.

### 1. Vue d'ensemble

Décrire l'architecture du périmètre **avant** d'entrer dans le détail : structure
des dossiers, séparation des responsabilités, flux de données, dépendances.

### 2. Conduite par axe

Chaque ligne couvre un des trois axes prioritaires :

| Axe prioritaire | Cas | Conduite | Référentiels à charger |
|---|---|---|---|
| **Extensibilité** | découplage, découpage en modules, interfaces, points d'extension | déléguer au sous-agent `architect` | skill `global-context` + skill `cpp-specialist` |
| **Maintenabilité** | lisibilité, cohérence, duplication, complexité, code mort | analyse inline | skills `cpp-specialist`, `cpp-coding-standards` |
| **Maintenabilité** | testabilité, **couverture mesurée** & zones non testées | analyse inline | skill `cpp-testing` (+ outil de couverture : CTest/gcov/llvm-cov) |
| **Performances** | optimisation C++ | analyse inline | skills `cpp-specialist`, `cpp-coding-standards`, `cmake-patterns` |

Pour chaque problème identifié : **fichier/module concerné**, nature du problème,
**impact concret**, et correction recommandée (avec exemple de code si pertinent).

### 3. Discipline d'analyse (anti-complaisance)

- **Distinguer** « constaté par lecture du code » vs « **hypothèse à mesurer** ».
  Tout claim de **performance** est une hypothèse tant qu'un profiler (ou un
  benchmark) ne l'a pas confirmé — ne jamais le présenter comme un fait ;
  recommander explicitement le profilage et assumer l'incertitude.
- **Distinguer quick wins** (effort faible, gain immédiat) des **refactorings
  structurels** (effort élevé, gain durable).
- Signaler anti-patterns, code dupliqué, dépendances obsolètes/inutiles (côté
  C++ : `extern/`, CMake), zones non couvertes par les tests.
- **Pas de troncature silencieuse** : déclarer explicitement ce qui n'a **pas** été
  couvert dans le périmètre (fichiers ignorés, axe non instruit).

### 4. Format de sortie

Structure du rapport, quel que soit le format :

- **Synthèse en tête** : les 3 à 5 points les plus critiques.
- **Tableau priorisé** : `Priorité | Axe | Problème | Recommandation | Effort estimé`.
  La priorité est indiquée par une émoticône : 🔴 haute, 🟡 moyenne, 🟢 basse.
- **Détail technique** ensuite, regroupé par module.

Destination selon `<FICHIER_SORTIE>` :

- **non fourni** → rendre **inline** dans la conversation ;
- **`.md`** → écrire le rapport en Markdown ;
- **`.html`** → écrire un **HTML autonome prêt à imprimer en PDF** (voir contraintes
  ci-dessous), puis indiquer à l'utilisateur : *ouvrir le fichier dans un
  navigateur → Imprimer → destination « Enregistrer au format PDF »*.

**Contraintes du HTML (uniquement si sortie `.html`)** :

- **Un seul fichier autonome** : tout le CSS dans un `<style>` inline, aucune
  ressource externe (pas de CDN, police ou image distante) — le fichier doit
  s'imprimer correctement hors-ligne.
- **CSS d'impression** : inclure `@page { margin: 1.5cm; }` et une règle
  `@media print` ; éviter les coupures de tableau/section disgracieuses avec
  `break-inside: avoid` sur les lignes et les blocs de findings.
- **Pastilles de priorité colorées** : rendre 🔴/🟡/🟢 par des badges CSS (rouge
  `#d33` / orange `#e6a700` / vert `#2e9e44`) lisibles aussi en niveaux de gris.
- **Lisibilité papier** : police système à empattement ou sans (14px base),
  tableau à bordures fines, largeur de contenu bornée (`max-width` ~ 900px).
- **En-tête** : titre, périmètre audité et date de génération en haut du document.

### 5. Handoff

Analyse **seule** — pas de modification sans validation. Toute implémentation
retenue est ensuite réalisée sur demande explicite, revue avant de conclure.

## Contraintes

- **Précis et actionnable** : pas de conseil générique type « améliorer la qualité
  du code ».
- Si une recommandation comporte un **risque ou un compromis** (ex. gain de perf au
  détriment de la lisibilité), le dire explicitement.
- **Justifier les priorités** : pourquoi tel point passe avant tel autre.
- Si une information manque pour juger, **poser la question** (Règle d'Or,
  skill `global-context`).

## Limites connues

- L'analyse en lecture ne vaut pas mesure : les claims de perf restent des
  hypothèses jusqu'à profilage/benchmark. Ce repo n'embarque pas le sous-agent
  dédié `cpp-optimizer` (détection toolchain, matrice de features) : l'analyse perf
  est donc plus générique qu'une passe outillée.
- La couverture dépend du `<PÉRIMÈTRE>` ; un audit « projet entier » se découpe en
  plusieurs passes scopées plutôt qu'une passe superficielle unique.
