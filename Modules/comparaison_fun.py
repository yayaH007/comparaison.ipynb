

import altair as alt
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import site
import sys


#compare todays values to older values
def comparaisonToday (name, periode,date_saisi) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)

    df = pd.read_sql_query(f"select Dernier,Date from Action where date<='{date_saisi}'  order by date desc", db)

    if periode == "Month":
        df = df.iloc[0:23].copy()
    elif periode == "Year":
        df = df.iloc[0: 254].copy()
    elif periode == "Trimester":
        df= df.iloc[0:65].copy()
    elif periode == "2weeks":
        df = df.iloc[0:10].copy()
    elif periode == "3years":
        df=df
    else:
        print("syntax problem:" ,periode)
        return 0

    dff=df.query('Date==@date_saisi')

    if (len(dff)==0) :
        print("La date saisi: "+date_saisi+ " n'existe pas dans la bdd")
        quit()
    else :
        valeur_today=dff['Date'].iat[0]
        df["Rank"] = df["Dernier"].rank()

        rank=df.Rank.iat[0]
        n=len(df)
        q=((rank/n)).round(3)

        #print( "Date: " ,date_saisi ,":  The value of ",name ,"stocks:",valeur_today.round(3) ," is the  ",q,"% pourcentile of "+periode+" values")
        return (q)

#compare this trimeter/month's mean value to older values

def comparaisonPeriode(name,periode,date_saisi):
    if periode!= "Trimester" and periode!= "Month" and periode!="Week" :
        print("probleme syntaxe")
        quit()
    table_name = 'meanPrice' +'per'+periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(f"select prix_moyen from {table_name} where date_deb<='{date_saisi}'  order by date_deb desc", db)
    df["Rank"] = df["prix_moyen"].rank()
    valeur_now=df["prix_moyen"].iat[0]
    rank = df.Rank.iat[0]
    n = len(df)
    q = ((rank / n) ).round(3)

    #print("Date: " ,date_saisi , " : This "+periode+" mean value of ",name," stocks:", valeur_now.round(3)," is the ",q, "% pourcentile of all "+periode+"s mean values")
    return (q)





def calcule_indice(name,periode,date_saisi) :

    if (comparaisonToday(name,periode,date_saisi)==0) :
        quit()

    k_today=1-comparaisonToday(name,periode,date_saisi)/100
    k_cac = comparaisonPeriode("CAC40", "Month", date_saisi) / 100    #le mois !!!!!!!!!!!!!!!!

    if (name=="Airbnb") :
        k_cac = comparaisonPeriode("Dow_Jones", "Month", date_saisi) / 100


    print(k_today)
    """k_periode=1-comparaisonPeriode(name,periode)"""

    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    query=f"select NoteFinale , Date  from Consensus where Date='{date_saisi}'"
    df = pd.read_sql_query(query, db)


    if (df.empty):
        print("consensus indisponible")
        print("k_cac=", k_cac, "k_action", k_today)
        k =  k_today * k_cac
    else :
        k_consensus=df["NoteFinale"].iat[0]
        k = k_today * k_cac*k_consensus
        print("k_consensus=", k_consensus, "  k_cac=", k_cac, "k_action", k_today)

    return(k)





