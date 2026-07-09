---
description: Veille outillage open source ciblée sur la codebase courante — identifie des projets OSS récents, les teste en sandbox isolé, produit un rapport de décision.
argument-hint: [périmètre (axe à privilégier, ex. observabilité, tests, performances)]
---

# dev-tech-watch

Utiliser cette commande pour une **veille outillage open source ciblée sur la
codebase courante** : identifier des projets OSS récents qui apporteraient de la
valeur au stack du projet, les **évaluer empiriquement en sandbox**, et produire un
rapport de décision (adopter / watch / écarter).

À ne pas confondre avec `/sota` (veille **académique** sur un sujet algorithmique,
papers + discipline de citation). Ici la cible est l'**outillage industriel** et le
livrable est un **rapport produit** appuyé sur des tests réels.

Périmètre fourni (optionnel — axe à privilégier ; sinon, balayer tous les axes) : $ARGUMENTS

## Principe de séparation et de rigueur

- La commande **agit** (crée des sandbox, installe, exécute, écrit le rapport). Elle
  délègue l'analyse de contexte au sous-agent `architect` ; l'intégration et les
  tests sont menés **inline** (ce repo n'embarque pas de sous-agent `developer`).
- **Règle d'Or héritée de `researcher`** : aucune métrique, licence ou affirmation
  inventée. Toute donnée non vérifiée est étiquetée `à vérifier` ; une métrique
  estimée (ex. croissance hebdomadaire de stars) est marquée `estimation`. Mieux
  vaut un champ marqué incertain qu'un chiffre asséné.
- **Honnêteté du résultat** : si aucun projet réellement pertinent n'émerge, le dire
  explicitement. Un rapport vide et argumenté vaut mieux qu'un rapport rempli de
  bruit. L'absence de candidat est un **constat motivé**, jamais un silence.

## Garde-fou sécurité (BLOQUANT)

Installer et exécuter du code OSS tiers est une opération à risque. Obligations :
- **Sandbox isolé** par projet — jamais sur le code de production, idéalement un
  conteneur / environnement jetable.
- **Aucune modification** du code de prod ni des fichiers de dépendances du projet
  réel (`package.json`, `pyproject.toml`, `Cargo.toml`, `composer.json`, CMake…).
- Lire la documentation d'installation officielle ; ne pas exécuter de script
  d'install opaque sans l'avoir inspecté.

---

## Phase 1 — CONTEXTE (délégation au sous-agent `architect`)

Déléguer au sous-agent `architect` pour reconstituer, via `read` / `search` / `list` :

1. **Stack technique** : langages, frameworks, librairies principales, base de
   données, infrastructure (lire les manifestes de dépendances, fichiers CI, IaC).
2. **Domaine métier** : à partir du README, de la documentation, des noms des
   modules principaux et des dépendances, reconstituer ce que fait l'application.
3. **Points de friction / zones à valeur** : où un outil tiers aiderait —
   performances, observabilité, sécurité, DX, automatisation de tests, gestion de la
   donnée, etc. Si `périmètre` est fourni, prioriser cet axe.

Sortie de phase : une note de contexte (stack + domaine + axes de friction
priorisés) qui cadre la veille.

## Phase 2 — VEILLE (recherche GitHub ciblée)

Rechercher (capacité de recherche web / GitHub) les projets OSS pertinents pour le
stack identifié, en appliquant ces **filtres** :

**Retenir** :
- Publiés ou significativement mis à jour sur les **3 derniers mois**.
- **> 500 stars** OU croissance rapide (**> ~100 stars/semaine**, marquée
  `estimation` car difficile à vérifier précisément).
- **Compatibles** avec le stack de la phase 1.

**Écarter** :
- Projets non maintenus (**dernier commit > 6 mois**).
- Forks sans valeur ajoutée.
- Licences incompatibles avec un usage commercial : **AGPL, SSPL, BSL** — et tout
  cas où la compatibilité ne peut pas être confirmée (exclusion conservatrice).

Consigner la **date de consultation** : ces métriques sont datées.

## Phase 3 — SÉLECTION & TEST (inline, en sandbox isolé)

1. **Sélectionner 3 à 5 projets**, en privilégiant la **diversité des cas d'usage**
   couverts plutôt que plusieurs variantes d'un même outil.
2. Pour chaque projet retenu, créer un dossier `/tech-watch/{date}/{nom-du-projet}/`.
3. Dans le **sandbox isolé** (cf. garde-fou), directement :
   - installer le projet en suivant sa documentation officielle ;
   - configurer une **intégration minimale viable** sur un cas d'usage représentatif
     de la codebase (sans toucher au code de prod) ;
   - exécuter **au moins 3 scénarios** : un cas **nominal**, un cas **limite**, un cas
     d'**échec** ; capturer logs et outputs pertinents.

Si un projet ne s'installe pas ou ne peut pas être testé, le consigner comme tel —
ne pas extrapoler un résultat de test non exécuté.

## Phase 4 — RAPPORT

Rédiger `/tech-watch/{date}/rapport.md`. Pour **chaque projet évalué** :

```markdown
## <nom> — <lien GitHub>

**Description** : <deux phrases>
**Métriques d'adoption** : stars, contributeurs actifs, fréquence des releases,
date du dernier commit (étiqueter `à vérifier` / `estimation` au besoin).
**Licence & compatibilité** : <licence> — <compatible / incompatible / à confirmer>.
**Problème résolu dans notre contexte** : <quel point de friction, en citant les
fichiers ou modules concernés>.
**Résultats des tests** : <nominal / limite / échec — avec extraits de logs/outputs>.
**Effort d'intégration estimé** : <heures de dev, impact bundle, dépendances ajoutées>.
**Risques** : <maturité, gouvernance, lock-in, performance>.
**Recommandation** : Adopter rapidement | Garder en watch (réévaluer dans 3 mois) | Écarter.
```

Clore le rapport par :
- un **tableau de synthèse comparatif** (projet × critères) ;
- un **classement par ratio valeur / effort d'intégration** ;
- une section **Limites de la veille** : axes non couverts, métriques non vérifiées,
  date de consultation.

Si aucun projet ne passe les filtres ou les tests : écrire un rapport court et
honnête expliquant **pourquoi** (axes explorés, candidats écartés et motif), sans
remplir avec des choix médiocres.

## Phase 5 — REPORT (utilisateur)

Récapituler : nombre de candidats balayés, nombre testés, recommandations par
catégorie (adopter / watch / écarter), et chemin du rapport.

---

## Règles d'effet de bord

- **Tout vit sous `/tech-watch/{date}/`** : sandbox, configs de test, rapport.
- **Jamais de modification du projet réel** (code, dépendances, config).
- **Aucune adoption automatique** : la commande recommande, la décision et
  l'intégration en prod appartiennent à l'équipe.

## Utilisation

- `/dev-tech-watch` : veille tous axes.
- `/dev-tech-watch observabilité` : veille ciblée sur un axe de friction.
