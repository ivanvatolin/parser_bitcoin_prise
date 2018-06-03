# 1. Парсер однопоточный
# 2. Замер времени
# 3. Multiprocessing
# 4. Замер времени
# 5. Экспорт в CSV
from datetime import datetime

import requests
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool

URL = 'https://coinmarketcap.com/all/views/all/'


def get_html(url):
    resp = requests.get(url)
    return resp.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='text-large').text
    except Exception:
        name = ''

    try:
        price = soup.find('span', id='quote_price').text
    except Exception:
        price = ''

    data = {'name': name.replace('\n',' ').strip(),
            'price': price.replace('\n',' ').strip()}

    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'].strip(),
                        data['price'].strip()))
        print('{} parsed'.format(data['name']))


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start_total = datetime.now()
    all_links = get_all_links(get_html(URL))

    with Pool(10) as p:
        p.map(make_all, all_links)

    # make_all(all_links)

    print('All links parsed for', str(datetime.now() - start_total))


if __name__ == '__main__':
    main()
