import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('suivi_residence.db')
    c = conn.cursor()
    # On crée la table si elle n'existe pas encore
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

st.set_page_config(page_title="Traçabilité Tilleuls", layout="wide")

st.title("🕒 Suivi des interventions")

# --- FORMULAIRE DE SAISIE ---
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
    
    submit = st.form_submit_button("✅ Enregistrer")

    if submit:
        # 1. On prépare les données
        maintenant = datetime.now()
        date = maintenant.strftime("%d/%m/%Y")
        heure = maintenant.strftime("%H:%M")
        
        # Liste des missions cochées
        missions_list = []
        if h1: missions_list.append("Toilette")
        if h2: missions_list.append("Habillage")
        if r1: missions_list.append("Aide repas")
        if r2: missions_list.append("Goûter")
        if c1: missions_list.append("Lit")
        if c2: missions_list.append("Animation")
        missions_finales = ", ".join(missions_list)

        # 2. On écrit dans la base SQL
        conn = sqlite3.connect('suivi_residence.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO interventions (date, heure, employe, missions, observations)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, heure, nom, missions_finales, commentaire))
        conn.commit()
        conn.close()

        st.success(f"Enregistré le {date} à {heure}")
        st.balloons()

# --- PARTIE HISTORIQUE (POUR LE TUTEUR) ---
st.divider()
st.subheader("📊 Historique des dernières 24h")

conn = sqlite3.connect('suivi_residence.db')
# On récupère les données avec Pandas (très puissant pour les tableaux)
df = pd.read_sql_query("SELECT date, heure, employe, missions, observations FROM interventions ORDER BY id DESC", conn)
conn.close()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune donnée enregistrée pour le moment.")
