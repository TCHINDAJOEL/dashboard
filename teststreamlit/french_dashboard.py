# Importation des modules principaux
import calendar  # Module de base de Python pour les calendriers
from datetime import datetime  # Module de base de Python pour travailler avec les dates et heures
import streamlit as st  # Bibliothèque Streamlit pour la création d'applications web interactives
import plotly.graph_objs as go  # Bibliothèque Plotly pour la création de graphiques interactifs
from streamlit_option_menu import option_menu

# -----------------------PARAMÈTRES-----------------------
# Catégories de revenus et de dépenses
revenus = ["Salaire", "Blog", "Autres Revenus"]
dépenses = ["Loyer", "Services Publics", "Épicerie", "Voiture", "Autres Dépenses", "Épargne"]
# Devise utilisée
devise = "EUR"
# Titre de la page
titre_page = "Suivi des Revenus et Dépenses"
# Icône de la page
icone_page = "💰"  # Vous pouvez utiliser une autre icône de la feuille de triche emoji : https://www.webfx.com/tools/emoji-cheat-sheet/
# Configuration de la mise en page
disposition = "centré"

# ----------------------------------

# Configuration de la page Streamlit avec le titre, l'icône et la mise en page
st.set_page_config(page_title=titre_page, page_icon=icone_page, layout="centered")
# Affichage du titre de la page
st.title(titre_page + " " + icone_page)

# Sélection des années et des mois dans une liste déroulante pour choisir la période
années = [datetime.today().year, datetime.today().year + 1]
mois = list(calendar.month_name[1:])  # Liste des noms des mois (en anglais)

# Menu de navigation avec deux options : "Saisie de Données" et "Visualisation de Données"
sélectionné = option_menu("Menu de Navigation",
                          ["Saisie de Données", "Visualisation de Données"],
                          icons=["pencil-fill", "bar-chart-fill"],  # http://icons.getbootstrap.com/
                          orientation="horizontal"
                          )

# Saisie des données
if sélectionné == "Saisie de Données":
    st.header(f"Saisie de Données en {devise}")
    # Formulaire pour saisir les données de revenus et de dépenses
    with st.form("formulaire_saisie", clear_on_submit=True):
        col1, col2 = st.columns(2)
        # Sélection du mois et de l'année
        col1.selectbox("Sélectionnez le Mois:", mois, key="mois")
        col1.selectbox("Sélectionnez l'Année:", années, key="année")

        "---"
        # Section pour les revenus avec des expanders pour chaque catégorie de revenus
        with st.expander("Revenus"):
            for revenu in revenus:
                st.number_input(f"{revenu}:", min_value=0, format="%i", step=10, key=revenu)
        # Section pour les dépenses avec des expanders pour chaque catégorie de dépenses
        with st.expander("Dépenses"):
            for dépense in dépenses:
                st.number_input(f"{dépense}:", min_value=0, format="%i", step=10, key=dépense)
        # Section pour les commentaires
        with st.expander("Commentaires"):
            commentaire = st.text_area("", placeholder="Saisissez un commentaire ici ...")
        "---"
        # Bouton pour sauvegarder les données
        soumis = st.form_submit_button("Sauvegarder les Données")
        if soumis:
            # Construction de la période (année_mois)
            période = str(st.session_state["année"]) + "_" + str(st.session_state["mois"])
            # Création de dictionnaires pour les revenus et les dépenses à partir des données saisies par l'utilisateur
            revenus = {revenu: st.session_state[revenu] for revenu in revenus}
            dépenses = {dépense: st.session_state[dépense] for dépense in dépenses}

            # TODO : Insérer les valeurs dans une base de données
            # Affichage des revenus et des dépenses sauvegardés
            st.write(f"Revenus: {revenus}")
            st.write(f"Dépenses: {dépenses}")
            st.success("Données sauvegardées !")

# Visualisation des données
if sélectionné == "Visualisation de Données":
    st.header("Visualisation de Données")
    # Formulaire pour sélectionner la période à visualiser
    with st.form("Données Sauvegardées"):
        # TODO: Récupérer les périodes à partir de la base de données
        période = st.selectbox("Sélectionnez la Période:", ["2024_Mars"])
        soumis = st.form_submit_button("Afficher les Données")
        if soumis:
            # TODO: Obtenir les données de la base de données pour la période sélectionnée
            revenus = {'Salaire': 1500, 'Blog': 50, 'Autres Revenus': 10}
            dépenses = {'Loyer': 600, 'Services Publics': 200, 'Épicerie': 300,
                        'Voiture': 100, 'Autres Dépenses': 50, 'Épargne': 150}

            # Création des métriques
            total_revenus = sum(revenus.values())
            total_dépenses = sum(dépenses.values())
            solde_restant = total_revenus - total_dépenses
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Revenus", f"{total_revenus} {devise}")
            col2.metric("Total Dépenses", f"{total_dépenses} {devise}")
            col3.metric("Solde Restant", f"{solde_restant} {devise}")

            # Création du diagramme Sankey
            libellé = list(revenus.keys()) + ["Total Revenus"] + list(dépenses.keys())
            source = list(range(len(revenus))) + [len(revenus)] * len(dépenses)
            target = [len(revenus)] * len(revenus) + [libellé.index(dépense) for dépense in dépenses]
            valeur = list(revenus.values()) + list(dépenses.values())

            # Création du dictionnaire de données pour le diagramme Sankey
            lien = dict(source=source, target=target, value=valeur)
            noeud = dict(label=libellé, pad=15, thickness=20, color="#E695FF")

            # Création du diagramme Sankey
            fig = go.Figure(data=[go.Sankey(
                node=noeud,
                link=lien
            )])

            # Mise en forme du titre du diagramme
            fig.update_layout(title_text="Diagramme Sankey des Revenus et Dépenses", font_size=10)

            # Affichage du diagramme Sankey
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
