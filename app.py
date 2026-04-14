import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Gestion Tilleuls", layout="wide")

# Connexion au Google Sheet (utilise les Secrets que tu as remplis)
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données pour l'historique
try:
    df_existant = conn.read(ttl=0)
except:
    df_existant = pd.DataFrame(columns=["Date", "Heure", "Employe", "Missions", "Observations"])

# --- NAVIGATION PAR ONGLETS ---
tab1, tab2 = st.tabs(["📝 Saisie Agent", "📊 Espace Direction"])

# ---------------------------------------------------------
# ONGLET 1 : INTERFACE AGENT
# ---------------------------------------------------------
with tab1:
    st.header("Formulaire de suivi quotidien")
    
    with st.form("form_saisie", clear_on_submit=True):
        nom = st.selectbox("👤 Nom de l'agent", ["Jean", "Marie", "Paul", "Julie"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧼 Soins & Hygiène")
            m1 = st.checkbox("Toilette / Change")
            m2 = st.checkbox("Habillage")
            m3 = st.checkbox("Hydratation")
        with col2:
            st.subheader("🍽️ Vie Sociale & Repas")
            m4 = st.checkbox("Aide au repas")
            m5 = st.checkbox("Animation")
            m6 = st.checkbox("Accompagnement")
            
        obs = st.text_area("Observations particulières")
        
        submit = st.form_submit_button("Valider l'enregistrement", use_container_width=True)
        
        if submit:
            maintenant = datetime.now()
            
            # Liste des missions
            missions = []
            for m, label in zip([m1, m2, m3, m4, m5, m6], ["Toilette", "Habillage", "Hydratation", "Repas", "Animation", "Accompagnement"]):
                if m: missions.append(label)
            
            # Création de la nouvelle ligne
            nouvelle_ligne = pd.DataFrame([{
                "Date": maintenant.strftime("%d/%m/%Y"),
                "Heure": maintenant.strftime("%H:%M"),
                "Employe": nom,
                "Missions": ", ".join(missions),
                "Observations": obs
            }])
            
            # Mise à jour Google Sheets
            df_final = pd.concat([df_existant, nouvelle_ligne], ignore_index=True)
            conn.update(data=df_final)
            
            st.success("Données enregistrées avec succès !")
            st.balloons()

# ---------------------------------------------------------
# ONGLET 2 : ESPACE DIRECTION
# ---------------------------------------------------------
with tab2:
    st.header("Tableau de bord de la Direction")
    
    if not df_existant.empty:
        st.write("Voici l'ensemble des interventions enregistrées :")
        
        # Filtre rapide par employé
        filtre_nom = st.multiselect("Filtrer par agent", options=df_existant["Employe"].unique())
        
        df_display = df_existant
        if filtre_nom:
            df_display = df_existant[df_existant["Employe"].isin(filtre_nom)]
            
        st.dataframe(df_display, use_container_width=True)
        
        # Bouton de téléchargement Excel
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger l'historique en CSV",
            data=csv,
            file_name=f"export_tilleuls_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
        )
    else:
        st.warning("Aucune donnée disponible pour le moment.")
