import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Traçabilité Tilleuls", layout="wide")

# ID de ton Google Sheet (celui que j'ai extrait de ton message précédent)
SHEET_ID = "1HHBEDLQX0K62C9q77RLB10BoX5EeEQCdEL1UsDEuYGk"
# URL de lecture robuste
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# --- CHARGEMENT DES DONNÉES ---
try:
    # On essaie de lire le Google Sheet
    df_existant = pd.read_csv(url)
except Exception as e:
    # Si ça plante (problème de partage), on crée un tableau vide pour ne pas bloquer l'appli
    st.error(f"Erreur de connexion au Google Sheet : {e}")
    df_existant = pd.DataFrame(columns=["Date", "Heure", "Employe", "Missions", "Observations"])

st.title("🕒 Suivi des interventions")
st.write("Résidence des Tilleuls - CCAS de Vindry-sur-Turdine")

# --- FORMULAIRE ---
with st.form("form_complet", clear_on_submit=True):
    nom = st.selectbox("👤 Employé(e)", ["Jean", "Marie", "Paul", "Julie"])
    
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🧼 Soins")
        h1 = st.checkbox("Toilette")
        h2 = st.checkbox("Habillage")
        h3 = st.checkbox("Change")

    with col2:
        st.subheader("🍽️ Repas")
        r1 = st.checkbox("Aide repas")
        r2 = st.checkbox("Distribution goûter")
        r3 = st.checkbox("Installation salle")

    with col3:
        st.subheader("🏠 Confort & Social")
        c1 = st.checkbox("Réfection du lit")
        c2 = st.checkbox("Entretien chambre")
        c3 = st.checkbox("Animation / Écoute")

    st.divider()
    commentaire = st.text_area("📝 Observations (comportement, chute, refus de soin...)")
    
    submit = st.form_submit_button("✅ Valider l'enregistrement", use_container_width=True)

    if submit:
        # Préparation de l'heure et date
        maintenant = datetime.now()
        date_j = maintenant.strftime("%d/%m/%Y")
        heure_j = maintenant.strftime("%H:%M")
