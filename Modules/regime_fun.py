import pandas as pd
import requests
import scrapy
import spacy
import fr_core_news_sm
from collections import Counter
import pytextrank

from sqlalchemy import create_engine
import sqlite3
from datetime import datetime , date


#extraction du consensus des analysts et stockage dans la bdd
def consensusdb(name ,url_consensus):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions'+name+'.sqlite'
    html = requests.get(url_consensus).content
    df = pd.read_html(html,index_col=False)
    cons=df[0]
    cons=cons.iloc[0:-1, [0,-1]]
    cons["Opinion"]=cons["Opinion"].str.split(". ",expand=True).iloc[:,1]
    note=float(cons.iat[-1,-1])
    nb_analyst=int(cons.iat[-2,-1])
    avis_analyst=list(cons.iloc[0:-1,-1])

    nb_achater =int(avis_analyst[0])
    nb_renforcer=int(avis_analyst[1])
    nb_conserver=int(avis_analyst[2])
    nb_alleger=int(avis_analyst[3])
    nb_vendre=int(avis_analyst[4])

    if (1<=note<2) :
        consen="Acheter"
        conseil="La valeur va monter. C’est le moment d’en acheter"
    if (2<=note<3) :
        consen ="Renforcer"
        conseil="Une partie de la hausse est passée ,et elle va continuer."
    if (3 <= note < 4):
        consen ="Conserver"
        conseil ="Ni achater ni vendre"
    if (4 <= note < 5):
        consen ="Alléger"
        conseil ="Pour ceux qui en possèdent, il est temps de vendre . Les autres ne devraient pas s’intéresser à cette valeur."
    if (5 <= note < 6):
        consen ="Vendre"
        conseil ="Une baisse des cours est prédite, il faut vendre le titre dès que possible"

    notelist = [1 * nb_achater,0.75 * nb_renforcer,0.5 * nb_conserver,0.25 * nb_alleger]
    Date = date.today()
    noteF=sum(notelist)/nb_analyst

    df = pd.DataFrame(columns=['Date','nbAnalyst ','nbAchater',
                               'nbRenforcer','nbConserver','nbAlleger',
                               'nbVendre','NoteFinale','ConsensusAnalystes'])

    df=df.append({'Date':Date,'nbAnalyst ':nb_analyst,'nbAchater':nb_achater,
               'nbRenforcer':nb_renforcer,'nbConserver':nb_conserver,
               'nbAlleger':nb_alleger,'nbVendre':nb_vendre,'NoteFinale':noteF,'ConsensusAnalystes':consen},ignore_index=True)

    df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d').dt.date
    db = sqlite3.connect(location)
    max_date=pd.read_sql_query(f"select max(Date) as Date from Consensus ", db).Date.iat[0]
    if ( str(Date)!=str(max_date)):
        df.to_sql('Consensus', db, if_exists='append')
        print("DB completed")
    else :
        print ("no data to add to consensus")
    db.close()





