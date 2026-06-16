# devagents — plugin Claude Code

Plugin pour Claude Code dédié à la chaîne **recherche scientifique → faisabilité** :
produire un état de l'art rigoureux sur un sujet algorithmique, puis évaluer ce qu'il
faut mettre en place dans le code pour l'implémenter.

## Installation

Ce dépôt est à la fois le **plugin** `devagents` et un **marketplace** Claude Code
mono-plugin nommé `perso-agents` (manifestes dans `.claude-plugin/`).

### Depuis GitHub (recommandé)

Dans une session Claude Code :

```
/plugin marketplace add cedlau/devagents
/plugin install devagents@perso-agents
```

> La forme courte `cedlau/devagents` cible GitHub ; les formes
> `https://github.com/cedlau/devagents` ou `git@github.com:cedlau/devagents.git`
> fonctionnent aussi.

### Depuis un clone local

```
git clone https://github.com/cedlau/devagents.git
```

puis, dans Claude Code :

```
/plugin marketplace add /chemin/vers/devagents
/plugin install devagents@perso-agents
```

### Vérifier / gérer

```
/plugin          # UI : activer, désactiver, désinstaller
/help            # /sota, /feasibility-analysis, /sota-and-feasibility-analysis y figurent
```

Après une mise à jour du dépôt : `/plugin marketplace update perso-agents`, puis
recharge la session si nécessaire.

## Utilisation

### Commandes

| Commande | Rôle |
|---|---|
| `/sota <ALGORITHME> [méthodes] [sortie]` | État de l'art seul (sous-agent `researcher`). |
| `/feasibility-analysis <périmètre> <méthodes> [sortie]` | Analyse de faisabilité sur le code (sous-agent `architect`). |
| `/sota-and-feasibility-analysis <ALGORITHME> [périmètre] [sortie]` | Orchestrateur : enchaîne les deux. |

Exemples :

```
/sota épaisseur
/sota "courbures discrètes" "Taubin, cotangent" docs/curvatures.md
/feasibility-analysis src/cgmesh docs/curvatures.md
/sota-and-feasibility-analysis épaisseur src/cgmesh docs/thickness.md
```

- **`/sota`** produit un état de l'art (cartographie par familles, couverture
  temporelle datée, ≥ 12 sources académiques, tableau comparatif) terminé par une
  section « Méthodes retenues » qui sert de contrat d'interface vers la faisabilité.
- **`/feasibility-analysis`** consomme ces « Méthodes retenues » (ou une liste en
  clair) et produit, sur le périmètre de code visé, ce qui est réutilisable / ce qui
  manque / un plan incrémental — sans écrire de code d'implémentation.
- **`/sota-and-feasibility-analysis`** enchaîne les deux dans un même livrable
  (Partie 1 = état de l'art, Partie 2 = faisabilité).

### Récupération de papers

Pendant un état de l'art, l'agent `researcher` peut récupérer et lire des PDFs en
accès ouvert. Les scripts Python correspondants nécessitent un environnement prêt :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r "<plugin>/scripts/requirements.txt"
```

Les skills `python-setup`, `paper-fetch` et `pdf-extraction` décrivent la procédure ;
l'agent les applique automatiquement quand c'est pertinent. Les PDFs récupérés sont
rangés par convention sous `.cache/papers/` à la racine du projet de travail.

## Contenu

### Sous-agents (`agents/`)

- **`researcher`** — chercheur scientifique senior : lecture critique, synthèses,
  comparaisons, états de l'art ; règle d'or « référence ou abstention », anti-fabrication.
- **`architect`** — architecte logiciel senior (C++) : structure, découplage,
  trade-offs, plan incrémental, **sans** écrire de code d'implémentation.

### Skills (`skills/`)

Contexte et procédures, auto-découverts par description et applicables à la demande :

- `global-context` — règles de communication et anti-complaisance, appliquées par les agents.
- `cpp-specialist` — standards C++ moderne (RAII, idiomes, revue).
- `cpp-coding-standards` — C++ Core Guidelines.
- `cmake-patterns` — Modern CMake (target-based).
- `pdf-extraction` — extraction texte d'un PDF volumineux (`scripts/pdf_to_text.py`, dépend de `pypdf`).
- `paper-fetch` — récupération d'un PDF open access par arXiv ID / DOI (`scripts/paper_fetch.py`, stdlib seule).
- `python-setup` — préparation de l'environnement virtuel Python.

### Scripts (`scripts/`)

`pdf_to_text.py`, `paper_fetch.py`, `requirements.txt` — invoqués par les skills
`pdf-extraction` / `paper-fetch` via `${CLAUDE_PLUGIN_ROOT}/scripts/`.

## Notes

- Outils des agents : `Read`/`Grep`/`Glob`/`Bash`, plus `WebSearch`/`WebFetch` pour
  `researcher` (recherche web pendant l'état de l'art).
- Les chemins internes utilisent `${CLAUDE_PLUGIN_ROOT}`.
- Périmètre langage limité au **C++** : pour un autre langage, l'`architect` signale
  l'absence du standard correspondant plutôt que d'inventer des règles.
