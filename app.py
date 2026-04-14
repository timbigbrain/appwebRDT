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
        nom = st.selectbox("👤 Nom de l'agent", ["Thierry", "Marie", "Jean"])
        
        # Correction : On définit bien les 3 colonnes ici
        col1, col2, col3 = st.columns(3)
        
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
            
        with col3:
            st.subheader("😆 Animation")
            m7 = st.checkbox("Revue de presse")
            m8 = st.checkbox("Chauffe-citron")
            m9 = st.checkbox("Loto")
            
        st.divider()
        obs = st.text_area("Observations particulières (comportement, incident...)")
        
        submit = st.form_submit_button("✅ Valider l'enregistrement", use_container_width=True)
        
        if submit:
            maintenant = datetime.now()
            
            # Liste de TOUTES les missions pour le calcul
            checks = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
            labels = ["Toilette", "Habillage", "Hydratation", "Repas", "Animation", "Accompagnement", "Revue de presse", "Chauffe-citron", "Loto"]
            
            missions_list = []
            for m, label in zip(checks, labels):
                if m: missions_list.append(label)
            
            nb_missions = len(missions_list)
            missions_str = ", ".join(missions_list)

            # --- LOGIQUE DES COULEURS ---
            if nb_missions >= 5:
                st.success(f"🌟 Excellent travail ! {nb_missions} missions accomplies.")
            elif 2 <= nb_missions <= 4:
                st.warning(f"⚠️ Journée validée : {nb_missions} missions accomplies.")
            else:
                st.error(f"ℹ️ Attention : seulement {nb_missions} mission(s) enregistrée(s).")

            # Sauvegarde en base de données
            conn = sqlite3.connect('suivi_tilleuls.db')
            c = conn.cursor()
            c.execute('INSERT INTO interventions (date, heure, employe, missions, observations) VALUES (?, ?, ?, ?, ?)',
                      (maintenant.strftime("%d/%m/%Y"), maintenant.strftime("%H:%M"), nom, missions_str, obs))
            conn.commit()
            conn.close()
            
            st.toast(f"Données envoyées à la direction !")

# ---------------------------------------------------------
# ONGLET 2 : ESPACE DIRECTION (SÉCURISÉ)
# ---------------------------------------------------------
with tab2:
    st.header("🔐 Accès Restreint")
    
    password = st.text_input("Veuillez entrer le code d'accès direction", type="password")
    
    if password == "123":
        st.success("Accès autorisé")
        
        conn = sqlite3.connect('suivi_tilleuls.db')
        df = pd.read_sql_query("SELECT * FROM interventions ORDER BY id DESC", conn)
        conn.close()
        
        if not df.empty:
            st.subheader("Historique des interventions")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV (Excel)", data=csv, file_name="export_tilleuls.csv", mime="text/csv")
        else:
            st.info("Aucune donnée enregistrée.")
    elif password != "":
        st.error("Code incorrect")import streamlit as st
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
        nom = st.selectbox("👤 Nom de l'agent", ["Thierry", "Marie", "Jean"])
        
        # Correction : On définit bien les 3 colonnes ici
        col1, col2, col3 = st.columns(3)
        
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
            
        with col3:
            st.subheader("😆 Animation")
            m7 = st.checkbox("Revue de presse")
            m8 = st.checkbox("Chauffe-citron")
            m9 = st.checkbox("Loto")
            
        st.divider()
        obs = st.text_area("Observations particulières (comportement, incident...)")
        
        submit = st.form_submit_button("✅ Valider l'enregistrement", use_container_width=True)
        
        if submit:
            maintenant = datetime.now()
            
            # Liste de TOUTES les missions pour le calcul
            checks = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
            labels = ["Toilette", "Habillage", "Hydratation", "Repas", "Animation", "Accompagnement", "Revue de presse", "Chauffe-citron", "Loto"]
            
            missions_list = []
            for m, label in zip(checks, labels):
                if m: missions_list.append(label)
            
            nb_missions = len(missions_list)
            missions_str = ", ".join(missions_list)

            # --- LOGIQUE DES COULEURS ---
            if nb_missions >= 5:
                st.success(f"🌟 Excellent travail ! {nb_missions} missions accomplies.")
            elif 2 <= nb_missions <= 4:
                st.warning(f"⚠️ Journée validée : {nb_missions} missions accomplies.")
            else:
                st.error(f"ℹ️ Attention : seulement {nb_missions} mission(s) enregistrée(s).")

            # Sauvegarde en base de données
            conn = sqlite3.connect('suivi_tilleuls.db')
            c = conn.cursor()
            c.execute('INSERT INTO interventions (date, heure, employe, missions, observations) VALUES (?, ?, ?, ?, ?)',
                      (maintenant.strftime("%d/%m/%Y"), maintenant.strftime("%H:%M"), nom, missions_str, obs))
            conn.commit()
            conn.close()
            
            st.toast(f"Données envoyées à la direction !")

# ---------------------------------------------------------
# ONGLET 2 : ESPACE DIRECTION (SÉCURISÉ)
# ---------------------------------------------------------
with tab2:
    st.header("🔐 Accès Restreint")
    
    password = st.text_input("Veuillez entrer le code d'accès direction", type="password")
    
    if password == "123":
        st.success("Accès autorisé")
        
        conn = sqlite3.connect('suivi_tilleuls.db')
        df = pd.read_sql_query("SELECT * FROM interventions ORDER BY id DESC", conn)
        conn.close()
        
        if not df.empty:
            st.subheader("Historique des interventions")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV (Excel)", data=csv, file_name="export_tilleuls.csv", mime="text/csv")
     else:
            st.info("Aucune donnée enregistrée.")
    elif password != "":
        st.error("Code incorrect")
# FIN DU FICHIER (ne rien ajouter ici)
