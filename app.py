import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Traçabilité Tilleuls", layout="wide") # "wide" utilise tout l'écran

st.title("🕒 Feuille de route quotidienne")
st.write("Résidence des Tilleuls - CCAS de Vindry-sur-Turdine")

with st.form("form_complet"):
    nom = st.selectbox("👤 Employé(e)", ["[Thierry]")
    
    st.divider()
    
    # Création de 3 colonnes pour gagner de la place
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🧼 Soins & Hygiène")
        h1 = st.checkbox("Toilette")
        h2 = st.checkbox("Habillage")
        h3 = st.checkbox("Change")
        h4 = st.checkbox("Hydratation")

    with col2:
        st.subheader("🍽️ Repas")
        r1 = st.checkbox("Aide au repas")
        r2 = st.checkbox("Distribution goûter")
        r3 = st.checkbox("Installation salle")
        r4 = st.checkbox("Débarrassage")

    with col3:
        st.subheader("🏠 Confort & Social")
        c1 = st.checkbox("Réfection du lit")
        c2 = st.checkbox("Entretien chambre")
        c3 = st.checkbox("Animation / Écoute")
        c4 = st.checkbox("Accompagnement")

    st.divider()
    commentaire = st.text_area("📝 Observations (comportement, chute, refus de soin...)")
    
    submit = st.form_submit_button("✅ Valider la journée", use_container_width=True)

    if submit:
        maintenant = datetime.now()
        date = maintenant.strftime("%d/%m/%Y")
        heure = maintenant.strftime("%H:%M")
        
        st.success(f"Bravo {nom} ! Tes missions ont été enregistrées le {date} à {heure}.")
        st.balloons()
