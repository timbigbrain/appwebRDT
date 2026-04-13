import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Traçabilité Tilleuls", page_icon="🕒")

st.title("🕒 Suivi des interventions")
st.write("Résidence des Tilleuls - CCAS de Vindry-sur-Turdine")

# --- INTERFACE DE SAISIE ---
with st.container(border=True):
    nom = st.selectbox("Employé(e)", ["Jean", "Marie", "Paul", "Julie"])
    action = st.selectbox("Tâche réalisée", [
        "Entretien chambre", 
        "Distribution repas", 
        "Aide à la toilette", 
        "Animation",
        "Autre"
    ])
    commentaire = st.text_area("Observations")
    
    if st.button("Valider l'enregistrement", use_container_width=True):
        date_heure = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Pour l'instant on affiche, l'étape suivante sera de sauvegarder
        st.success(f"Enregistré ! {nom} - {action} à {date_heure}")
        st.balloons()

# --- HISTORIQUE (Aperçu) ---
st.divider()
st.subheader("Dernières interventions")
st.info("Les données seront bientôt sauvegardées dans une base de données SQL.")
