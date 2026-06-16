---
name: pdf-extraction
description: Extraire le texte d'un PDF volumineux vers un fichier .txt pour contourner les limites de lecture directe d'un PDF par le LLM. À utiliser avant d'analyser le contenu d'un PDF substantiel (paper, rapport technique).
---

# Skill : pdf-extraction

Utiliser ce skill lorsqu'un document PDF volumineux doit être analysé textuellement.

## Pipeline conseillé

1. **Prérequis (Environnement) :** Appliquer le skill `python-setup` pour préparer l'environnement virtuel, puis installer les dépendances du script via `pip install -r "${CLAUDE_PLUGIN_ROOT}/scripts/requirements.txt"` (fournit `pypdf`).
2. **Extraction :** Exécuter le script dédié :
   ```powershell
   python "${CLAUDE_PLUGIN_ROOT}/scripts/pdf_to_text.py" <chemin_du_pdf>
   ```
3. **Traitement :** Utiliser le fichier `.txt` généré (nommé `<nom_du_pdf>-extracted.txt`) pour l'analyse ultérieure.

## Notes
- Le script `pdf_to_text.py` gère la décompression des flux PDF et l'extraction page par page.
- Le fichier texte généré permet de contourner les limites de taille de lecture directe des fichiers PDF par le LLM.
