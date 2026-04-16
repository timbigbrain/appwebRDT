import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px # <--- Nouveau : pour le graphique

# --- CONFIGURATION ET BASE DE DONNÉES ---
st.set_page_config(page_title="Gestion Tilleuls", layout="wide")
if "keep_alive" not in st.session_state:
    st.session_state["keep_alive"] = datetime.now()

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
            st.subheader("😆 Animation Spécifique")
            m7 = st.checkbox("Revue de presse")
            m8 = st.checkbox("Chauffe-citron")
            m9 = st.checkbox("Loto")
            
        st.divider()
        obs = st.text_area("Observations particulières (comportement, incident, chute...)")
        
        submit = st.form_submit_button("✅ Valider l'enregistrement", use_container_width=True)
        
        if submit:
            maintenant = datetime.now()
            checks = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
            labels = ["Toilette", "Habillage", "Hydratation", "Repas", "Animation", "Accompagnement", "Revue de presse", "Chauffe-citron", "Loto"]
            
            missions_list = [label for m, label in zip(checks, labels) if m]
            nb_missions = len(missions_list)
            missions_str = ", ".join(missions_list)

            if nb_missions >= 5:
                st.success(f"🌟 Excellent travail ! {nb_missions} missions accomplies.")
            elif 2 <= nb_missions <= 4:
                st.warning(f"⚠️ Journée validée : {nb_missions} missions accomplies.")
            else:
                st.error(f"ℹ️ Attention : seulement {nb_missions} mission(s) enregistrée(s).")

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
            # --- NOUVEAU : GRAPHIQUE DE PROGRESSION ---
            st.divider()
            st.subheader("📈 Progression de Thierry")
            
            # On filtre les données pour Thierry uniquement
            df_thierry = df[df['employe'] == "Thierry"].copy()
            
            if not df_thierry.empty:
                # On compte le nombre de missions pour chaque ligne
                # On sépare la chaîne de caractères (virgules) et on compte les éléments
                df_thierry['nb_missions'] = df_thierry['missions'].apply(lambda x: len(x.split(',')) if x else 0)
                
                # Création du graphique avec Plotly
                fig = px.line(
                    df_thierry.sort_values('id'), # Tri par ID pour l'ordre chronologique
                    x='date', 
                    y='nb_missions',
                    title="Nombre de missions réalisées par jour",
                    markers=True,
                    line_shape="spline",
                    color_discrete_sequence=["#2E7D32"] # Un beau vert
                )
                
                fig.update_layout(yaxis_range=[0, 10]) # On bloque l'échelle de 0 à 10
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pas encore de données pour Thierry pour générer le graphique.")

            st.divider()
            st.subheader("📋 Historique complet")
            st.dataframe(df, use_container_width=True)
            
            # Export CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger CSV (1 fois par semaine)", data=csv, file_name="export.csv", mime="text/csv")
            
            # --- ZONE DE SUPPRESSION ---
            st.divider()
            with st.expander("🗑️ Supprimer une ligne spécifique"):
                id_a_supprimer = st.number_input("ID à effacer", min_value=1, step=1)
                if st.button("Confirmer la suppression"):
                    conn = sqlite3.connect('suivi_tilleuls.db')
                    c = conn.cursor()
                    c.execute('DELETE FROM interventions WHERE id = ?', (id_a_supprimer,))
                    conn.commit()
                    conn.close()
                    st.success(f"Ligne {id_a_supprimer} supprimée.")
                    st.rerun()
        else:
            st.info("Aucune donnée enregistrée.")
    elif password != "":
        st.error("Code incorrect")
