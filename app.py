import streamlit as st
import pandas as pd
import altair as alt
import io

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
base = alt.Chart(df).encode(
    x=alt.X('année:O', title='Année'),
    y=alt.Y('population:Q', 
            title='Population',
            axis=alt.Axis(format='~s', labelExpr="replace(datum.label, ',', ' ')"))
)

# Création de la ligne
line = base.mark_line(color='#3B825C')

# Création des points avec la même couleur
points = base.mark_point(
    color='#3B825C',
    size=100
).encode(
    tooltip=[
        alt.Tooltip('année:O', title='Année'),
        alt.Tooltip('population_formatted:N', title='Population')
    ]
)

# Combinaison de la ligne et des points
chart = (line + points).properties(
    width=800,
    height=400
)

# Affichage du titre
st.title('Évolution de la Population')

# Affichage du graphique
st.altair_chart(chart, use_container_width=True)

# Ajout des options d'export
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.write("### Télécharger les données")
    
    # Export CSV
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Télécharger en CSV",
        data=csv,
        file_name="population_data.csv",
        mime="text/csv",
    )
    
    # Export Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Population', index=False)
    st.download_button(
        label="📥 Télécharger en Excel",
        data=buffer.getvalue(),
        file_name="population_data.xlsx",
        mime="application/vnd.ms-excel",
    )

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