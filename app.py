import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Traçabilité Tilleuls", page_icon="🕒")

st.title("🕒 Suivi quotidien")
st.write("Résidence des Tilleuls - CCAS de Vindry-sur-Turdine")

with st.form("suivi_quotidien"):
    nom = st.selectbox("Employé(e)", ["Thierry"])
    
    st.write("---")
    st.subheader("Missions réalisées aujourd'hui :")
    
    # On crée des cases à cocher pour chaque mission
    m1 = st.checkbox("Entretien chambre")
    m2 = st.checkbox("Distribution repas")
    m3 = st.checkbox("Aide à la toilette")
    m4 = st.checkbox("Animation / Activité")
    m5 = st.checkbox("Transmission équipe")
    
    st.write("---")
    commentaire = st.text_area("Observations particulières")
    
    submit = st.form_submit_button("Valider la journée", use_container_width=True)

    if submit:
        # On liste les missions cochées
        missions_faites = []
        if m1: missions_faites.append("Entretien chambre")
        if m2: missions_faites.append("Distribution repas")
        if m3: missions_faites.append("Aide à la toilette")
        if m4: missions_faites.append("Animation")
        if m5: missions_faites.append("Transmission")
        
        date_heure = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        st.success(f"Bravo {nom} ! Tes missions ont été enregistrées à {date_heure}.")
        st.write(f"Actions validées : {', '.join(missions_faites)}")
        st.balloons()
