from Modules.prixcours_bdd import create_db,db_complete
from Modules.moyenneglissante_bdd import PriceMean
from Modules.regime_fun import consensusdb
from Modules.datacleaning import CreateNewsdbPeriode,CreateNewsdbDay ,MLdata
from textblob_fr import PatternTagger,PatternAnalyzer
from textblob import Blobber
tb=Blobber(pos_tagger=PatternTagger(),analyzer=PatternAnalyzer())


url1_Total="https://www.boursorama.com/_formulaire-periode/page-"
url2_Total="?symbol=1rPTTE&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D=3Y&historic_search%5Bperiod%5D=1"
url_consensus_total="https://www.boursorama.com/cours/consensus/1rPTTE/"
name1="Total"

url1_airbnb="https://www.boursorama.com/_formulaire-periode/page-"
url2_airbnb="?symbol=ABNB&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D=3Y&historic_search%5Bperiod%5D=1"
url_consens_airbnb="https://www.boursorama.com/cours/consensus/ABNB/"
name2="Airbnb"

url1_cac="https://www.boursorama.com/_formulaire-periode/page-"
url2_cac="?symbol=1rPCAC&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D=3Y&historic_search%5Bperiod%5D=1"
name3="CAC40"

url1_lvmh="https://www.boursorama.com/_formulaire-periode/page-"
url2_lvmh="?symbol=1rPMC&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D=3Y&historic_search%5Bperiod%5D=1"
url_consens_lvmh="https://www.boursorama.com/cours/consensus/1rPMC/"
name4="LVMH"

url1_dow="https://www.boursorama.com/_formulaire-periode/page-"
url2_dow="?symbol=%24INDU&historic_search%5BstartDate%5D=&historic_search%5Bduration%5D=3Y&historic_search%5Bperiod%5D=1"
name5="Dow_Jones"


### exp : Total
create_db(url1_Total,url2_Total,name1)# creer la nouvelle bdd avec l'historique disponible sur le site
db_complete(url1_Total,url2_Total,name1)  # completer l'historique si de nouvelles valeurs sont diponibles

#calcule des moyennes glissantes par semaine , mois et trismestre
PriceMean(name1,"Week")
PriceMean(name1,"Month")
PriceMean(name1,"Trimester")

#extraction du consensus disponible aujourd'hui et enregistrement dans la bdd
consensusdb(name1 ,url_consensus_total)

#enregister les articles d'actualités groupés par periode dans la bdd
#cette etape vient apres le lancement des scrapper pour l'extraction du site Boursorama
CreateNewsdbDay(name1)
CreateNewsdbPeriode(name1,"Month")
CreateNewsdbPeriode(name1,"Week")


#nettoyage des textes d'actualité et preparation pour les modeles ML
MLdata(name1,"Month")
MLdata(name1,"Week")














