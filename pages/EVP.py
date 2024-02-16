import pandas as pd 
import numpy as np 
import streamlit as st
import os
from pathlib import Path

image_path = "logo.jpg"
image = open(image_path, 'rb').read()
st.markdown(
    """
    <style>
        .css-1b9kyan {
            width: 100px;  /* Ajustez cette valeur selon vos besoins */
        }
    </style>
    """,
    unsafe_allow_html=True,
)




with st.sidebar:
    st.title("Marchiche Globale Solution")


    # Afficher l'image sélectionnée
    st.image(image, caption='Logo Marchiche Globale Solution', use_column_width=True)
st.subheader('EVP', divider='rainbow')

N={
   'Nombre Heures supplémentaires 100 %' :'HNORMA',
   'Nombre Heures supplémentaires 125 %' :'HRS125',
   'Nombre Heures supplémentaires 150 %' :'HRS150',
   'Nombre Heures supplémentaires 200 %' :'HRS200',
   'Indemnité de Panier':'PRPANN'
}

M1={
    'Rappel Sur Salaire':'RAPBAS',
    'Indemnité de transport':'INDTRA',
    'Indemnité de représentation':'INDREP',
    'Indemnité kilométrique':'INDKIL',
    #'Indemnité de déplacement':'INDEP',
    'Commission':'PRIICA',
    'Primes de Logement':'PRIALO',
    'Indemnité de téléphone':'INTEL',
    'Indemnité d\'Internet':'INDIN',
    'Indemnité de voiture':'PRIASP',
    'Prime de signature':'PRSIG',
    'Prime Spécial':'PRSPE',
    'Prime Annuel':'PRIAN',
    'Prime Divers':'PRDIV',
    'Indemnité de retraite':'INRET',
    'Indemnité médicale':'PRAMSI',
    'Indemnité de carburant':'INDCA',
    'Indemnité de travail à domicil':'INDTD',
    'Avantages en nature':'ANLOGE',
    'Prime de voyage':'PRIVYP',
    'Indemnité de licenciement':'INDLIC',
    'Dommages Et Intérêts':'INLIDO',
    'Cotisation retraite Complément':'C3RETH',
    'Retenu Avantages en Nature':'RAVNA'
}
N = {str(key.lower().strip()): value for key, value in N.items()}
M1 = {str(key.lower().strip()): value for key, value in M1.items()}

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = True

extention = st.radio(
        "selectionner la bonne extention 👇",
        ["xlsx", "CSV"],
        key="xlsx",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        horizontal=st.session_state.horizontal,
    )
uploaded_file = st.file_uploader(f"Uploader un fichier {extention}", type=[extention])
x,y=True,True

def obtenir_noms_feuilles(fichier_excel):
    try:
        # Utiliser la fonction ExcelFile de pandas pour obtenir les noms des feuilles sans charger le fichier entier
        with pd.ExcelFile(fichier_excel) as xls:
            noms_feuilles = xls.sheet_names
        return noms_feuilles
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None


if uploaded_file: 
    if extention == 'xlsx':
        on = st.toggle('sheet_name')
        if on:
            
           
            sn=  st.text_input('sheet_name', '')
            
            
            if sn in obtenir_noms_feuilles(uploaded_file):
                
                data_TeamsRH=pd.read_excel(uploaded_file,sheet_name=sn)
                
                
                
            else:
                st.error('saisie corectement le nom de sheet excel')
                x=False
               
        
        else:
            data_TeamsRH=pd.read_excel(uploaded_file)
    else:
        on = st.toggle('encoding --> latin1')
        if on:
            data_TeamsRH = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            data_TeamsRH = pd.read_csv(uploaded_file)
    if x==True and y==True:
        
            
        col_data_TeamsRH={i: str(i.strip().lower()) for i in data_TeamsRH.columns}
        data_TeamsRH.rename(columns=col_data_TeamsRH, inplace = True)
        st.write(data_TeamsRH.head())

        

    ##======================================================================##



        M1_col =set(M1.keys())
        N_col =set(N.keys())
        tot=list(M1_col | N_col)
        mmat=st.selectbox('mmat',
                            list(data_TeamsRH.columns),
                            index=1,
                            placeholder="Sélectionnez la colonne qui corespondent le matricule...",key=f"{188}")
        total=list(M1_col | N_col|{mmat})
        
        #total=list(total)

        
    

        data_TeamsRH=data_TeamsRH[total]
        data_TeamsRH['indemnité de panier']=data_TeamsRH['indemnité de panier']/10

        ##################

        # Création d'un DataFrame vide
        data = pd.DataFrame(columns=['MCLI', 'MMAT', 'MCONTRAT', 'MITEM', 'MVERSION', 'MRUB', 'N', 'T1', 'M1', 'TYPE'])
        
        # Listes pour stocker les nouvelles lignes
        new_rows = []

        for ind in data_TeamsRH[mmat].unique():
            for col in tot:
                if col in M1.keys():
                    if data_TeamsRH[data_TeamsRH[mmat] == ind][col].iloc[0] != 0.0:  

                        m1 = data_TeamsRH[col][data_TeamsRH[mmat] == ind].iloc[0]
                        nouvelle_ligne = pd.Series({
                            'MCLI': 'Z006', 'MMAT': ind, 'MCONTRAT': 1, 'MITEM': 0, 'MVERSION': 1,
                            'MRUB': M1[col], 'N': '', 'T1': '', 'M1': m1, 'TYPE': '$unit'
                        }, index=data.columns)
                        new_rows.append(nouvelle_ligne)
                else:
                    if data_TeamsRH[col][data_TeamsRH[mmat] == ind].iloc[0] != 0.0:
                        n = data_TeamsRH[col][data_TeamsRH[mmat] == ind].iloc[0]
                        nouvelle_ligne = pd.Series({
                            'MCLI': 'Z006', 'MMAT': ind, 'MCONTRAT': 1, 'MITEM': 0, 'MVERSION': 1,
                            'MRUB': N[col], 'N': n, 'T1': '', 'M1': '', 'TYPE': '$unit'
                        }, index=data.columns)
                        new_rows.append(nouvelle_ligne)


        # Ajout de toutes les nouvelles lignes au DataFrame en utilisant concat
        for i in range(len(new_rows)):
            data.loc[i]=list(new_rows)[i]

        #######################
        st.write('Resultat :',data)
        
        @st.cache_data
        def convert_df(df,t):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_excel(f"{t}.xlsx",index=False)
        #exel = convert_df(data)
        t=st.text_input('inserer')
        if t != '':
            if st.button("Download data as excel", type="primary"):
                convert_df(data,t)
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#chemin_actuel = current_dir / "main.css"

css_file = os.path.abspath(os.path.join(current_dir, os.pardir, "main.css"))
with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# Afficher l'image dans la barre latérale avec un slider

