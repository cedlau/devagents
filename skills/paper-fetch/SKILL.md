---
name: paper-fetch
description: Récupérer le PDF d'un article scientifique en accès ouvert par arXiv ID ou DOI (résolu via OpenAlex). À utiliser pour chasser une référence trouvée dans la bibliographie d'un paper, quand le PDF n'est pas déjà présent localement.
---

# Skill : paper-fetch

Utiliser ce skill quand l'agent `researcher` a besoin de récupérer le PDF d'un article référencé (typiquement dans la bibliographie d'un paper qu'il vient de lire) et que ce PDF n'est pas déjà présent sur le filesystem local.

Couvre uniquement les **papers en accès ouvert** : preprints arXiv, et papers DOI dont OpenAlex expose une URL PDF open access. Les papers paywallés ne sont pas accessibles par cette voie — le script échoue proprement avec un message explicite, et il appartient à l'agent de basculer sur la procédure de repli (demander le PDF à l'utilisateur).

## Pipeline conseillé

1. **Prérequis (Environnement) :** Appliquer le skill `python-setup` si l'environnement virtuel n'est pas encore en place. Le script `paper_fetch.py` n'utilise que la bibliothèque standard — aucun paquet supplémentaire à installer.

2. **Identification de la référence :** Extraire de la biblio du paper source un identifiant exploitable :
   - **arXiv ID** : format `YYMM.NNNNN` (ex : `2301.12345`) ou legacy `archive[.subj]/YYMMNNN` (ex : `cs.CL/0701001`).
   - **DOI** : format `10.<registrant>/<suffix>` (ex : `10.1038/nature12345`).

   Si la référence ne fournit que titre + auteurs + année, **ne pas inventer** un identifiant — soit chercher localement via la procédure *chase reference* de l'agent, soit demander à l'utilisateur.

3. **Téléchargement :**
   ```powershell
   python "${CLAUDE_PLUGIN_ROOT}/scripts/paper_fetch.py" <identifier> --output-dir .cache/papers/
   ```

   Le script :
   - Pour un arXiv ID : télécharge directement depuis `https://arxiv.org/pdf/<id>` ;
   - Pour un DOI : interroge l'API OpenAlex (`https://api.openalex.org/works/doi:<doi>`) pour résoudre une URL PDF open access, puis télécharge.

   Codes de sortie :
   - `0` : succès, le chemin du PDF est imprimé sur stdout.
   - `1` : échec réseau ou pas de PDF open access disponible.
   - `2` : identifiant non reconnu (mauvais format).

4. **Enchaînement avec l'extraction texte :** Le chemin imprimé peut être directement passé à `pdf_to_text.py` (skill `pdf-extraction`) :
   ```powershell
   $pdf = python "${CLAUDE_PLUGIN_ROOT}/scripts/paper_fetch.py" 2301.12345 --output-dir .cache/papers/
   python "${CLAUDE_PLUGIN_ROOT}/scripts/pdf_to_text.py" $pdf
   ```

## Notes

- **User-Agent** : le script identifie ses requêtes via un User-Agent par défaut. Pour un usage intensif (batch sur des dizaines de références), passer `--user-agent "ton-projet/version (mailto:contact@exemple.fr)"` est une politesse appréciée par arXiv et OpenAlex.
- **Rate limiting** : OpenAlex tolère ~10 requêtes/seconde par IP. arXiv recommande au plus une requête toutes les 3 secondes. Pour des batchs importants, espacer les appels côté caller.
- **Paywall** : si OpenAlex ne retourne pas d'URL PDF open access (paper paywallé, ou non indexé), le script échoue avec un message explicite. Ce n'est **pas** un signal pour aller chercher ailleurs en force — c'est un signal pour demander à l'utilisateur.
- **Cache** : par convention, ranger les PDFs récupérés sous `.cache/papers/` à la racine du projet utilisateur (à ajouter au `.gitignore` si pas déjà fait). Le script ne crée pas ce dossier automatiquement au-delà de la valeur `--output-dir`.

## Limites connues

- Pas de résolution titre + auteur → DOI. Si l'agent ne dispose que d'une citation textuelle sans identifiant, il faut soit chercher localement, soit demander à l'utilisateur.
- Pas de découverte de mirror pour les papers paywallés. Pas d'accès Sci-Hub ou équivalent — par choix : la chaîne de fetch doit rester traçable et légalement nette.
- Pas de retry automatique sur erreur réseau transitoire. Si le téléchargement échoue ponctuellement, l'agent relance la commande.
