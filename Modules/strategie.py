import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime, date
from Modules.comparaison_fun import comparaisonToday, comparaisonPeriode


#strategie definition
def strategie(lll,name, db, date_achat, param, listeprixbas, listedatebas, achatoupas, venteoupas, listeprixvente,listedatevente):
    df = pd.read_sql_query(f"select Dernier,Date from Action where date<='{date_achat}'  order by date desc", db)
    query = f"select NoteFinale , Date  from Consensus where Date='{date_achat}'"
    df_con = pd.read_sql_query(query, db)
    if (df_con.empty):
        indiceConsenus = None
    else:
        indiceConsenus = df_con["NoteFinale"].iat[0]
        indiceConsenus = float(indiceConsenus)
    date_str = df["Date"].iat[0]
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    prix = df["Dernier"].iat[0]
    achat = 0
    indiceAction = comparaisonToday(name, param['periode_analyse_cours_action'], date_str)

    if (indiceAction <= param['centile_max_action']):
        namesIndice="CAC40"
        if (name=="Airbnb") :
            namesIndice="Dow_Jones"
        indiceCAC = comparaisonPeriode(namesIndice, param['type_moyenne_glissante_cac'], date_str)
        #print("Cac",indiceCAC)
        if (indiceCAC <= param['centile_max_cac']  ): #or indiceCAC >= param['centile_min_cac']
            if (indiceConsenus) != None:
                if (indiceConsenus < 0.5):
                    return (" Consensus = ne pas acheter en ce moment ")
            achatoupas.append(1)
            achat = 1
            prix_achat = float(prix)
            listeprixbas.append(float(prix))
            listedatebas.append(date_str)
        else:
            lll.append(0)
            achatoupas.append(0)
            venteoupas.append(0)
            return (0,f"Le prix pourrait etre du a un maivais resultat de l'entrepise ,centile CAC40 est {indiceCAC}")
    else:
        lll.append(1)
        return (1,f"Pas le bon moment pour acheter , centile action est {indiceAction}")

    vente = 0
    if (achat == 1):
        df = pd.read_sql_query(f"select Dernier,Date from Action where date>='{date_achat}'  order by date desc", db)
        query = f"select Dernier,Date from Action where Date>'{date_achat}' and (julianday(Date)-julianday( '{date_achat}' )) <={param['periode_attente_vente']} order by date asc"
        df = pd.read_sql_query(query, db)
        for i in range(len(df)):
            date_str = df["Date"].iat[i]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            prix = float(df["Dernier"].iat[i])
            if ((prix - prix_achat) / prix_achat) > param['taux_gain']:
                vente = 1
                venteoupas.append(1)
                listedatevente.append(date_str)
                listeprixvente.append(prix)
                return ("Strategie fonctionne")
        if (vente == 0):
            venteoupas.append(0)
            date_str = df["Date"].iat[-1]
            prix = float(df["Dernier"].iat[-1])
            listedatevente.append(date_str)
            listeprixvente.append(prix)
            return (f"On a vendu apres {param['periode_attente_vente']} jours ")


#mesure de la pertinence de la strategie
def teststrategie(name, param):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(f"select Date from Action where date  order by date desc", db)
    dates = list(df['Date'])

    location1 = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActionsCAC40.sqlite'
    if (name=="Airbnb") :
        location1 = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActionsDow_Jones.sqlite'

    db1 = sqlite3.connect(location1)
    df1 = pd.read_sql_query(f"select Date from Action where date  order by date desc", db1)
    dates1 = list(df1['Date'])

    listedate = []
    for d in dates:
        if d in dates1:
            listedate.append(d)
    listedate=listedate[param['periode_attente_vente']:]


    listeprixbas = []
    listedatebas = []
    achatoupas = []
    venteoupas = []
    listeprixvente = []
    listedatevente = []
    actionoucac=[]
    lll=[]


    for date in listedate:
        #print(date)
        res=(strategie(lll,name, db, date, param, listeprixbas, listedatebas, achatoupas, venteoupas, listeprixvente,listedatevente))

    nb_strategie_fonctionne=0
    nb_strategie_fonctionne_pas=0
    ratio_strategie_fonctionn=[]

    for i in range(len(achatoupas)) :
        if (achatoupas[i]==1 ):
            if (venteoupas[i]==1 ):
                nb_strategie_fonctionne+=1
            else :
                nb_strategie_fonctionne_pas+=1
    #print(nb_strategie_fonctionne,nb_strategie_fonctionne_pas)
    ratio=[(listeprixvente[i]-listeprixbas[i])/listeprixbas[i] for i in range(len(listeprixbas)) ]
    #print(ratio)
    if (nb_strategie_fonctionne+nb_strategie_fonctionne_pas==0) :
        precision=0
    else:
        precision = nb_strategie_fonctionne / (nb_strategie_fonctionne + nb_strategie_fonctionne_pas)

    if precision!=0 :
        return {'Ratio Moyen du gain ':np.mean(ratio),'Precision': precision ,"nb_strategie_excute":nb_strategie_fonctionne + nb_strategie_fonctionne_pas }




