import requests
import csv
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep

global url
url = 'https://www.trulia.com/for_rent/Las_Vegas,NV/1p_baths/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,TIC_type/'
host = 'https://www.trulia.com'

def get_html(url, useragent=None, proxy=None, params=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    r.encoding = 'utf8'
    return r.text

def main():
    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')
    for i in range(15):
        a = uniform(2,7)
        sleep(a)
        proxy = {'http':'http://'+choice(proxies)}
        useragent= {'User-Agent':choice(useragents)}
        try:
            html =get_html(url, useragent, proxy)
            print('User-Agent: ', useragent, '\nProxy: ', proxy)
            print('-----------------------------------')
        except:
            continue

    get_content(html)

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    apartments = []
    for ultag in soup.find_all('ul', attrs={'data-testid':'search-result-list-container'}):
        for litag in ultag.find_all('li', class_='Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-b7y9ki-2 jiZmPM'):
            try:
                apartments.append({
                    'title': litag.find(attrs={'data-testid':'property-street'}).text,
                    'location':litag.find(attrs={'data-testid':'property-region'}).text,
                    'link': host+str(litag.find('a', class_='PropertyCard__StyledLink-m1ur0x-3 dgzfOv').get('href')),
                    'price':litag.find(attrs={'data-testid':'property-price'}).text,
                    'bedrooms':litag.find(attrs={'data-testid':'property-beds'}).text
               })
            except AttributeError:
                apartments.append({
                    'title': '--',
                    'location': '--',
                    'link': '--',
                    'price': '--',
                    'bedrooms': '--'
                })

    writing_csv(apartments)

    # if len(apartments) == 0:
    #     print('The list "Apartments" is empty.')

def writing_csv(apartments):
    items = len(apartments)
    print('Количество обьявлений',items)
    with open('rentInLV.csv', 'a', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
        for index in range(items):
            writer.writerow((apartments[index]['title'], apartments[index]['location'], apartments[index]['price'], apartments[index]['link'],apartments[index]['bedrooms']))

main()
# def parse():
#     html = get_html(URL)
#     if html.status_code == 200:
#         get_content(html.text)
#     else:
#         print(html.status_code)
#         print('Error')

