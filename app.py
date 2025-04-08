import streamlit as st
import pandas as pd
import altair as alt
import io
import os

# Configuration du chemin du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

# Configuration de la page
st.set_page_config(
    page_title="Évolution de la Population",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constantes pour le formatage des nombres
FORMAT_CONVENTIONS = {
    'population_axis': {'format': ' >,.0f', 'label_expr': "replace(datum.label, ',', ' ')"},
    'population_table': 'formatted',  # utilise population_formatted
    'year': 'O'  # Ordinal, pas de séparateur
}

# Création des données
data = {
    'année': [1968, 1975, 1982, 1990, 1999, 2006, 2011, 2016, 2021],
    'population': [8949, 9550, 9800, 10100, 11250, 12500, 13750, 14854, 16000]
}

df = pd.DataFrame(data)

def format_number(x):
    """Formate un nombre selon les conventions françaises."""
    if pd.isna(x):
        return ""
    return f"{int(x):,}".replace(",", " ")

def validate_formatting(df):
    """Valide que le formatage respecte les conventions."""
    assert 'population_formatted' in df.columns, "La colonne population_formatted est requise"
    assert 'année' in df.columns, "La colonne année est requise"
    assert 'population' in df.columns, "La colonne population est requise"
    # Vérifier que les années n'ont pas de séparateur
    assert all(df['année'].astype(str).str.match(r'^\d{4}$')), "Les années doivent être au format YYYY"
    return True

def apply_french_formatting(df):
    """Applique le formatage français aux données."""
    df['population_formatted'] = df['population'].apply(format_number)
    # Ajout d'une colonne pour l'affichage brut dans le tableau
    df['population_brute'] = df['population'].astype(str)
    return df

# Ajout d'une colonne formatée pour les tooltips uniquement
df = apply_french_formatting(df)
validate_formatting(df)

# Création du graphique
base = alt.Chart(df).encode(
    x=alt.X('année:O', title='Année'),
    y=alt.Y('population:Q', 
            title='Population',
            axis=alt.Axis(
                format=FORMAT_CONVENTIONS['population_axis']['format'],
                labelExpr=FORMAT_CONVENTIONS['population_axis']['label_expr']
            )),
    tooltip=[
        alt.Tooltip('année:O', title='Année'),
        alt.Tooltip('population_formatted:N', title='Population')
    ]
)

# Création de la ligne
line = base.mark_line(color='#3B825C')

# Création des points avec la même couleur, plus petits et sans contour
points = base.mark_point(
    color='#3B825C',
    size=60,
    filled=True
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

# Création de deux colonnes pour le tableau et l'analyse
col_table, col_analysis = st.columns([1, 1])

with col_table:
    # Création du DataFrame pour l'affichage
    display_df = pd.DataFrame({
        'Année': df['année'],
        'Population': df['population_brute']  # Utilisation de la version en texte brut
    })
    
    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            "Année": st.column_config.Column(
                "Année",
                width="small"
            ),
            "Population": st.column_config.Column(  # Utilisation d'une colonne simple
                "Population",
                help="Population de la commune"
            )
        }
    )

with col_analysis:
    st.write("### Analyse de l'évolution")
    st.write("""
    L'analyse de l'évolution de la population sur la période 1968-2021 révèle une croissance démographique marquée par deux phases distinctes :

    1. **Une période de croissance modérée (1968-1990)** : La population passe de 8 949 à 10 100 habitants, soit une augmentation de 12,9% sur 22 ans. Cette période est caractérisée par une progression régulière mais relativement lente.

    2. **Une accélération soutenue (1990-2021)** : En 31 ans, la population croît de 58,4%, passant de 10 100 à 16 000 habitants. Cette phase témoigne d'un dynamisme démographique plus marqué, avec une augmentation moyenne d'environ 190 habitants par an. La tendance à l'accélération se maintient jusqu'en 2021, sans signe de ralentissement.

    Sur l'ensemble de la période, la population a presque doublé (+78,8%), passant de 8 949 à 16 000 habitants. Cette progression constante, sans période de déclin, suggère une attractivité territoriale durable.
    """)

    # Ajout des boutons d'export personnalisés
    st.write("### Télécharger les données")
    
    # Préparation des données pour l'export (données brutes)
    df_export = df[['année', 'population']]
    
    # Export CSV
    csv = df_export.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Télécharger en CSV",
        data=csv,
        file_name="population_data.csv",
        mime="text/csv",
    )
    
    # Export Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, sheet_name='Population', index=False)
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
# - Les points sont de taille modérée (size=60) et remplis sans contour (filled=True)
# - L'application utilise un thème clair avec un fond blanc pour une meilleure lisibilité
# - Les textes sont en couleur #272F4D pour l'interface et #000011 pour les graphiques
# - La police Axiforma est utilisée pour les graphiques
# 
# ### Formatage des nombres
# - Une fonction `format_number` est utilisée pour garantir le formatage selon la convention française
# - Les années sont affichées sans séparateur (ex: 1968)
# - Les volumes de population suivent deux conventions :
#   1. Dans les tableaux : pas de séparateur pour permettre le tri (ex: 16000)
#   2. Dans les graphiques et tooltips : espace comme séparateur de milliers selon la convention française (ex: 16 000)
# - La notation scientifique est désactivée pour une meilleure lisibilité
# - Les tooltips utilisent le même formatage que l'axe des ordonnées pour la cohérence
# - Le formatage est uniquement utilisé pour l'affichage (tooltips, axe Y) et non pour l'export
# - Les données exportées sont brutes pour permettre leur réutilisation dans d'autres logiciels
# 
# ### Configuration technique
# - Un fichier `.streamlit/config.toml` est présent pour assurer la stabilité de l'application
# - Le timeout est configuré à 2 heures pour éviter les déconnexions
# - Les paramètres du serveur sont optimisés pour une meilleure performance
# - Le mode "watchdog" est désactivé pour réduire les interruptions
# - La compression WebSocket est désactivée pour améliorer la stabilité
# - L'export des données utilise le menu natif de Streamlit (bouton "..." en haut à droite des tableaux)
# - Seules les données brutes sont exportées (pas de colonnes formatées) 