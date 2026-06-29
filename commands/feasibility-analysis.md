---
description: Analyse de faisabilité sur le code existant — ce qu'il faut mettre en place pour implémenter une feature à partir de méthodes déjà identifiées.
argument-hint: <périmètre/module> <doc-SOTA-ou-méthodes> [fichier de sortie]
---

# Commande : analyse de faisabilité

Évaluer **ce qu'il faut mettre en place dans le code pour implémenter une feature**,
à partir d'un ensemble de méthodes déjà identifiées (typiquement issues d'un état de
l'art). Recette **atomique** : elle ne fait pas l'état de l'art (voir `/sota`). Elle
consomme les **« Méthodes retenues »** en entrée et produit un plan de faisabilité
sur le code existant.

**À ne pas confondre avec un audit de dette technique** : la dette technique *audite
du code existant* (qualité) ; ici on évalue la *faisabilité d'une feature nouvelle*
(ce qui existe pour l'implémenter, ce qui manque, le plan).

## Entrée

`$ARGUMENTS`

- `<PÉRIMÈTRE>` (**obligatoire**, 1er argument) : bibliothèque / module cible
  (ex. `src/module`).
- `<MÉTHODES>` (**obligatoire**, 2e argument) : soit le chemin d'un doc SOTA (dont la
  section « Méthodes retenues » sera lue), soit la liste des méthodes en clair.
- `<FICHIER_SORTIE>` (optionnel) : convention `src/<lib>/docs/<sujet>.md` (peut être
  le même fichier que le SOTA, en ajoutant une « Partie 2 »).

## Pipeline opérationnel

Déléguer au sous-agent **`architect`** (outil Agent / Task), qui applique le skill
`global-context` + le contexte langage (skill `cpp-specialist` + skills
`cpp-coding-standards`, `cmake-patterns` pour le C++ ; ce plugin n'embarque que le
contexte C++).

### 0. Cadrage

Charger les `<MÉTHODES>` : si un chemin de doc SOTA est fourni, **lire sa section
« Méthodes retenues »**. Confirmer `<PÉRIMÈTRE>` et langage dominant. Si l'entrée est
absente ou ambiguë, **demander** plutôt que supposer.

### 1. Cartographie de l'existant

Pour chaque méthode retenue : **ce qui existe et est réutilisable** dans le
`<PÉRIMÈTRE>` (chemins + numéros de ligne), **ce qui manque**, et les **briques
nécessaires**.

### 2. Discipline d'analyse (anti-complaisance)

- **Distinguer strictement** « vérifié par lecture du code » vs « **hypothèse à
  reproduire par exécution** ». Tout diagnostic de bug est une **hypothèse** tant
  qu'il n'a pas été exécuté/testé — l'étiqueter et le router vers une reproduction par exécution.
- **Pas de troncature silencieuse** : déclarer ce qui n'a **pas** été examiné.

### 3. Pistes d'intégration — exploration et validation utilisateur

**Ne pas s'enfermer prématurément sur une seule solution.** Identifier **toutes les
pistes d'intégration envisageables** (a minima les principales alternatives viables),
même partielles, et les présenter à l'utilisateur **avant** d'en privilégier une.

- Pour chaque piste : principe, points d'ancrage dans l'existant, ce qu'elle implique,
  **trade-offs** explicites (coût, risque, réutilisation, impact).
- **Soumettre ces pistes à l'utilisateur pour validation** et solliciter ses
  suggestions : il a souvent déjà une idée de la façon dont l'intégration — ou une
  partie d'elle — peut être réalisée. **Intégrer ses retours** avant de figer le plan.
- Présenter les pistes **en désignant une solution recommandée** (justifiée au regard
  des alternatives) : si l'utilisateur ne souhaite pas trancher lui-même une piste,
  c'est cette recommandation qui sert de défaut pour la suite.
- Ne figer le plan qu'**après** ce retour (validation, suggestion, ou recours au
  défaut recommandé), en justifiant le choix au regard des alternatives écartées (et
  des raisons de leur écart).
- **Frontière atomique** : ces pistes portent sur l'**intégration dans le code** des
  « Méthodes retenues » ; elles ne rouvrent pas le **choix des méthodes** (territoire
  de `/sota`). Si une piste révèle qu'une méthode retenue est inadaptée, le signaler
  en remontée vers le SOTA plutôt que de réinstruire l'état de l'art ici.

### 4. Plan & trade-offs

**Plan d'implémentation incrémental** (MVP → cible) sur la piste retenue + **trade-offs**
explicites. **Pas d'écriture de code d'implémentation** (frontière conception /
implémentation).

### 5. Sortie

Écrire dans `<FICHIER_SORTIE>` si fourni (sinon inline), en français. Si le fichier
contient déjà l'état de l'art, ajouter cette analyse comme « Partie 2 » / « Annexe ».
**Conserver la trace des pistes explorées** (retenue *et* écartées) dans la sortie.

### 6. Handoff

Analyse **seule**. Toute implémentation retenue passe ensuite par une phase
d'implémentation, puis une revue de code. Les bugs supposés sont d'abord reproduits
par exécution avant tout diagnostic.

## Checklist anti-biais (avant de conclure)

| Risque | Garde-fou |
|---|---|
| Bug affirmé sans exécution | Distinction vérifié-par-lecture / hypothèse-à-reproduire (§2) |
| « Tout couvert » | Déclarer explicitement le non-examiné (§2) |
| Verrouillage prématuré sur une solution | Explorer toutes les pistes et les soumettre à l'utilisateur avant de converger (§3) |
| Ignorer l'idée d'intégration de l'utilisateur | Solliciter et intégrer ses suggestions avant de figer le plan (§3) |
| Glissement vers l'implémentation | Frontière conception / implémentation (§4) |

## Limites connues

- L'analyse en lecture ne vaut pas exécution : les diagnostics restent des
  hypothèses jusqu'à reproduction.
- La qualité de l'analyse dépend de la clarté des `<MÉTHODES>` en entrée : un
  contrat « Méthodes retenues » flou produit une faisabilité floue.
