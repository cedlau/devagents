---
name: python-setup
description: Préparer l'environnement d'exécution Python (venv + dépendances) avant de lancer un script Python du plugin (pdf_to_text.py, paper_fetch.py).
---

# Skill : python-setup

Utiliser ce skill pour préparer l'environnement d'exécution de n'importe quel script Python du plugin.

## Procédure

1. **Création de l'environnement virtuel :**
   ```powershell
   python -m venv .venv
   ```

2. **Activation :**
   - Sur Windows (PowerShell) : `.\.venv\Scripts\Activate`
   - Sur Linux/macOS : `source .venv/bin/activate`

3. **Installation des dépendances :**
   Vérifier la présence d'un fichier `requirements.txt` à la racine ou dans le dossier du script :
   ```powershell
   pip install -r requirements.txt
   ```

## Pourquoi utiliser ce skill ?
- **Isolation :** Évite les conflits entre les versions de bibliothèques.
- **Portabilité :** Facilite le déploiement sur une autre machine.
- **Propreté :** Garde votre installation Python système intacte.
