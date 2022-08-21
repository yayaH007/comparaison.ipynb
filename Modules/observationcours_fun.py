import altair as alt
import pandas as pd
import sqlite3



#observation  graphique des donnée de la bdd
def plot_cours(name,color='red'):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions'+name+'.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(f"select date ,dernier from Action where date>='2019-08-15'  order by date ASC", db)
    start_date = df.Date.iat[0]
    end_date = df.Date.iat[-1]
    max = df.Dernier.max()
    min = df.Dernier.min()
    df["Dernier01"]=df["Dernier"]/max
    x = alt.X('Date:T', scale=alt.Scale(domain=[start_date, end_date], clamp=True))
    y = alt.Y('Dernier:Q', title='Price', scale=alt.Scale(domain=[min - 5, max + 5], clamp=True))
    x_sel = alt.selection_interval(encodings=['x'])
    chart = alt.Chart(df). \
        mark_line(color=color, opacity=0.6). \
        encode(
        x=x,
        y=y,
        tooltip=[alt.Tooltip('Date:T'), alt.Tooltip('Dernier', title='Price')]). \
        properties(
        width=1000,
        height=300
    ).add_selection(x_sel)
    db.close()
    return ( chart.interactive())

def plot_two(name1,name2) :
    chart1 = plot_cours(name1,'steelblue')
    chart2 = plot_cours(name2)
    return ((chart1 + chart2).interactive())

def plot_cours_mean(name,periode) :
    table_name = 'meanPrice'+'per'+periode
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    query=f"select date(julianday(date_deb) + (julianday(date_fin) - julianday(date_deb))/2) as date ,\
            prix_moyen from {table_name}  order by date ASC"
    df = pd.read_sql_query(query, db)
    max = df.prix_moyen.max()
    min = df.prix_moyen.min()
    x = alt.X('date:T',title='Date')
    y = alt.Y('prix_moyen:Q',title='MeanPrice', scale=alt.Scale(domain=[min - 5, max + 5], clamp=True))
    chart = alt.Chart(df). \
        mark_line(color='steelblue', opacity=0.6,point=True). \
        encode(
        x=x,
        y=y,
        tooltip=[alt.Tooltip('date:T'), alt.Tooltip('prix_moyen', title='MeanPrice'+periode)]). \
        properties(
        width=1000,
        height=300 )
    chart2=plot_cours(name)
    db.close()
    return((chart+chart2).interactive())

def plot_variation(name):
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df = pd.read_sql_query(f"select Date ,Var from Action  order by date ASC", db)
    start_date = df.Date.iat[0]
    end_date = df.Date.iat[-1]
    chart = alt.Chart(df).mark_bar().encode(
        x='Date:T',
        y='Var:Q',
        tooltip=[alt.Tooltip('Date:T'), alt.Tooltip('Var', title='  Variation % ')] , 
        color=alt.condition(
            alt.datum.Var > 0,
            alt.value("steelblue"),  # The positive color
            alt.value("orange")  # The negative color
        )).properties(width=1000, height=300)
    db.close()
    return (chart.interactive())


def histogramePriceAll(name) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df=pd.read_sql_query(f"select Dernier from Action order by date desc",db)
    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('Dernier',
        bin=alt.BinParams(maxbins=30),title='Price'),
        y = 'count()',
        tooltip=[alt.Tooltip('Dernier', title='  Price ',bin=alt.BinParams(maxbins=30)),alt.Tooltip('count()')]
    ).properties(
    title='3-years Histogram ')
    return(hist.interactive())


def histogramePriceMonth(name) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df=pd.read_sql_query(f"select Dernier from Action order by date desc ",db)
    df = df.iloc[0:23].copy()
    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('Dernier',
        bin=alt.BinParams(maxbins=30),title='Price'),
        y = 'count()',
        tooltip=[alt.Tooltip('Dernier', title='  Price ',bin=alt.BinParams(maxbins=10)),alt.Tooltip('count()')]
    ).properties(
    title='This Month Histogram ')
    return(hist.interactive())


def histogramePriceTrimestre(name) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df=pd.read_sql_query(f"select Dernier from Action order by date desc",db)
    df = df.iloc[0:65].copy()
    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('Dernier',
        bin=alt.BinParams(maxbins=30),title='Price'),
        y = 'count()',
        tooltip=[alt.Tooltip('Dernier', title='  Price ',bin=alt.BinParams(maxbins=30)),alt.Tooltip('count()')]
    ).properties(
    title='This Trimestre Histogram ')
    return(hist.interactive())


def histogramePriceYear(name) :
    location = 'C:/Users/eyaha/PycharmProjects/Memoire/CoursActions' + name + '.sqlite'
    db = sqlite3.connect(location)
    df=pd.read_sql_query(f"select Dernier from Action order by date desc",db)
    df = df.iloc[0:254].copy()
    hist = alt.Chart(df).mark_bar().encode(
        x = alt.X('Dernier',
        bin=alt.BinParams(maxbins=30),title='Price'),
        y = 'count()',
        tooltip=[alt.Tooltip('Dernier', title='  Price ',bin=alt.BinParams(maxbins=30)),alt.Tooltip('count()')]
    ).properties(
    title='This year Histogram ')
    return(hist.interactive())




