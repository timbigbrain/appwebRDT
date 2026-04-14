import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURATION ET BASE DE DONNÉES ---
st.set_page_config(page_title="Gestion Tilleuls", layout="wide")

def init_db():
    conn = sqlite3.connect('suivi_tilleuls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            heure TEXT,
            employe TEXT,
            missions TEXT,
            observations TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
            
        obs = st.text_area("Observations particulières (comportement, incident...)")
        
        submit = st.form_submit_button("✅ Valider l'enregistrement", use_container_width=True)
        
        if submit:
            maintenant = datetime.now()
            date_j = maintenant.strftime("%d/%m/%Y")
            heure_j = maintenant.strftime("%H:%M")
            
            # Liste des missions
            missions_faites = []
            labels = ["Toilette", "Habillage", "Hydratation", "Repas", "Animation", "Accompagnement"]
            for m, label in zip([m1, m2, m3, m4, m5, m6], labels):
                if m: missions_faites.append(label)
            
            missions_str = ", ".join(missions_faites)

            # Sauvegarde en SQLite
            conn = sqlite3.connect('suivi_tilleuls.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO interventions (date, heure, employe, missions, observations)
                VALUES (?, ?, ?, ?, ?)
            ''', (date_j, heure_j, nom, missions_str, obs))
            conn.commit()
            conn.close()
            
            st.success(f"Enregistré avec succès ! (Date: {date_j} à {heure_j})")
            st.snow()

# ---------------------------------------------------------
# ONGLET 2 : ESPACE DIRECTION
# ---------------------------------------------------------
with tab2:
    st.header("Tableau de bord de la Direction")
    
    conn = sqlite3.connect('suivi_tilleuls.db')
    df = pd.read_sql_query("SELECT * FROM interventions ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        # Filtre par agent
        agents = df["employe"].unique().tolist()
        filtre = st.multiselect("Filtrer par agent :", agents)
        
        df_final = df
        if filtre:
            df_final = df[df["employe"].isin(filtre)]
            
        st.dataframe(df_final, use_container_width=True)
        
        # Bouton de téléchargement pour Excel
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger l'historique en CSV (Excel)",
            data=csv,
            file_name=f"export_tilleuls_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aucune donnée enregistrée pour le moment.")
