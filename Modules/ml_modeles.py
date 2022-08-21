from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score


#variation cours prediction
def SentimentModele(name,periode,choice):
    paramlist = [0,0.05, 0.06, 0.07, 0.08,  0.09, 0.1, 0.101, 0.102, 0.103, 0.104, 0.105, 0.106]
    query ="select cleanTextPolarity, variation,top20wordsPolarity from MLData"+periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(query, db)
    column=["Parametre"]
    column.extend(paramlist)
    dff = pd.DataFrame(columns=column)
    if (choice=="CleanText"):
        listePolarity=list(df['cleanTextPolarity'])
    if (choice=="FrequentWords"):
        listePolarity= list(df['top20wordsPolarity'])
    listeVariation=list(df['variation'])
    listePolarity.pop()
    listeVariation.pop()
    resultat=[]
    bestparam=0
    bestsomme=0
    for param in paramlist :
        listeRes = []
        for el in listePolarity :
            if el>=param :
                listeRes.append(1)
            if el<param :
                listeRes.append(0)
        somme=0
        for i in range(len(listeVariation)):
            if int(listeVariation[i])==listeRes[i]:
                 somme=somme+1
        if (somme>bestsomme):
            bestsomme=somme
            bestparam=param
        resultat.append(float(somme / len(listeVariation)))
    ligne=['Ratio']
    ligne.extend(resultat)
    dff.loc[1]=ligne
    return(bestparam,dff)


def modele2 (name,periode) :
    query = "select text, variation,cleanText from MLData" + periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(query, db)
    X=df["cleanText"]
    Y=df["variation"]
    X_train, X_val, y_train, y_val = train_test_split(X, Y, train_size=0.75)
    vectorizer = TfidfVectorizer()
    train_vectors = vectorizer.fit_transform(X_train)
    test_vectors = vectorizer.transform(X_val)
    for c in [0.005,0.01, 0.05, 0.25, 0.5, 1]:
        lr = LogisticRegression(C=c)
        lr.fit(train_vectors, y_train)
        print("Précision pour C=%s: %s" % (c, accuracy_score(y_val, lr.predict(test_vectors))))



def modele3(name,periode):
    query = "select variation,cleanText,top20words , top30words ,top40words from MLData" + periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(query, db)
    X = df["top20words"]
    Y = df["variation"]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.75)
    vectorizer = TfidfVectorizer()
    train_vectors = vectorizer.fit_transform(X_train)
    test_vectors = vectorizer.transform(X_test)
    clf = MultinomialNB().fit(train_vectors, y_train)
    predicted = clf.predict(test_vectors)
    print(accuracy_score(y_test, predicted))



def modele4(name, periode, spacy_tokenizer=None):
    query = "select variation,cleanText,top20words , top30words ,top40words from MLData" + periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(query, db)
    X = df["top20words"]
    Y = df["variation"]
    vectorizer = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    classifier = LinearSVC()
    tfvectorizer = TfidfVectorizer(tokenizer=spacy_tokenizer)
    pipe = Pipeline([#("cleaner", predictors()),
                     ('vectorizer', vectorizer),
                     ('classifier', classifier)])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.7)
    pipe.fit(X_train, y_train)
    print("Accuracy: ", pipe.score(X_test, y_test))



def modele5(periode):
    names=["Airbnb","Total","LVMH"]
    df = pd.DataFrame(columns=['variation','cleanText','top20words' , 'top30words' ,'top40words'])
    query = "select variation,cleanText,top20words , top30words ,top40words from MLData" + periode
    for name in names :
        location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
        db = sqlite3.connect(location)
        dff = pd.read_sql_query(query, db)
        df=pd.concat([df,dff])
    X = df["cleanText"]
    Y = df["variation"]
    cv = CountVectorizer(binary=True)
    cv.fit(X)
    X_onehot = cv.transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_onehot, Y, train_size=0.75)  # ,random_state=42
    for c in [0.005, 0.01, 0.05, 0.25, 0.5, 1]:
        lr = LogisticRegression(C=c)
        lr.fit(X_train, y_train)
        print("Précision pour C=%s: %s" % (c, accuracy_score(y_val, lr.predict(X_val))))



def modele6(name, periode) :
    if periode=="Day" :
        query="select  text ,variation,cleanText,top20words  from MLData" + periode +" where variation is not '-'"
    else :
        query = "select  text ,variation,cleanText,top30words  from MLData" + periode +" where variation is not '-'"
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(query, db)

    if periode=="Day":
        X = df["top20words"]
    else :
        X = df["top30words"]
    Y = df["variation"].astype(int)

    X=list(X)
    Y=list(Y)
    X.pop()
    Y.pop()
    k=int(len(X)*0.75)

    training_text = X[0:k]
    testing_text = X[k:]
    training_labels = Y[0:k]
    testing_labels = Y[k:]
    # preprocess
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(training_text)
    word_index = tokenizer.word_index
    training_sequences = tokenizer.texts_to_sequences(training_text)
    training_padded = pad_sequences(training_sequences, maxlen=120, padding='post', truncating='post')
    testing_sequences = tokenizer.texts_to_sequences(testing_text)
    testing_padded = pad_sequences(testing_sequences, maxlen=120, padding='post', truncating='post')
    # convert lists into numpy arrays to make it work with TensorFlow
    training_padded = np.array(training_padded)
    training_labels = np.array(training_labels)
    testing_padded = np.array(testing_padded)
    testing_labels = np.array(testing_labels)
    print(training_padded)
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(10000, 16, input_length=120),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(24, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    num_epochs = 10
    history = model.fit(training_padded,
                        training_labels,
                        epochs=num_epochs,
                        validation_data=(testing_padded, testing_labels),
                        verbose=2)



