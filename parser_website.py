import requests
import asyncio
from bs4 import BeautifulSoup as BS4
import os
import lxml

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
URLS = ['https://vos-mo.ru/about/rasporyazheniya-administratsii-rayona/',
       'https://vos-mo.ru/napravleniya/arkhitektura-i-gradostroitelstvo/obshchestvennye-obsuzhdeniya/',
       'https://vos-mo.ru/about/postanovleniya-administratsii-rayona/']
URLS_1 = ['https://pavpos.ru/doc_category/post_glavy/',
        'https://pavpos.ru/doc_category/rasp_glavy/',
        'https://pavpos.ru/doc_category/docums/']


def read_keywords():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, 'keywords.txt'), 'r', encoding='utf-8') as f:
        keywords = ''.join(f.readlines()).strip().split('\n')
    return keywords

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    soup = BS4(r.text, 'lxml')
    return soup

def write_filtr(name_doc):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, 'filtr.txt'), 'a', encoding='utf-8') as f:
        f.write(f'{name_doc.strip()}\n')

def read_filtr():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_path, 'filtr.txt'), 'r', encoding='utf-8') as f:
        filtr_read = ''.join(f.readlines()).strip().split('\n')

    return filtr_read

def admmozhaysk(keywords):
    all_docs_mozhaysk = {}
    for keys in keywords:#[0:1]
        url = 'http://www.admmozhaysk.ru/docs/search?query='
        for keyword in keys.split(' '): url += f'{keyword.lower()}+'
        url = url.strip('+')
        # print(url)

        soup = get_html(url)

        containers = soup.find_all('a', class_='document is-simple mt')

        for container in containers:
            name_doc = container.find('b').text.strip()
            href_doc = f"http://www.admmozhaysk.ru{container.get('href')}" #/docs
            all_docs_mozhaysk[name_doc] = href_doc

    return all_docs_mozhaysk

def main_mozhaysk():
    keywords = read_keywords()
    all_docs_mozhaysk = admmozhaysk(keywords)
    return all_docs_mozhaysk

def vos_mo(keywords):
    all_docs_vos_mo = {}

    for URL in URLS:
        # print(URL)
        soup = get_html(URL)
        containers = soup.find('div', class_='news-list').find_all('div', class_='news-item')
        for container in containers:
            # print(container)
            name = container.find('h3').find('a').text.strip()
            href = f"https://vos-mo.ru{container.find('h3').find('a').get('href')}"
            all_docs_vos_mo[name] = href

    return all_docs_vos_mo

def main_vos_mo():
    keywords = read_keywords()
    # print(keywords)
    all_docs_vos_mo = vos_mo(keywords)
    return all_docs_vos_mo


#//////////////////////////////////////////////////////////////

def pavpos(keywords):
    all_docs_pavpos = {}

    for URL in URLS_1:
        # print(URL)
        soup = get_html(URL)
        containers = soup.find('div', class_='list').find_all('div', class_='item_wrap')
        for container in containers:
            name_1 = container.find('div', class_='name').find('a').text.strip()
            name_2 = container.find('div', class_='desc')#.text.strip()

            if name_2.find_all('a') != []:
                find_a_txt = ''
                for find_a in name_2.find_all('a'):
                    find_a_txt += f'{find_a.text}\n'
                name_2 = name_2.text.replace(find_a_txt, '')
            else:
                name_2 = name_2.text
            name_2 = name_2.strip()

            names = f'{name_1} {name_2}'.split('\n')#.replace('\n', ' ')
            name = ''
            for n in names: name += f'{n.strip()} '
            href = container.find('div', class_='name').find('a').get('href')
            all_docs_pavpos[name] = href

    # for key, val in all_docs_pavpos.items():
    #     print(f'{key} - {val}')
    return all_docs_pavpos

def main_pavpos():
    keywords = read_keywords()
    all_docs_pavpos = pavpos(keywords)
    return all_docs_pavpos



def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    keywords = read_keywords()

    mozhaysk = main_mozhaysk()

    vos_mo = main_vos_mo()
    pavpos = main_pavpos()

    if 'filtr.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'filtr.txt'), 'a') as f:
            pass

    return mozhaysk, vos_mo, pavpos

