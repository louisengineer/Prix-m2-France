import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# 1. Charger et nettoyer les données
@st.cache_data
def load_and_clean_data():
    data_path = "dvf.csv"
    DVF = pd.read_csv(data_path, encoding="UTF-8")
    return DVF

# Charger et nettoyer les données
df = load_and_clean_data()

# Interface utilisateur avec Streamlit
st.title("Évolution du Prix au m² en France")

# Sélectionner la commune
communes = df['nom_commune'].unique()
commune_selectionnee = st.selectbox("Sélectionnez une commune :", communes)

# Filtrer les données pour la commune sélectionnée
data_commune = df[df['nom_commune'] == commune_selectionnee]

# Vérifier s'il y a des données
if not data_commune.empty:
    st.subheader(f"Évolution du prix au m² pour : {commune_selectionnee}")
    
    # Séparer les données pour Appartements et Maisons
    data_appartement = data_commune[data_commune['type'] == 'Appartement']
    data_maison = data_commune[data_commune['type'] == 'Maison']
    
    # Prix moyen par année pour les appartements
    prix_m2_annuel_appartement = data_appartement.groupby('annee')['prixm2'].mean().reset_index()
    
    # Prix moyen par année pour les maisons
    prix_m2_annuel_maison = data_maison.groupby('annee')['prixm2'].mean().reset_index()

    # Créer deux colonnes pour l'affichage
    col1, col2 = st.columns(2)
        

    # Graphique interactif pour les Appartements
    with col1:
        st.metric(label="Appartements - Prix au m² moyen", 
                value=f"{prix_m2_annuel_appartement['prixm2'].iloc[-1]:,.0f}€/m²",
                delta=f"{prix_m2_annuel_appartement['prixm2'].pct_change().iloc[-1] * 100:.2f}% depuis 12 mois")

        # Création de la courbe avec zone remplie et points (markers)
        fig_appartement = px.area(prix_m2_annuel_appartement, x='annee', y='prixm2',
                                labels={'annee': 'Année', 'prixm2': 'Prix au m² (€)'},
                                title='Appartements - Prix au m²',
                                markers=True,
                                line_shape='spline')

        # Ajout des informations de survol personnalisées
        fig_appartement.update_traces(hovertemplate='<b>%{x}</b>: %{y:,.0f}€/m²')

        # Mettre à jour les ticks de l'axe des années pour afficher des années pleines
        fig_appartement.update_layout(xaxis=dict(tickmode='linear', tick0=prix_m2_annuel_appartement['annee'].min(), dtick=1),
        yaxis=dict(range=[prix_m2_annuel_appartement['prixm2'].min() * 0.95, prix_m2_annuel_appartement['prixm2'].max() * 1.05])
)

        # Afficher le graphique
        st.plotly_chart(fig_appartement)

    # Graphique interactif pour les Maisons
    with col2:
        st.metric(label="Maisons - Prix au m² moyen", 
                value=f"{prix_m2_annuel_maison['prixm2'].iloc[-1]:,.0f}€/m²",
                delta=f"{prix_m2_annuel_maison['prixm2'].pct_change().iloc[-1] * 100:.2f}% depuis 12 mois")

        # Création de la courbe avec zone remplie et points (markers)
        fig_maison = px.area(prix_m2_annuel_maison, x='annee', y='prixm2',
                            labels={'annee': 'Année', 'prixm2': 'Prix au m² (€)'},
                            title='Maisons - Prix au m²',
                            markers=True,
                            line_shape='spline')

        # Ajout des informations de survol personnalisées
        fig_maison.update_traces(hovertemplate='<b>%{x}</b>, %{y:,.0f}€')

        # Mettre à jour les ticks de l'axe des années pour afficher des années pleines
        fig_maison.update_layout(xaxis=dict(tickmode='linear', tick0=prix_m2_annuel_maison['annee'].min(), dtick=1),
        yaxis=dict(range=[prix_m2_annuel_maison['prixm2'].min() * 0.95, prix_m2_annuel_maison['prixm2'].max() * 1.05])
)

        # Afficher le graphique
        st.plotly_chart(fig_maison)


else:
    st.write("Aucune donnée disponible pour cette commune.")
