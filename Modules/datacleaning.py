import pandas as pd
import sqlite3
from datetime import datetime
from collections import Counter
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob import Blobber
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


#creation de la base de données des textes d'article groupé par periode
def CreateNewsdbPeriode(name,periode) :
    nlp = spacy.load("fr_core_news_sm")
    cch=name.lower()
    news = pd.read_csv('./news_scrapping/'+name+'/news_'+cch+'.csv')
    datesdf= news['date']
    dateslist=list(datesdf)
    dateslist =[datetime. strptime(date_str, '%Y-%m-%d').date() for date_str in dateslist ]
    dates=set(dateslist)
    datesnews=list(dates)

    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    query = "select *  from meanPriceper"+periode
    df = pd.read_sql_query(query, db)

    ct = []
    subjectivity1 = []
    polarite1 = []
    top20 = []
    subjectivity20 = []
    polarite20 = []
    top30 = []
    subjectivity30 = []
    polarite30 = []
    top40 = []
    subjectivity40 = []
    polarite40 = []
    textliste = []

    for i in range(len(df)):
        text=''
        date_deb_str = df.iloc[i, 1]
        date_fin_str = df.iloc[i, 2]
        date_deb=datetime. strptime(date_deb_str, '%Y-%m-%d').date()
        date_fin=datetime. strptime(date_fin_str, '%Y-%m-%d').date()

        datesnewsperiode=[date for date in datesnews if date>=date_deb and date<=date_fin ]

        for d in datesnewsperiode :
            dstr=str(d)
            dff=news.query('date==@dstr')
            for j in range(len(dff)):
                text = text + (dff.iat[j, 1]) + '\n'

        res = clean(text, nlp)
        ct.append(res[0])
        polarite1.append(res[1])
        subjectivity1.append(res[2])
        textliste.append(text)
        top20.append(res[3])
        polarite20.append(res[4])
        subjectivity20.append(res[5])
        top30.append(res[6])
        polarite30.append(res[7])
        subjectivity30.append(res[8])
        top40.append(res[9])
        polarite40.append(res[10])
        subjectivity40.append(res[11])

    df['text'] = textliste
    df['cleanText'] = ct
    df['cleanTextPolarity'] = polarite1
    df['cleanTextSubjectivity'] = subjectivity1

    df['top20words'] = top20
    df['top20wordsPolarity'] = polarite20
    df['top20wordsSubjectivity'] = subjectivity20

    df['top30words'] = top30
    df['top30wordsPolarity'] = polarite30
    df['top30wordsSubjectivity'] = subjectivity30

    df['top40words'] = top40
    df['top40wordsPolarity'] = polarite40
    df['top40wordsSubjectivity'] = subjectivity40

    df.to_sql('NewsAnalysisPer'+periode, db, if_exists='replace')
    print('NewsAnalysisPer'+periode +'db' +name+" created ")


#cration de la table d'article d'actulité par jour
def CreateNewsdbDay(name) :
    nlp = spacy.load("fr_core_news_sm")
    cch = name.lower()
    news = pd.read_csv('./news_scrapping/' + name + '/news_' + cch + '.csv')
    datesdf = news['date']
    dateslist = list(datesdf)
    dateslist = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in dateslist]
    dates = set(dateslist)
    datesnews = list(dates)

    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    query = "select *  from Action"
    df = pd.read_sql_query(query, db)

    ct = []
    subjectivity1 = []
    polarite1 = []
    top20 = []
    subjectivity20 = []
    polarite20 = []
    textliste=[]

    for i in range(len(df)):
        text = ''
        date_str = df.iloc[i, 1]
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        dff = news.query('date==@date_str')

        for j in range(len(dff)):
            text = text + (dff.iat[j, 1]) + '\n'

        res = clean(text, nlp)
        textliste.append(text)
        ct.append(res[0])
        polarite1.append(res[1])
        subjectivity1.append(res[2])

        top20.append(res[3])
        polarite20.append(res[4])
        subjectivity20.append(res[5])

    df['text']=textliste
    df['cleanText'] = ct
    df['cleanTextPolarity'] = polarite1
    df['cleanTextSubjectivity'] = subjectivity1

    df['top20words'] = top20
    df['top20wordsPolarity'] = polarite20
    df['top20wordsSubjectivity'] = subjectivity20

    df.to_sql('NewsAnalysisPerDay', db, if_exists='replace')
    print('NewsAnalysisPerDay db ' + name + " created ")



#nettoyage des texte d'article d'actualité
def clean(text,nlp):
    doc = nlp(text)
    stop_words = set(STOP_WORDS)  # stop words
    deselect_stop_words = ['n\'', 'ne', 'pas', 'plus', 'personne', 'aucun', 'ni', 'aucune', 'rien']
    for w in deselect_stop_words:
        if w in stop_words:
            stop_words.remove(w)
        else:
            continue
    liste = []
    for token in doc:
        liste.append((token, token.pos_))
    liste2 = []
    for token, tag in liste:
        if not ((token.text in stop_words) or (len(token.text) == 1) or (len(token.text) == 2)):
            liste2.append((token, tag))
    liste3 = []
    for token, tag in liste2:
        liste3.append((token.lemma_))

    ct = (' '.join(liste3))
    sentiment= tb(ct).sentiment

    word_freq = Counter(liste3)

    common_words20 = word_freq.most_common(20)
    topp20 = [word[0] for word in common_words20]
    top20 = (' '.join(topp20))
    sentiment20=tb(top20).sentiment

    common_words30 = word_freq.most_common(30)
    topp30 = [word[0] for word in common_words30]
    top30 = (' '.join(topp30))
    sentiment30 = tb(top30).sentiment

    common_words40 = word_freq.most_common(40)
    topp40 = [word[0] for word in common_words40]
    top40 = (' '.join(topp40))
    sentiment40 = tb(top40).sentiment
    return(ct,sentiment[0],sentiment[1],top20,sentiment20[0],sentiment20[1],top30,sentiment30[0],sentiment30[1],top40,sentiment40[0],sentiment40[1])


#creation de la table de bdd pour les modeles ML
def MLdata(name,periode):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    if(periode=="Week" or periode=="Month") :
        query='select Variation , text,cleanText, cleanTextPolarity,cleanTextSubjectivity,top20words,top20wordsPolarity,top20wordsSubjectivity,top30words,top30wordsPolarity,top30wordsSubjectivity ,top40words,top40wordsPolarity,top40wordsSubjectivity  from NewsAnalysisPer'+periode+' order by date_deb asc'
    if(periode=="Day") :
        query='select Variation ,text , cleanText,cleanTextPolarity,cleanTextSubjectivity,top20words,top20wordsPolarity,top20wordsSubjectivity from NewsAnalysisPer'+periode+' order by Date asc'
    df = pd.read_sql_query(query, db)
    variation=list(df['Variation'])
    variation=[variation[i+1] for i in range(len(variation)-1)]
    variation.append('-')
    df=df.drop(columns=['Variation'])
    df['variation']=variation
    df.drop(df[df.text==""].index, inplace=True)
    df.to_sql('MLData'+periode, db, if_exists='replace')
    print('MLData'+periode+' created')



