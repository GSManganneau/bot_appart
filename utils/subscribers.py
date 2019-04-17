from utils.db import retrieve, update


def get_subscribers():
    query = "select * from subscribers"
    rows = retrieve(query)
    return rows


def insert_subscribers(id):
    query = "insert or ignore into subscribers (id) values ('%s')" % id
    update(query)

