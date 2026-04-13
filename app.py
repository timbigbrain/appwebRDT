import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Traçabilité Tilleuls", layout="wide")

st.title("🕒 Suivi des interventions (Sauvegarde Cloud)")

# Connexion au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données existantes
df_existant = conn.read(ttl=0) # ttl=0 pour forcer la mise à jour immédiate

with st.form("form_interventions", clear_on_submit=True):
    nom = st.selectbox("👤 Employé(e)", ["Jean", "Marie", "Paul", "Julie"])
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🧼 Soins")
        h1 = st.checkbox("Toilette")
        h2 = st.checkbox("Habillage")
    with col2:
        st.subheader("🍽️ Repas")
        r1 = st.checkbox("Aide repas")
        r2 = st.checkbox("Goûter")
    with col3:
        st.subheader("🏠 Confort")
        c1 = st.checkbox("Lit")
        c2 = st.checkbox("Animation")

    commentaire = st.text_area("📝 Observations")
    submit = st.form_submit_button("✅ Enregistrer dans Google Sheets", use_container_width=True)

    if submit:
        # Préparation de la nouvelle ligne
        maintenant = datetime.now()
        date = maintenant.strftime("%d/%m/%Y")
        heure = maintenant.strftime("%H:%M")
        
        missions_list = [m for m, checked in zip(["Toilette", "Habillage", "Repas", "Goûter", "Lit", "Animation"], [h1, h2, r1, r2, c1, c2]) if checked]
        
        nouvelle_donnee = pd.DataFrame([{
            "Date": date,
            "Heure": heure,
            "Employe": nom,
            "Missions": ", ".join(missions_list),
            "Observations": commentaire
        }])

        # Fusion avec l'ancien tableau et mise à jour
        df_mis_a_jour = pd.concat([df_existant, nouvelle_donnee], ignore_index=True)
        conn.update(data=df_mis_a_jour)
        
        st.success(f"Données envoyées sur Google Sheets ! Bravo {nom}.")
        st.snow()

# Affichage de l'historique en direct du Google Sheet
st.divider()
st.subheader("📊 Historique en temps réel (Google Sheets)")
st.dataframe(df_existant, use_container_width=True)
