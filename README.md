# Application d'Évolution de la Population

Cette application Streamlit permet de visualiser l'évolution de la population d'une commune exemple sous forme de graphique interactif.

## Fonctionnalités

- Visualisation de l'évolution de la population de 1968 à 2021
- Formatage des nombres selon la convention française (espaces comme séparateurs de milliers)
- Interface interactive avec tooltips
- Design moderne et lisible

## Déploiement

L'application est déployée sur Streamlit Cloud et accessible à l'adresse :
https://app-population-app-h7j6uqngmktbtgcbftwbdf.streamlit.app/

## Structure du projet

- `app.py` : Code principal de l'application
- `requirements.txt` : Liste des dépendances Python
- `.streamlit/config.toml` : Configuration de l'application

## Développement local

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancer l'application :
```bash
streamlit run app.py
``` 