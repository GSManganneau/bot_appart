from utils.time import timestamp
import sqlite3
db = "rentBot.db"


def get_new_proxies():
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import re
        chrome_path = '/usr/bin/google-chrome'
        chromedriver_path = '/usr/local/bin/chromedriver'
        window_size = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % window_size)
        chrome_options.binary_location = chrome_path
        driver = webdriver.Chrome(executable_path=chromedriver_path,
                                  chrome_options=chrome_options)
        driver.get("http://www.gatherproxy.com/embed/?p=443")
        elements = driver.find_elements_by_tag_name("tbody")
        text = elements[0].text
        proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text)
        driver.close()
        return proxies


def generate_insert_query(ip):
    now = timestamp()
    query = "insert or ignore into proxies (ip_address, status, insert_time) values ('%s', 'ok', '%s')" % (ip, now)
    return query


def insert_into_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    proxies = get_new_proxies()
    queries = [generate_insert_query(ip) for ip in proxies]
    for query in queries:
        print("query: ", query)
        cursor.execute(query)
    conn.commit()
    conn.close()


def get_ok_proxies():
    query = "select ip_address from proxies where status = 'ok'"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return list(res)


def update_status_proxy(ip):
    query = "update proxies SET status = 'ko' where ip_address = '%s'" % ip
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def clean_proxies():
    now = timestamp()
    query = "delete from proxies where status = 'ko' or %s - insert_time > 300" % now
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
