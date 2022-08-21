import pandas as pd
import sqlite3
import numpy as np

#calcule des myenne glissante des cours et stockage dans la bdd
def PriceMean(name,periode) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    if (periode=="Week"):
        p=5
    if (periode=="Month"):
        p=23
    if ((periode=="Trimester")):
        p=65
    db = sqlite3.connect(location)
    query="select Date  , Dernier  from Action"
    df=pd.read_sql_query(query,db)

    liste=[]
    dfgliss= pd.DataFrame(columns=['date_deb', 'date_fin', 'prix_moyen'])
    j = 0
    for i in range (len(df)) :
        price=df.loc[i,"Dernier"]
        liste.append(price)
        if ((i % p==0 and i!=0)) :
            date_deb = df.loc[j, "Date"]
            date_fin=df.loc[i,"Date"]
            mean = np.mean(liste)
            dfgliss=dfgliss.append({'date_deb':date_deb, 'date_fin': date_fin, 'prix_moyen':mean}, ignore_index=True)
            j=i+1
            liste=[]

    if (j!=len(df)) :
        date_deb = df.loc[j, "Date"]
        date_fin = df.loc[len(df)-1, "Date"]
        mean = np.mean(liste)
        dfgliss = dfgliss.append({'date_deb': date_deb, 'date_fin': date_fin, 'prix_moyen': mean}, ignore_index=True)

    dfgliss.sort_values(by=['date_deb'],ascending=True)
    ll=["-"]
    for i in range(len(dfgliss)-1):
        val2=float(dfgliss.iat[i+1,2])
        val1=float(dfgliss.iat[i,2])
        if (val2>val1) :
            ll.append(1)
        else:
            ll.append(0)

    dfgliss['Variation'] = ll
    table_name = 'meanPrice'  +'per'+periode
    dfgliss.to_sql(table_name, db, if_exists='replace')
    print('data base created')
    db.close()




