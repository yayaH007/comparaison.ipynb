import pandas as pd
import requests
import sqlite3
from datetime import datetime


#extraction des données du cours du site Boursorama
def premierParcours(url1, url2):
    i = 1
    url = url1 + str(i) + url2
    html = requests.get(url).content
    df = pd.read_html(html)[0]
    last_date = df.iat[0, 0]
    b = True
    while (b):
        i = i + 1
        url = url1 + str(i) + url2
        html = requests.get(url).content
        df1 = pd.read_html(html)[0]
        first_date = df1.iat[0, 0]
        b = (first_date != last_date)
        if (b == True):
            df = pd.concat([df, df1], ignore_index=True)
    df.Date = pd.to_datetime(df.Date, format='%d/%m/%Y').dt.date
    prix_exmpl = df.loc[0, 'Dernier']
    if (type(prix_exmpl) == str):
        df['Dernier'] = df['Dernier'].str.replace(' ', '')
    df['Dernier'] = df['Dernier'].astype(float)
    df = df.sort_values(by='Date', ignore_index=True)
    df['Var. %'] = df['Var. %'].str.split('%', expand=True)[0].astype(float)
    df=df.rename(columns={'Var. %':'Var'})
    liste = []
    for val in df['Var']:
        if (float(val) >= 0):
            liste.append(1)
        else:
            liste.append(0)
    df['Variation'] = liste
    return (df.convert_dtypes())

def create_db(url1, url2,name):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions'+name+'.sqlite'
    df = premierParcours(url1, url2)
    db = sqlite3.connect(location)
    df.to_sql('Action', db, if_exists='replace')
    print('data base created')
    db.close()

def db_complete(url1, url2,name):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    query="select max(Date) from Action"
    date_max=pd.read_sql_query(query,db).iat[0, 0]
    date_max= datetime.strptime(date_max, "%Y-%m-%d").date()
    i = 1
    url = url1 + str(i) + url2
    html = requests.get(url).content
    df = pd.read_html(html)[0]
    df.Date = pd.to_datetime(df.Date, format='%d/%m/%Y').dt.date

    prix_exmpl=df.loc[0, 'Dernier']
    if ( type(prix_exmpl)==str) :
        df['Dernier'] = df['Dernier'].str.replace(' ', '')
    df['Dernier'] = df['Dernier'].astype(float)
    b=True
    m=len(df)
    n=len(df)
    while (b) :
        df=df.query("Date>@date_max").copy()
        m = len(df)
        b=not(df.empty)
        if (b):
            df['Var. %'] = df['Var. %'].str.split('%', expand=True)[0].astype(float)
            df=df.rename(columns={'Var. %':'Var'})
            liste = []
            for val in df['Var']:
                if (float(val) >= 0):
                    liste.append(1)
                else:
                    liste.append(0)
            df['Variation'] = liste
            df.to_sql('Action',db, if_exists='append')
            print("data base needs to be completed")
            if (n==m):
                i=i+1
                url = url1 + str(i) + url2
                html = requests.get(url).content
                df = pd.read_html(html)[0]
                df.Date = pd.to_datetime(df.Date, format='%d/%m/%Y').dt.date
                n=len(df)
            else:
                 b=False
        else:
            print('No new data to add to database')
    db.close()




