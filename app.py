import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🚴 Chronométrage Course Vélo")

# Initialisation
if "passages" not in st.session_state:
    st.session_state.passages = pd.DataFrame(columns=["dossard","tour","temps"])

if "engages" not in st.session_state:
    st.session_state.engages = None

# Upload engagés
file = st.file_uploader("Importer les engagés", type=["csv","xlsx"])

if file:
    if file.name.endswith(".csv"):
        st.session_state.engages = pd.read_csv(file)
    else:
        st.session_state.engages = pd.read_excel(file)

# Paramètres
nb_tours = st.number_input("Nombre de tours", min_value=1, value=5)

# Saisie
dossard = st.text_input("Dossard")

if st.button("Valider"):
    if st.session_state.engages is None:
        st.error("Importer les engagés")
    elif not dossard.isdigit():
        st.error("Dossard invalide")
    else:
        d = int(dossard)

        if d not in st.session_state.engages["dossard"].values:
            st.error("Dossard inconnu")
        else:
            df = st.session_state.passages
            tours = df[df["dossard"]==d].shape[0]

            if tours >= nb_tours:
                st.warning("Déjà terminé")
            else:
                new = {"dossard":d,"tour":tours+1,"temps":datetime.now()}
                st.session_state.passages = pd.concat([df, pd.DataFrame([new])])
                st.success(f"Tour {tours+1} enregistré")

# Classement
if not st.session_state.passages.empty:
    classement = st.session_state.passages.groupby("dossard")["tour"].max().reset_index()
    classement = classement.sort_values("tour", ascending=False)
    st.subheader("Classement")
    st.dataframe(classement)
