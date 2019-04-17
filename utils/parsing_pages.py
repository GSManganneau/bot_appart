from bs4 import BeautifulSoup
import json


def seloger_parsing(response):
    soup = BeautifulSoup(response, features="html.parser")
    a_tags = soup.find_all("a", class_="c-pa-link link_AB")
    print("a_tags", a_tags)
    links = [a.get("href") for a in a_tags]
    return links


def century21_parsing(response):
    page = BeautifulSoup(response, features="html.parser")
    bloc_annonce = page.find(id="blocANNONCES")
    list_biens = bloc_annonce.find_all("ul")[0]
    a_tags = list_biens.find_all('a')
    links = [a.get("href") for a in a_tags]
    return links


def louervite_parsing(response):
    j = json.loads(response)
    links = [r["Url"] for r in j["d"]["Data"]["Resultats"]["Resultats"]]
    return links


def orpi_parsing(response):
    if "o-grid__col o-grid__col--12" in response:
        page = BeautifulSoup(response, features="html.parser")
        all_annonces = page.find('div', attrs={"class": "o-grid__col o-grid__col--12"})
        matched_annonces_bloc = all_annonces.find('ul')
        a_tags = matched_annonces_bloc.find_all('a')
        links = [a.get("href") for a in a_tags]
        return links
    else:
        print("no good reponse")


def guyhoquet_parsing(response):
    soup = BeautifulSoup(response, features="html.parser")
    listing = soup.find('div', attrs={'id': 'listing_bien'})
    a_tags = listing.find_all('a')
    links = [a.get("href") for a in a_tags]
    tmp = list(filter(lambda x: x is not None, links))
    tmp2 = list(filter(lambda x: "#" not in x, tmp))
    res = [x.replace("..", "") for x in tmp2]
    return res


def figaro_immo_parsing(response):
    soup = BeautifulSoup(response, features="html.parser")
    items = soup.find('div', attrs={'class': 'container-items js-container-items'})
    a_tags = items.find_all('a')
    all_links = [a.get('href') for a in a_tags]
    words = ["edito", "immobiliere", "cadrimmo", "ciblage"]
    links = list(filter(lambda x: all(w not in x for w in words), all_links))
    return links


def logicimmo_parsing(response):
    soup = BeautifulSoup(response, features="html.parser")
    offers = soup.find_all('p', {'class': 'offer-type'})
    a_tags = [offer.find('a') for offer in offers]
    links = [a.get('href') for a in a_tags]
    return list(filter(lambda x: "orpi" not in x, links))




