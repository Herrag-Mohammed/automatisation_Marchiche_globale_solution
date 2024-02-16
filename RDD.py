import pandas as pd 
import numpy as np 
import streamlit as st 
import re
from unidecode import unidecode
from fuzzywuzzy import fuzz
from pathlib import Path
import subprocess

# Installation de la dépendance openpyxl
subprocess.call(['pip', 'install', 'openpyxl'])
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

# Afficher l'image dans la barre latérale avec un slider
with st.sidebar:
    st.title("Marchiche Globale Solution")
    # Afficher l'image sélectionnée
    st.image(image, caption='Logo Marchiche Globale Solution', use_column_width=True)
def creer_dataframe(data_TeamsRH,c1:list,l:list,condition):#name_table
    if len(c1) != len(l):
        return 'verifier c1 et c2'
    else :
        data={}
        length=data_TeamsRH.shape[0]
        for i,j in zip(l,c1) :
            if type(i)==list :
                data[j]=[condition[i[1]][k] for k in data_TeamsRH[i[0]]]
                
            elif i=='':
                data[j]=['' for _ in range(length)]
            elif i in data_TeamsRH.columns:
                data[j]=[k for k in data_TeamsRH[i]]
            else:
                data[j]=[i for _ in range(length)]
        return pd.DataFrame(data)

Code_PO_MA = {    
    'ad dakhla': '73000',
    'ad darwa': '52000',
    'agadir': '80000',
    'aguelmous': '53000',
    'ahfir': '63050',
    'ain el aouda': '11000',
    'ait melloul': '80010',
    'ait ourir': '42050',
    'al aaroui': '91000',
    'al fqih ben çalah': '24000',
    'al hoceïma': '32000',
    'al khmissat': '23350',
    'al attawia': '35000',
    'arfoud': '53000',
    'azemmour': '24000',
    'aziylal': '22000',
    'azrou': '53100',
    'aïn harrouda': '20180',
    'aïn taoujdat': '34000',
    'berrchid': '27150',
    'ben guerir': '43150',
    'beni yakhlef': '26300',
    'berkane': '35000',
    'biougra': '83000',
    'bir jdid': '26100',
    'bou arfa': '21000',
    'boujad': '24350',
    'bouknadel': '16120',
    'bouskoura': '27160',
    'béni mellal': '23000',
    'casablanca': '20000',
    'casa': '20000',
    'chichaoua': '41000',
    'demnat': '45000',
    'el aïoun': '36000',
    'el hajeb': '25000',
    'el jadid': '24000',
    'el kelaa des srarhna': '40000',
    'errachidia': '52000',
    'fnidq': '92000',
    'fès': '30000',
    'guelmim': '81000',
    'guercif': '36000',
    'iheddadene': '60500',
    'imzouren': '93000',
    'inezgane': '80000',
    'jerada': '67250',
    'kenitra': '14000',
    'khemis sahel': '15150',
    'khénifra': '54000',
    'kouribga': '25000',
    'ksar el kebir': '20000',
    'larache': '92000',
    'laayoune': '70000',
    'marrakech': '40000',
    'martil': '93200',
    'mechraa bel ksiri': '28050',
    'mediouna': '26200',
    'mehdya': '28600',
    'meknès': '50000',
    'midalt': '52000',
    'missour': '54000',
    'mohammedia': '20800',
    'moulay abdallah': '54040',
    'moulay bousselham': '93250',
    'mrirt': '54010',
    'my drarga': '45000',
    'mdiq': '93200',
    'nador': '620',
    'oued zem': '59200',
    'ouezzane': '14200',
    'oujda-angad': '60000',
    'oulad barhil': '24200',
    'oulad tayeb': '14240',
    'oulad teïma': '82100',
    'oulad yaïch': '26450',
    'qasbat tadla': '15200',
    'rabat': '10000',
    'safi': '46000',
    'sale': '11000',
    'sefrou': '31000',
    'settat': '26000',
    'sidi bennour': '24250',
    'sidi qacem': '31050',
    'sidi slimane': '24000',
    'sidi smail': '60050',
    'sidi yahia el gharb': '12000',
    'sidi yahya zaer': '11030',
    'skhirate': '12050',
    'souk et tnine jorf el mellah': '26300',
    'tahla': '54000',
    'tameslouht': '40000',
    'tangier': '90000',
    'taourirt': '60300',
    'taza': '35000',
    'temara': '12000',
    'temsia': '30000',
    'tifariti': '70000',
    'tit mellil': '20100',
    'tinghir': '45800',
    'tétouan': '93000',
    'youssoufia': '46300',
    'zagora': '47900',
    'zawyat ech cheïkh': '14210',
    'zaïo': '60600',
    'Zeghanghane': '45000',
    'bejaad':'25060' }


