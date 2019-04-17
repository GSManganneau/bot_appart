import requests
from utils.db import retrieve, update
from utils.hashing import h11
from utils.time import timestamp
from utils.proxies import get_ok_proxies, update_status_proxy
from utils.user_agents import user_agent_list


class Plateform:

    def __init__(self, name, query, parsing_method, domain_name=None):
        self.name = name
        self.query = query
        self.domain_name = domain_name
        self.parsing = parsing_method
        self.db = "rentBot.db"

    def get_response(self):
        import itertools
        import random
        proxies = get_ok_proxies()
        proxies_and_user_agent = list(itertools.product(proxies, user_agent_list))
        proxy, user_agent = random.choice(proxies_and_user_agent)
        print("getting apparts from %s with ip %s and user-agent %s" % (self.name, proxy, user_agent))
        https_proxy = "https://%s" % proxy
        from requests.exceptions import RequestException
        try:
            res = requests.get(self.query, headers={"User-Agent": user_agent}, proxies={"https": https_proxy})
            return res, proxy
        except RequestException as e:
            print(e)
            update_status_proxy(proxy)
            return self.get_response()

    def parse_response(self):
        result, proxy = self.get_response()
        try:
            if result.ok:
                links = self.parsing(result.text)
                if len(links) == 0:
                    raise Exception("bad response, change proxy")
                if self.domain_name is not None:
                    return [self.domain_name + l for l in links]
                else:
                    return links
        except Exception as e:
            print("request failed with exception %s, try with a new proxy" % e)
            update_status_proxy(proxy)
            return self.parse_response()

    def link_to_insert_request(self, link, table):
        hash_link = h11(link)
        raw_link = link
        site = self.name
        time = timestamp()
        return "insert or ignore into %s (hash_link, raw_link, site, insert_time) values ('%s', '%s', '%s', '%s')" % (
            table, hash_link,
            raw_link, site,
            time)

    def insert_into_db(self, table):
        links = self.parse_response()
        print("links", links)
        queries = [self.link_to_insert_request(link, table) for link in links]
        print("queries", queries)
        for q in queries:
            print("insert appart in db")
            update(q)

    @staticmethod
    def get_new_apparts(table, period):
        now_timestamp = timestamp()
        query = "select * from %s where %s - insert_time < %s" % (table, now_timestamp, period)
        rows = retrieve(query)
        res = ["This appartement from %s match your expectation \n check the link %s" % (row[2], row[1]) for row in
               rows]
        return res



