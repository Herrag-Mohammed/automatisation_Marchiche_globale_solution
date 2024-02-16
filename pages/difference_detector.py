import numpy as np
import pandas as pd 
import streamlit as st
from pathlib import Path
import os
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
#chemin_actuel = current_dir / "main.css"

css_file = os.path.abspath(os.path.join(current_dir, os.pardir, "main.css"))

with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# Afficher l'image dans la barre latérale avec un slider
with st.sidebar:
    st.title("Marchiche Globale Solution")
st.subheader('difference detector', divider='rainbow')
image='logo.jpg'
with st.sidebar:
    st.title("Marchiche Globale Solution")


    # Afficher l'image sélectionnée
    st.image(image, caption='Logo Marchiche Globale Solution', use_column_width=True)

uploaded_file = st.file_uploader("Uploader un fichier CSV", type=['xlsx'])
uploaded_file1 = st.file_uploader("Uploader un fichier CSV", type=['csv'])
if uploaded_file is not None :
    data = pd.read_excel(uploaded_file,sheet_name='Z006-MARCHICHE_GLOBAL_SOLUT_0')
    for i in ['Salaire de Base','CNSS', 'IGR', 'Salaire Brut']:
        data[i]=data[i].astype(str).str.replace(',', '.').astype(float)

if uploaded_file1 is not None:
    data_sage = pd.read_csv(uploaded_file1, encoding='latin1',sep=';')


if uploaded_file1 and uploaded_file: 
    data_sage['Prestations sociales CNSS PS']=data_sage['Prestations sociales CNSS PS'].str.replace(',', '.')
    data_sage['Cotisation AMO PS']=data_sage['Cotisation AMO PS'].str.replace(',', '.')
    data_sage['cnss+amo']=data_sage['Prestations sociales CNSS PS'].astype(float)+data_sage['Cotisation AMO PS'].astype(float)

    for i in ['Salaire de base','cnss+amo','Impôt sur le revenu','Salaire Brut imposable']:
        data_sage[i]=data_sage[i].astype(str).str.replace(',', '.').astype(float)
    x=[]
    for ind,i in enumerate(data_sage.Matricule):
        if data['Net à payer'][data['Ancien matricule']==i].iloc[0] != data_sage['Net à payer'][data_sage.Matricule==i].iloc[0]:
            x.append(i)

    d=data[['Ancien matricule','Salaire de Base','CNSS', 'IGR', 'Salaire Brut']]
    d_sage=data_sage[['Matricule','Salaire de base','cnss+amo','Impôt sur le revenu','Salaire Brut imposable']]



    d_sage = d_sage.rename(columns={
        "Matricule":"Ancien matricule",
        'Salaire de base': 'Salaire de Base',
        'cnss+amo': 'CNSS',
        'Impôt sur le revenu':'IGR',
        'Salaire Brut imposable': 'Salaire Brut'
    })
 

    valid_ids = d['Ancien matricule'].tolist()
    d_sage = d_sage[d_sage['Ancien matricule'].isin(valid_ids)]
    d=d[d['Ancien matricule'].isin(x)]
    d_sage=d_sage[d_sage['Ancien matricule'].isin(x)]

    def compare_and_color(row):
        colors = []
        for col in d.columns:
            val1 = row[col]
            val2 = d_sage.at[row.name, col]
            color = 'black'
            if val1 == val2:
                color = 'green'  # Couleur pour les valeurs =
            elif val1 != val2:
                color = 'red'  # Couleur pour les valeurs !=
            colors.append(f'color: {color}')
        return colors

 
    styled_df1 = d.style.apply(compare_and_color, axis=1)

    tab1, tab2 = st.tabs(["correction par matricules", "matricule introuvable"])
    def save_as_excel(df, filename='dataframe.xlsx'):
        with st.spinner('Enregistrement du fichier...'):
            df.to_excel(filename, index=False)
        st.success(f'Le fichier "{filename}" a été enregistré avec succès!')
    with tab1:
        st.header("correction par matricules")
        st.write(styled_df1)
        if st.button('save to Excel correction par matricules'):
            save_as_excel(styled_df1, filename='output.xlsx')
    with tab2:

        h=set(data['Ancien matricule'])
        h_=set(data_sage['Matricule'])
        diff=h - h_
        st.header("matricule introuvable")
        df=data[data['Ancien matricule'].isin(list(diff))]
        st.write(df)
        if st.button('save to Excel matricule introuvable'):
            save_as_excel(df, filename='output.xlsx')

    st.write("Contenu du fichier CSV :")
    st.write(data)
    st.write("Contenu du fichier CSV :")
    st.write(data_sage)