st.subheader('RDD', divider='rainbow')


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
    
    #if i not in ['Date de naissance','Date d\'intégration']:
            
     #       data_TeamsRH[i] = data_TeamsRH[i].astype(str).
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    entr = st.sidebar.radio(
    "Choisissez l'entreprise préférée",
    ["MGS","Sogetrel", "Sofrecom"],#Marchiche Globale Solution
    index=None)
    if entr=='MGS':


        colums__=data_TeamsRH.columns
        st.write(data_TeamsRH.head())
        st.divider()
        if x==True and y==True:
            condition = {
                    'civ':{'monsieur':'$01',
                    'mademoiselle':'$03',
                    'madame':'$02'},
                    'sexe':{
                        'monsieur':'$1',
                        'mademoiselle':'$2',
                        'madame':'$2'
                    },
                    'civMarier':{'madame':'$01',
                    'monsieur':'$02'},

                    'sexeMarier':{
                        'madame':'$1',
                        'monsieur':'$2'
                    },
                    'sf':{
                        'marié':'$02',
                        "mariée":'$02',
                        "marié(e)":'$02',
                        'célibataire':'$01',
                        'divorcée':'$03',
                        'divorcé(e)':'$03',
                        '':''
                    },
                    'CEMPLOI' :{
                    'directeur général': '001',
                    'chef comptable': '002',
                    'coursier': '003',
                    'technical support consultant': '004',
                    'account manager': '005',
                    'hr account manager': '006',
                    'junior technical sales manager': '007',
                    'content moderation supervisor': '008',
                    'senior programe officer': '009',
                    'head of north africa': '010',
                    'area business head': '011',
                    'digital fundraising specialist': '012',
                    'user management advisor': '013',
                    'content management advisor': '014',
                    'family management advisor': '015',
                    'vip user management advisor': '016',
                    'femme de menage': '017',
                    'territory s manager': '018',
                    'rh and payroll specialist': '019',
                    'program coordinator': '020',
                    'comptable': '021',
                    'hr specialist': '022',
                    'event management advisor': '023',
                    'agency management advisor': '024',
                    'l&d specialist africa & m e': '025',
                    'busines manager north africa': '026',
                    'advisor': '027',
                    'vip user management advisor': '028',
                    'regional marketing manager eme': '029',
                    'partnership manager - north af': '030',
                    'directeur zone internationale': '031',
                    'content management advisor': '032',
                    'senior family management adv': '033',
                    'associate project manager': '034',
                    'program specialist learning': '035',
                    'sales engineer': '036',
                    'pubg mena prod manager': '037',
                    'director of communication': '038',
                    'dealer network development': '039',
                    'lead specialist sourcing': '040',
                    'in-country partnership special': '041',
                    'area sales manager maghreb': '042',
                    'content management advisor': '044',
                    'family management advisor': '045',
                    'hr service manager': '047',
                    'consultant sirh': '048',
                    'business development manager': '049',
                    'managing director': '050',
                    'market manager north africa': '051',
                    'senior ams director': '052',
                    'social media manager': '053',
                    'regional sales manager': '054',
                    'senior marketing specialist': '055',
                    'président directeur général': '056',
                    'directeur d’un département': '057',
                    'directeur commercial': '058',
                    'directeur financier': '059',
                    'directeur administratif': '060',
                    'directeur technique': '061',
                    'directeur des ressources humaine': '062',
                    'directeur d’une succursale': '063',
                    'agent commercial': '064',
                    'vrp': '065',
                    'agent itinérant': '066',
                    'président directeur général': '067',
                    'directeur d\'une succursale': '068',
                    'developpeur': '069',
                    'responsable technique': '070',
                    'channel sales manager': '071',
                    'sales leader-sub safrica afric': '072',
                    'client payroll officer': '073',
                    'princing specialist': '074',
                    'web scraper': '075',
                    'senior software engineer': '076',
                    'editor': '077',
                    'senior customer success partne': '078',
                    'backend engineer': '079',
                    'qa test engineer': '080',
                    'engineering manager': '081',
                    'claim analyst': '082',
                    'it system administrator': '083',
                    'senior customer success partner': '085',
                    'export manager mena': '086',
                    'directeur administratif et fin': '087',
                    'gestionnaire de paie': '088',
                    'credit controller': '090',
                    'consultant': '091',
                    'territory sales executive': '092',
                    'système engineering leader': '093',
                    'client project leader': '094',
                    'senior field marketing manager': '095',
                    'sales manager': '096',
                    'demand generation': '097',
                    'prodact value promoter': '098',
                    'directeur exécutif': '100',
                    'ingénieur avant-vente sirh': '101',
                    'directeur integration des solu': '102',
                    'sales director': '103'
                },
                    'CATEGSP':{
                    'directeur': '$cad',
                    'cadre': '$cad',
                    'agent de maitrise': '$agm',
                    'employé': '$emp',
                    'agent de maitrise': '$agm',
                    'apprenti employé': '$app',
                    'ouvrier': '$ouv',
                    'stagiaire': '$sta',
                    'stagiaire non rémunéré': '$stanr',
                    '':''}
                }
            def nettoyer_texte(chaine):
                return re.sub(r'\s+', ' ', chaine)

            def nettoyer_espace(chaine):
                return chaine.strip()

            def acsent(chaine):
                return unidecode(chaine)
            def LOWER(chaine):
                return chaine.lower()

            data_TeamsRH['Emploi occupé'] = data_TeamsRH['Emploi occupé'].apply(lambda x: acsent(x))
            # Appliquer la fonction à la colonne 'Texte' du DataFrame
            data_TeamsRH['Emploi occupé'] = data_TeamsRH['Emploi occupé'].apply(lambda x: nettoyer_espace(x))
            # Appliquer la fonction à la colonne 'Texte' du DataFrame
            data_TeamsRH['Emploi occupé'] = data_TeamsRH['Emploi occupé'].apply(lambda x: nettoyer_texte(x))

            
            data_TeamsRH['Emploi occupé'] = data_TeamsRH['Emploi occupé'].apply(lambda x: LOWER(x))

            d=dict()
            for ind,i in enumerate (data_TeamsRH['Emploi occupé']):
                d[ind]=i.split(" ")
            l=list()
            x=condition['CEMPLOI']
            
            for i in x.keys():
                l.append(i.split(' '))

            F=dict()
            for ind,k in zip(d.keys(),d.values()):
                m=[]
                for i in l: 
                    if len(k)==len(i) :
                        m.append(i)
                F[ind]=m
            final={}
            for ind,(i,j) in enumerate(zip(d.values(),F.values())):
                list_score=[]
                for k in range(len(j)):
                    similarity_ratio=0
                    for p in range(len(i)):
                        similarity_ratio += fuzz.ratio(i[p],j[k][p])
                    list_score.append(similarity_ratio)
                d_val=' '.join(i)

                F_val=' '.join(j[list_score.index(max(list_score))])
                final[d_val]=F_val

            g=dict()
            for k,v in zip(final.keys(),final.values()):
                g[v]=k
            data_TeamsRH['Emploi occupé']=data_TeamsRH['Emploi occupé'].map(final)

            l={'Matricule RH ': 'int',
            'Prenom': 'str',
            'CIN': 'str',
            'Date de naissance': 'date',
            'Nom': 'str',
            'Salairee de base MAD': 'float',
            'Statut ': 'CATEGSP',
            'Fonction ': 'CEMPLOI',
            "Date d'intégration": 'date'}
            m=[0,0,0,1,1,1,2,2,2] 

            #f=['int','str','date','float','CATEGSP','CEMPLOI']
            
            col1, col2, col3 = st.columns(3)
            columns_={}
            index_=[0,3,8,6,2,19,17,16,11]
            
            for ind,(j,z,i) in enumerate(zip(l.keys(),m,index_)):   
                
                if z==0:
                    with col1:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")

                elif z==1:
                    with col2:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")
                else:
                    with col3:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")
            with col3:
                        columns_['Adresse postale']=st.selectbox('Adresse postale',
                            list(colums__),
                            index=9,
                            placeholder="Sélectionnez une valeur...",key=f"{9}")
            with col1:
                        columns_['NB d\'enfants à charge']=st.selectbox('NB d\'enfants à charge',
                            list(colums__),
                            index=5,
                            placeholder="Sélectionnez une valeur...",key=f"{10}")
            st.divider()
                        
            c1, c2, c3 = st.columns(3)
            with c1:
                MSOC=st.text_input('S1CONTRAT >> MSOC', '')
            with c2:
                META=st.text_input('S2ETA >> META', '')
                path=st.text_input('inserer name file','')
            with c3:
                MCLI=st.text_input('S2CATEG >> MCLI', '')
            
       
            
            st.divider()
            renamed_columns=dict()
            for v,k in zip(columns_.keys(),columns_.values()):
                renamed_columns[k]=v
                
            data_TeamsRH.rename(columns=renamed_columns, inplace = True)
           
            

            #st.write(data_TeamsRH)
            for i in data_TeamsRH.select_dtypes(exclude=['int', 'float']).columns:
                data_TeamsRH[i] = data_TeamsRH[i].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
            
            data_TeamsRH = data_TeamsRH.dropna(subset=data_TeamsRH.columns, how='all')
            data_TeamsRH["Date de naissance"] = data_TeamsRH["Date de naissance"].replace(" ", pd.NaT)

            # Convertissez la colonne "Date de naissance" en format de date spécifique
            format_date = "%d/%m/%Y"
            data_TeamsRH["Date de naissance"] = pd.to_datetime(data_TeamsRH["Date de naissance"],
                                                                format=format_date, errors='coerce')
            data_TeamsRH["Date d'intégration"] = pd.to_datetime(data_TeamsRH["Date d'intégration"],format=format_date, errors='coerce')
        ######## st.write(data_TeamsRH,data_TeamsRH.dtypes)
            

            #data=pd.read_excel('./Base salarié_15.02.2024__.xlsx',sheet_name='BDD COLLAB')
            data_TeamsRH['Salairee de base MAD']=data_TeamsRH['Salairee de base MAD'].fillna(0)
            
            data_TeamsRH['Date de naissance'] = pd.to_datetime(data_TeamsRH['Date de naissance'], format='%d/%m/%Y')

            data_TeamsRH['Date d\'intégration'] = pd.to_datetime(data_TeamsRH['Date d\'intégration'])
            data_TeamsRH['Date d\'intégration'] = data_TeamsRH['Date d\'intégration'].dt.strftime('%d/%m/%Y')
            data_TeamsRH['Date de naissance'] = data_TeamsRH['Date de naissance'].dt.strftime('%d/%m/%Y')

            
            #Formatez la colonne 'DateNaissance' pour ne conserver que la date (jour, mois, année)
            #st.write(data_TeamsRH)
            data=data_TeamsRH.fillna('')

            data["ADRVILLE"] = [str(i).split('-')[-1].replace(' ', '') if i != '' else '' for i in data["Complément d'adresse"] ]
            data["ADRCOMP"] = [str(i).split('-')[-2] if len(str(i).split('-'))>1  else '' for i in data["Complément d'adresse"] ]
       
            data["ADRCPOS"] = [Code_PO_MA[i] if i != '' else '' for i in data["ADRVILLE"]]
            #data["Complément d'adresse"] = data["Adresse"]
            #data.rename({'Adresse':'Complément d\'adresse'})
            
        
    elif entr == 'Sogetrel':
        condition = {
            'civ':{'monsieur':'$01',
            'mademoiselle':'$03',
            'madame':'$02'},
            'sexe':{
                'monsieur':'$1',
                'mademoiselle':'$2',
                'madame':'$2'
            },
            'civMarier':{'madame':'$01',
            'monsieur':'$02'},

            'sexeMarier':{
                'madame':'$1',
                'monsieur':'$2'
            },
            'sf':{
                'marié':'$02',
                "mariée":'$02',
                'célibataire':'$01',
                'divorcée':'$03',
                '':''
            },
            'CEMPLOI' :{
            'directrice de sites': '01',
            'responsable qualité et formation': '02',
            'responsable operation': '03',
            'formateur': '04',
            'responsable technique': '05',
            'responsable equipe': '06',
            'chargé de recrutement': '07',
            'office manager': '08',
            'responsable admin et gestion': '09',
            'chargé (e) de conduite d\'activité': '10',
            'technicien it': '11',
            'responsable ressources humaines': '12',
            '':''},
            'CATEGSP':{
            'directeur': '$cad',
            'cadre': '$cad',
            'agent de maitrise': '$agm',
            'employé': '$emp',
            'agent de maitrise': '$agm',
            'apprenti employé': '$app',
            'ouvrier': '$ouv',
            'stagiaire': '$sta',
            'stagiaire non rémunéré': '$stanr',
            '':''}
        }
        colums__=data_TeamsRH.columns
        st.write(data_TeamsRH.head())
        st.divider()
        if x==True and y==True:

            l={'Matricule RH ': 'int',
            'Prenom': 'str',
            'CIN': 'str',
            'Date de naissance': 'date',
            'Nom': 'str',
            'Salairee de base MAD': 'float',
            'Statut ': 'CATEGSP',
            'Fonction ': 'CEMPLOI',
            "Date d'intégration": 'date'}
            m=[0,0,0,1,1,1,2,2,2] 

            #f=['int','str','date','float','CATEGSP','CEMPLOI']
            
            col1, col2, col3 = st.columns(3)
            columns_={}
            index_=[0,2,5,6,1,15,9,8,7]
            
            for ind,(j,z,i) in enumerate(zip(l.keys(),m,index_)):   
                
                if z==0:
                    with col1:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")

                elif z==1:
                    with col2:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")
                else:
                    with col3:
                        columns_[j]=st.selectbox(j,
                            list(colums__),
                            index=i,
                            placeholder="Sélectionnez une valeur...",key=f"{ind}")
            with col2:
                        columns_['Adresse postale']=st.selectbox('Adresse postale',
                            list(colums__),
                            index=12,
                            placeholder="Sélectionnez une valeur...",key=f"{9}")
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1:
                MSOC=st.text_input('S1CONTRAT >> MSOC', '')
            with c2:
                META=st.text_input('S2ETA >> META', '')
                path=st.text_input('inserer name file','')
            with c3:
                MCLI=st.text_input('S2CATEG >> MCLI', '')
            

                
            
            st.divider()
            
            data_TeamsRH.rename(columns=columns_, inplace = True)
            #st.write(data_TeamsRH)
            for i in data_TeamsRH.select_dtypes(exclude=['int', 'float']).columns:
                data_TeamsRH[i] = data_TeamsRH[i].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
            
            data_TeamsRH = data_TeamsRH.dropna(subset=data_TeamsRH.columns, how='all')
            data_TeamsRH["Date de naissance"] = data_TeamsRH["Date de naissance"].replace(" ", pd.NaT)

            # Convertissez la colonne "Date de naissance" en format de date spécifique
            format_date = "%d/%m/%Y"
            data_TeamsRH["Date de naissance"] = pd.to_datetime(data_TeamsRH["Date de naissance"],
                                                                format=format_date, errors='coerce')
            data_TeamsRH["Date d'intégration"] = pd.to_datetime(data_TeamsRH["Date d'intégration"],
                                                                format=format_date, errors='coerce')
        ######## st.write(data_TeamsRH,data_TeamsRH.dtypes)
            

            #data=pd.read_excel('./Base salarié_15.02.2024__.xlsx',sheet_name='BDD COLLAB')
            data_TeamsRH['Salairee de base MAD']=data_TeamsRH['Salairee de base MAD'].fillna(0)
            
            data_TeamsRH['Date de naissance'] = pd.to_datetime(data_TeamsRH['Date de naissance'], format='%d/%m/%Y')

            data_TeamsRH['Date d\'intégration'] = pd.to_datetime(data_TeamsRH['Date d\'intégration'])
            data_TeamsRH['Date d\'intégration'] = data_TeamsRH['Date d\'intégration'].dt.strftime('%d/%m/%Y')
            data_TeamsRH['Date de naissance'] = data_TeamsRH['Date de naissance'].dt.strftime('%d/%m/%Y')

            
            #Formatez la colonne 'DateNaissance' pour ne conserver que la date (jour, mois, année)
            #st.write(data_TeamsRH)
            data=data_TeamsRH.fillna('')

            data["ADRCOMP"] = [str(i).split(' ')[-2].replace(" ",'') if i != '' else '' for i in data["Adresse postale"] ]
            data["ADRVILLE"] = [str(i).split(' ')[-1] if i != '' else '' for i in data["Adresse postale"] ]
            
            data["ADRCPOS"] = [Code_PO_MA[i] if i != '' else '' for i in data["ADRVILLE"]]
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        #st.write(data)


    #data=data.iloc[:-5]
    data['Matricule RH ']=data['Matricule RH '].astype(int)
    data['Fonction '] = data['Fonction '].str.strip()
    data['Fonction '] = data['Fonction '].str.lower()
    data['Statut '] = data['Statut '].str.strip()
    data['Statut '] = data['Statut '].str.lower()

    ################
    sexe =st.toggle('if columns <<Civilité>> exist select checkbox')
    data=data.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    if  sexe :
        
        s=[]
        for i,j in  zip(data['Sexe'],data['Situation familiale']) :
            if i=='femme':
                if j=='Célibataire':
                    s.append('mademoiselle')
                else:
                    s.append('madame')
            else :
                s.append('monsieur')
        data['Civilité']=s
        
        st.success('success adding the column << Civilité >>')
    data.Nom=data.Nom.str.capitalize()
    data.Prenom=data.Prenom.str.capitalize()
    st.write(data) 

    st.divider()
    BBB=st.button("Resulta >>", type="primary")

    data=data.fillna('')
    



    if BBB:
        tttt=  [        'S1IDE',
            'S1ADR',
            'S1CONJOINT',
            'S1ENFPC',
            'S1CONTRAT',
            'S2TYPECONTR',
            'S2ETA',
            'S2EMPLOI',
            'S2CATEG',
            'S2HORCONTR',
            'S2REMUNER',
            'S2ANALYT']
        t1, t2,t3, t4,t5, t6,t7, t8,t9, t10,t11, t12= st.tabs(tttt)
        with t1:
        #xsS1IDE t1
            C=['MMAT','MRGL',	'MITEM' ,'MVERSION','CIVILITE',	'NOM1',	'PRENOM1','NOMJF','SEXE',
                        'DNAISS','LNNOMCOM','NUMNAT','NUMCNSS',	'SITFAM',	'LNPAYS_MND','LOCALIDNUMBER','ANCMAT']
            L=['Matricule RH ','r1',0,0,['Civilité','civ'],'Nom','Prenom','',['Civilité','sexe'],
                        'Date de naissance','','CIN','',['Situation familiale','sf'],'$MA','','']
            S1IDE=creer_dataframe(data, C,L,condition)
            #{}
            st.write(S1IDE.head(3))
        
        ######

        with t4:
            
            #S1ENFPC t4
            def S1ENFPC_dataframe(data,C,L):
                ind_al= 0
                l=[]
                for mat_ind ,mat in enumerate(list(data['Matricule RH '])):
                    #st.write(data[data['Matricule RH ']==mat]['Situation familiale'])
                    if data.loc[data['Matricule RH '] == mat, 'NB d\'enfants à charge'].iloc[0] != 0:
                        
                        for _ in range(int(data['NB d\'enfants à charge'][mat_ind])):
                            IJ={}

                            L[6]=f'Nom{ind_al}'
                            for i,j in zip(L,C):
                                
                                if type(i)==list :
                                    #  st.write(data[i[0]][mat_ind])
                                    IJ[j]=condition[i[1]][data[i[0]][mat_ind]] 
                                elif i  in data.columns:
                                    IJ[j]=data[i][mat_ind]
                                else:
                                    IJ[j]=i
                            
                                #st.write(IJ) [data['Matricule RH ']==mat]
                            l.append(IJ) 
                            ind_al+=1 
                            
                    if data.loc[data['Matricule RH '] == mat, 'NB d\'enfants à charge'].iloc[0] != 0 and data['Situation familiale'][mat_ind] in ['marié' ,'mariée'] and data['Sexe'][mat_ind]=='homme':
                        IJ={}
                        LL=L
                        #LL[3]=data['Date de naissance'][mat_ind]
                        LL[5]='$01'
                        LL[10]='$1'
                        st.write(ind_al)
                        LL[6]=f'Nom{ind_al}'
                        for ii in LL:
                            if type(ii)==list :
                                IJ[j]=condition[ii[1]][data[ii[0]][mat_ind]]
                            elif ii in data.columns:
                                IJ[j]=data[ii][mat_ind]
                            else:   
                                IJ[j]=ii
                        
                        l.append(IJ)
                        ind_al+=1
                
                    else  : #[data['Matricule RH ']==mat]Sexe
                        if data['Situation familiale'][mat_ind] in ['marié' ,'mariée'] and data['Sexe'][mat_ind]=='homme':
                            LL = L
                            
                            LL[6]=f'Nom{ind_al}'
                            LL[5]='$01'
                            LL[10]='$1'
                            #LL[3]=data['Date de naissance'][mat_ind]
                            IJ1={}
                            for inex,m in enumerate (LL):
                                
                                if type(m)==list :
                                    g=data[m[0]][mat_ind]
                                    #st.write('m',m,data[m[0]][data['Matricule RH ']==mat][mat_ind])
                                    IJ1[C[inex]]=condition[m[1]][g]
                                elif m in data.columns:
                                    #o=[data['Matricule RH ']==mat]
                                    IJ1[C[inex]]=data[m][mat_ind]
                                else:   
                                    IJ1[C[inex]]=m
                            ind_al+=1
                                
                            l.append(IJ1)

                ind=0
                df = pd.DataFrame(columns=C)
                for i in l:
                    df.loc[ind]=i
                    ind+=1
                df['MMAT']=df['MMAT'].astype(int)  
                return df
            
            C=['MMAT','MITEM' ,'MVERSION',	'NOM1',	'NOM2',	'PRENOM1',	'TITRE',	'SEXE',	'DNAISS',	'TYPEPC1',	'TYPEPC2' ]
            L=['Matricule RH ',0,0,'Nom enf','','prenom2','','$1','01/01/2020','','$fisc']
            S1ENFPC=S1ENFPC_dataframe(data, C,L)
            st.write(S1ENFPC)
        ######
        #S1CONJOINT t3
        with t3:
            def S1CONJOINT_dataframe(data,C,L):
                ind_al= 0
                l=[]
                for mat_ind ,mat in enumerate(list(data['Matricule RH '])):
                    
                    if data.loc[data['Matricule RH '] == mat, 'Situation familiale'].iloc[0] in ['marié',"mariée",'marié(e)']:
                    

                        IJ={}
                        L[6]=f'Nom{ind_al}'
                        for i,j in zip(L,C):
                            
                            if type(i)==list :
                                #  st.write(data[i[0]][mat_ind])
                 
                                IJ[j]=condition[i[1]][data[i[0]][mat_ind]] 
                            elif i  in data.columns:
                                IJ[j]=data[i][mat_ind]
                            else:
                                IJ[j]=i
                        l.append(IJ) 
                        ind_al+=1
                ind=0
                df = pd.DataFrame(columns=C)
                for i in l:
                    df.loc[ind]=i
                    ind+=1
                df['MMAT']=df['MMAT'].astype(int)  
                return df
                            
                  
            #S1CONJOINT t3
            C=['MMAT','MITEM' ,'MVERSION','DDEB','DFIN','CIVILITE','NOM1','NOM2','PRENOM1','TITRE','SEXE','DNAISS' ]
            L=['Matricule RH ',0,0,'01/01/2000','',['Civilité','civMarier'],'Nom','','Prenom ','',['Civilité','sexeMarier'],'']
            #D=data[data['Situation familiale'].isin(['marié' ,'mariée'])]
            S1CONJOINT=S1CONJOINT_dataframe(data,C,L)#creer_dataframe(D, C,L) 
            st.write(S1CONJOINT.head())
        ######
        with t5:

            #S1CONTRAT t5
            C=['MMAT','MITEM' ,'MVERSION','DDEB','DFIN','MRGL','MSOC','CPERIOD','MOTIFENTREE','DSORTIE','DSOLDE',
                'MOTIFSORTIE','DANC1','DANC2','DANC3','DDEM','MOTCHG','DUE_CODESAL','DUE_CODEAR']

            L=['Matricule RH ',1,0,'Date d\'intégration','','r1',MSOC,'','$02',
            '','','','Date d\'intégration','Date d\'intégration','Date d\'intégration','','$empty','$empty','$empty']
            S1CONTRAT=creer_dataframe(data, C,L,condition)
            st.write(S1CONTRAT.head(5))
        ########
        with t6:

            #S2TYPECONTR t6
            C=['MMAT','MITEM' ,'MVERSION',	'DDEB',	'DFIN',	'TYPCONTRAT',	'MCONTRAT',	'DADSUCODEDROIT']

            L=['Matricule RH ',0,0,'Date d\'intégration','','$cdi',1,'']
            S2TYPECONTR=creer_dataframe(data, C,L,condition)
            st.write(S2TYPECONTR.head(5))
        ########
        with t7:

            #S2ETA t7
            C= ['MMAT','MITEM' ,'MVERSION', 'MCONTRAT', 'DDEB', 'DFIN', 'META', 'CODETRAVFE', 'SERVICE']
            L=['Matricule RH ',0,0,1,'Date d\'intégration','',META,'$empty','$empty']
            S2ETA=creer_dataframe(data, C,L,condition)
            st.write(S2ETA.head(5))    
        #########
        with t8:

            #S2EMPLOI t8
            C = ['MMAT','MITEM' ,'MVERSION', 'MCONTRAT', 'DDEB', 'DFIN', 'CEMPLOI']
            L=['Matricule RH ',0,0,1,'Date d\'intégration','',['Fonction ','CEMPLOI']]########
            S2EMPLOI=creer_dataframe(data, C,L,condition)
            st.write(S2EMPLOI.head(5) )  
        ##########
        with t9:

            #S2CATEG t9
            C= ['MCLI', 'MMAT', 'MCONTRAT', 'MITEM' ,'MVERSION', 'MVERSION', 'DDEB',
                    'DFIN', 'MOTCHG', 'CATEGSP', 'PRUDHOM_COLLEGE']

            L=[MCLI,'Matricule RH ',1,0,0,0,'Date d\'intégration','','$empty',['Statut ','CATEGSP'],'']
            S2CATEG=creer_dataframe(data, C,L,condition)
            st.write(S2CATEG.head(5))
        ###########
        with t10:

        #S2HORCONTR t10
            C=  ['MMAT', 'DDEB', 'DFIN', 'HORAIREAN', 'HORAIREMENS', 'HORAIREHEBDO', 'HORAIREJOUR',
                'CODETYPHOR', 'CODETPSTRAV', 'POURTPSTRAV', 'NBJOURAN', 'MODECAL', 'ACTDEFAUT', 
                'ACTMODE', 'PLANNING','MITEM' ,'MVERSION','MCONTRAT']

            L=['Matricule RH ','Date d\'intégration','',2288,191,44,8,'$me','','','','','','','$tcs',0,0,1]
            S2HORCONTR=creer_dataframe(data, C,L,condition)
            st.write(S2HORCONTR.head(5) )    
        #############
        with t11:

        #S2REMUNER t11
            C = ['MMAT', 'DDEB', 'DFIN', 'CREMUNER', 'MONTREMU', 'CDEVISE','MITEM' ,'MVERSION','MCONTRAT']
            L = ['Matricule RH ','Date d\'intégration','','$sbj','Salairee de base MAD','$mad',0,0,1]########
            S2REMUNER=creer_dataframe(data, C,L,condition)
            S2REMUNER.MONTREMU=S2REMUNER.MONTREMU.astype(str)
            S2REMUNER['MONTREMU'] = S2REMUNER['MONTREMU'].str.replace(' ', '').str.replace(',', '.').astype(float)

            st.write(S2REMUNER.head(5))##### MONTREMU
        ##########
        with t12:

            #S2ANALYT t12
            C = ['MMAT', 'DDEB', 'DFIN','MITEM' ,'MVERSION','MCONTRAT']
            L = ['Matricule RH ','Date d\'intégration','',0,0,1]
            S2ANALYT=creer_dataframe(data, C,L,condition)
            st.write(S2ANALYT.head())
        ###########
        with t2:

            #S1ADR t2
            C  = [
                        'MMAT',
                        'DDEB',
                        'DFIN',
                        'ADRNUM',
                        'ADRBIS',
                        'ADRRUE',
                        'ADRCOMP',
                        'ADRVILLE',
                        'ADRCPOS',
                        'ADRTEL1',
                        'ADRTEL2',
                        'ADRMOB',
                        'ADRMAIL',
                        'ADRPAYS',
                        ]
            L = ['Matricule RH ','Date d\'intégration' ,'' ,'' , '','Adresse postale', 'ADRCOMP','ADRVILLE','ADRCPOS', '', '', '','' , '$MA']
            S1ADR=creer_dataframe(data, C,L,condition)
            st.write(S1ADR)

        
        #cc=st.button("Dowload result >>", type="primary")
        if path != '':
            import os  # For directory checking

            # Check if the 'resultat' directory exists, if not, create it
            directory = 'resultat'
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Define the file path
            p = f'{directory}/{path}.xlsx'
            #if st.button("Dowload result >>", type="primary"):
                #if t != '':
           
        
            with pd.ExcelWriter(p) as writer:
                # Write each DataFrame to a separate sheet
                S1IDE.to_excel(writer, sheet_name='S1IDE', index=False)
                S1ADR.to_excel(writer, sheet_name='S1ADR', index=False)
                S1CONJOINT.to_excel(writer, sheet_name='S1CONJOINT', index=False)
                S1ENFPC.to_excel(writer, sheet_name='S1ENFPC', index=False)
                S1CONTRAT.to_excel(writer, sheet_name='S1CONTRAT', index=False)
                S2TYPECONTR.to_excel(writer, sheet_name='S2TYPECONTR', index=False)
                S2ETA.to_excel(writer, sheet_name='S2ETA', index=False)
                S2EMPLOI.to_excel(writer, sheet_name='S2EMPLOI', index=False)
                S2CATEG.to_excel(writer, sheet_name='S2CATEG', index=False)
                S2HORCONTR.to_excel(writer, sheet_name='S2HORCONTR', index=False)
                S2REMUNER.to_excel(writer, sheet_name='S2REMUNER', index=False)
                S2ANALYT.to_excel(writer, sheet_name='S2ANALYT', index=False)
                
from pathlib import Path
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "main.css"
with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)



current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "main.css"
with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)          
# Charger une image (remplacez "chemin_vers_votre_image.jpg" par le chemin de votre image)


            
