import os

from sites.plateform import Plateform
from flask import Flask, request
import telegram

from utils.parsing_pages import seloger_parsing, century21_parsing, orpi_parsing, louervite_parsing, guyhoquet_parsing, \
    figaro_immo_parsing, logicimmo_parsing
from utils.queries import se_loger_query, century21_query, orpi_query, louervite_query, guyhoquet_query, \
    figaro_immo_query, logicimmo_query
from utils.subscribers import insert_subscribers, get_subscribers

app = Flask(__name__)
ACCESS_TOKEN = os.getenv("TELEGRAM_TOKEN")
db = "rentBot.db"
bot = telegram.Bot(ACCESS_TOKEN)
bot.set_webhook(url="https://rentbot.westeurope.cloudapp.azure.com/")

seLoger = Plateform("seLoger", se_loger_query, seloger_parsing)
century21 = Plateform("century21", century21_query, century21_parsing, "https://www.century21.fr")
louervite = Plateform("louervite", louervite_query, louervite_parsing, "https://www.louervite.fr/")
orpi = Plateform("orpi", orpi_query, orpi_parsing, "https://www.orpi.com")
guyhoquet = Plateform("guyhoquet", guyhoquet_query, guyhoquet_parsing, "https://www.guy-hoquet.com/")
figaro_immo = Plateform("figaro-immo", figaro_immo_query, figaro_immo_parsing,"https://immobilier.lefigaro.fr")
logicimmo = Plateform("logicimmo", logicimmo_query, logicimmo_parsing)


@app.route("/", methods=['GET', 'POST'])
def new_subscribers():
    update = request.get_json()
    print("update : ", update)
    chat_id = update['message']['chat']['id']
    insert_subscribers(chat_id)
    return "new subscribers added"


@app.route("/publish", methods=['POST'])
def publish_apparts():
    gap = request.get_json()['gap']

    def send_message(chat_id):
        # sends user the text message provided via input response parameter
        apparts = seLoger.get_new_apparts("Apparts", gap)
        print("sending apparts", apparts)
        if len(apparts) > 0:
            for appart in apparts:
                print("appart", appart)
                bot.send_message(chat_id, appart)
        return "success"
    print("publish apparts")
    subs = get_subscribers()
    for sub in subs:
        send_message(sub[0])
    return "Apparts published"


@app.route("/enrich", methods=['POST'])
def enrich_database():
    plateform = request.get_json()['plateform']
    print("enrich the database with apparts from %s \n" % plateform)
    if plateform == "seLoger":
        seLoger.insert_into_db("Apparts")
    if plateform == "century21":
        century21.insert_into_db("Apparts")
    if plateform == "louervite":
        louervite.insert_into_db("Apparts")
    if plateform == "orpi":
        orpi.insert_into_db("Apparts")
    if plateform == "guyhoquet":
        guyhoquet.insert_into_db("Apparts")
    if plateform == "figaro_immo":
        figaro_immo.insert_into_db("Apparts")
    if plateform == "logicimmo":
        logicimmo.insert_into_db("Apparts")
    return "database enriched"


@app.route("/proxies", methods=['POST'])
def enrich_proxies_database():
    from utils.proxies import insert_into_db
    insert_into_db()
    return "new proxies added"


@app.route("/clean_proxies", methods=['POST'])
def clean_proxies():
    from utils.proxies import clean_proxies
    clean_proxies()
    return "proxies' database cleaned"


if __name__ == "__main__":
    app.run()
