from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import html2text
from urllib.request import urlopen
import requests
import random
import time
import json
import pandas as pd

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
]

s = requests.Session()
with open(r'D:\scrapper\facebook_cookie.json') as c:
    load = json.load(c)

for cookie in load:
    s.cookies.set(cookie['name'], cookie['value'])

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
options.add_argument('--disable-gpu')
options.add_argument('disable-blink-features=AutomationControlled')


def check_html(text, query):
    soup = BeautifulSoup(text, 'lxml')
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    out = '\n'.join(chunk for chunk in chunks if chunk)

    out = out.lower()
    if len(out) == 0:
        return "doubt", 0
    count_occurance = (out.count(query.lower()))
    if count_occurance > 0:
        return True, count_occurance
    else:
        if "javascript" in out or "robot" in out:
            return "doubt", 0

        return False, 0


def get_text_html(url, query):
    user_agent = random.choice(USER_AGENTS)
    # options.add_argument('user-agent={}'.format(user_agent))
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\admin\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=options)

    header = {
        'user-agent': user_agent,
        'referer': 'https://www.google.com/'
    }
    try:
        request_page = s.get(url, headers=header, timeout=20)
        output, occu = check_html(request_page.text, query)
    except Exception as err:

        return False, 0

    if output != True:
        try:
            driver.get(url)
            time.sleep(5)
            output, occu = check_html(driver.page_source, query)
            if output != True:
                return False, 0
        except:
            return False, 0
    return output, occu


# print(get_text_html("https://open.spotify.com/artist/6niO7WSbw5n0nD58jPi2Mx","priest"))


start = datetime.now()


def main_runner(queries):
    for query in queries:
        search = query.replace(' ', '+')
        results = 100
        url = (f"https://www.google.com/search?q={search}&num={results}")

        requests_results = requests.get(url)
        soup_link = BeautifulSoup(requests_results.content, "html.parser")
        links = soup_link.find_all("a")

        data = []
        for link in links:
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                title = link.find_all('h3')
                if len(title) > 0:

                    dictionary = {}
                    link = (link.get('href').split("?q=")[1].split("&sa=U")[0])
                    print(link)
                    if "youtube" in link:
                        link = link.replace("%3Fv%3D", "?v=")
                    dictionary["link"] = link
                    try:
                        r_check = requests.head(link, timeout=10)
                        try:
                            if r_check.status_code == 302 or "text/html" not in r_check.headers["Content-Type"]:
                                dictionary["title"] = (title[0].getText())
                                dictionary["present"] = False
                                dictionary["occurance"] = 0
                                data.append(dictionary)
                                continue
                        except:
                            pass

                        dictionary["title"] = (title[0].getText())
                        output, occurance = get_text_html(
                            dictionary["link"], query)
                        dictionary["present"] = output
                        dictionary["occurance"] = occurance
                        data.append(dictionary)
                        print(output)
                        print("-------------------------------")
                        time.sleep(5)
                    except:
                        time.sleep(5)

        df = pd.DataFrame.from_dict(data)
        df.to_csv(r'{}_gen.csv'.format(query), index=False, header=True)


queries = ["lilith"]
main_runner(queries)
print(datetime.now()-start)


'''
scrape images
need input output formates
put multiprocessing accordingly
add proxies
check where the results are wrong and why and add them
check if require logins
make it ready for the deployment
'''
