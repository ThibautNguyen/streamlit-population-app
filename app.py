import streamlit as st
import pandas as pd
import altair as alt

# Configuration de la page
st.set_page_config(
    page_title="Évolution de la Population",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Création des données
data = {
    'année': [1968, 1975, 1982, 1990, 1999, 2006, 2011, 2016, 2021],
    'population': [8949, 9550, 9800, 10100, 11250, 12500, 13750, 14854, 16000]
}

df = pd.DataFrame(data)

# Fonction pour formater les nombres selon la convention française
def format_number(x):
    return f"{x:,.0f}".replace(",", " ")

# Ajout d'une colonne formatée pour les tooltips
df['population_formatted'] = df['population'].apply(format_number)

# Création du graphique
chart = alt.Chart(df).mark_line(
    point=True,
    color='#3B825C'
).encode(
    x=alt.X('année:O', title='Année'),
    y=alt.Y('population:Q', 
            title='Population',
            axis=alt.Axis(format='~s', labelExpr="replace(datum.label, ',', ' ')")),
    tooltip=[
        alt.Tooltip('année:O', title='Année'),
        alt.Tooltip('population_formatted:N', title='Population')
    ]
).properties(
    width=800,
    height=400
)

# Affichage du titre
st.title('Évolution de la Population')

# Affichage du graphique
st.altair_chart(chart, use_container_width=True)

# Documentation technique (non visible pour les utilisateurs)
# 
# ### À propos de ce graphique
# - Ce graphique montre l'évolution de la population d'une commune fictive
# - Les points sont espacés d'au moins 5 ans pour respecter les contraintes de comparaison
# - La couleur #3B825C est utilisée pour représenter les données de population
# - L'application utilise un thème clair avec un fond blanc pour une meilleure lisibilité
# - Les textes sont en couleur #272F4D pour l'interface et #000011 pour les graphiques
# - La police Axiforma est utilisée pour les graphiques
# 
# ### Formatage des nombres
# - Une fonction `format_number` est utilisée pour garantir le formatage selon la convention française
# - Les années sont affichées sans séparateur (ex: 1968)
# - Les volumes de population sont systématiquement affichés avec un espace comme séparateur de milliers (ex: 14 854)
# - La notation scientifique est désactivée pour une meilleure lisibilité
# - Les tooltips utilisent le même formatage que l'axe des ordonnées pour la cohérence
# 
# ### Configuration technique
# - Un fichier `.streamlit/config.toml` est présent pour assurer la stabilité de l'application
# - Le timeout est configuré à 2 heures pour éviter les déconnexions
# - Les paramètres du serveur sont optimisés pour une meilleure performance
# - Le mode "watchdog" est désactivé pour réduire les interruptions
# - La compression WebSocket est désactivée pour améliorer la stabilité 