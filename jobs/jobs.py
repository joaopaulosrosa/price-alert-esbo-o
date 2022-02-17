from curses import reset_prog_mode
from time import sleep
from django.conf import settings
from lxml import html, etree
import argparse
from collections import OrderedDict
import requests
import json
from base.models import AlarmAsset, Asset, AssetPriceHistory
import datetime
from bs4 import BeautifulSoup
from pandas_datareader import data as web
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import urllib.request
import time
import re

def create_update_assets():
    assets   = Asset.objects.all()
    headers = {
        'User-agent': 'Mozilla/5.0',
        }

    url      = 'https://console.hgbrasil.com/documentation/finance/symbols'
    webpage  = requests.get(url)
    soup     = BeautifulSoup(webpage.content, "html.parser")
    table    = soup.find_all("div", {"class": "card-body"})[0].find('ul')
    rows     = table.find_all('li')

    for row in rows:
        ticker = row.find('code').text
        a = assets.filter(ticker=ticker)
        if list(a) == []:
            response  = requests.get(f'https://finance.yahoo.com/quote/{ticker}.SA', headers=headers)
            if response.status_code == 200:

                company_name = row.find('a').text
                asset = Asset(company_name=company_name, ticker=ticker)
                if asset:
                    asset.save()
                    print(f'{asset.ticker} Created!')

    print('Assets Updated!')


def test_g():
    assets = Asset.objects.all()

    for asset in assets:
        response = requests.get(f'https://www.google.com/finance/quote/{asset}:BVMF?hl=pt')
        if response.status_code == 200:
            soup    = BeautifulSoup(response.text, "html.parser")
            price   = soup.find('div', {'class': 'YMlKec fxKbKc'})
            if price == None:
                asset.delete()
                asset.save
                print(f'{asset} DELETED!')



            else:
                preco = re.sub('[R$ ]', '', price.text)
                current = re.sub('[,]', '.', preco)
                history = AssetPriceHistory(asset=asset, price=current)
                if history:
                    history.save()
                    print(history)

    print('======== DONE =========')


# def last_pregao():
#     url = 'https://api-cotacao-b3.labdo.it/api/sysinfo'
#     return requests.get(url).json()['dt_ultimo_pregao']

# def teste():
#     assets = Asset.objects.all()
#     pregao = last_pregao()
#     url = f'https://api-cotacao-b3.labdo.it/api/cotacao/dt/{pregao}'
#     response  = requests.get(url).json()
#     ativos = []
#     # parser = html.fromstring(response.text)
#     # price = parser.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')
#     for asset in assets:
#         for a in response:
#             if a['cd_acao'] == asset.ticker:
#                 ativos.append(asset.ticker)

#     print(len(ativos))




    # for asset in assets:
    #     response = requests.get(f'https://www.moneytimes.com.br/cotacao/{asset}')
    #     if response.status_code == 200:

    #         soup     = BeautifulSoup(response.content, "html.parser")
    #         price = soup.find_all('span', {'class': 'tv-ticker-item-last__last js-symbol-last apply-overflow-tooltip'})

    #         print(price)

    #     else:
    #         print(f'{asset} REJECTED')


    # with urllib.request.urlopen('https://br.investing.com/equities/azul-sa-pref') as url:
    #     parser = url.read()
    # with open(response, 'r', encoding='utf8') as f:
    #     text_html = f.read()

    # def build_lxml_tree(_html):
    #     tree = html.fromstring(_html)
    #     tree = etree.ElementTree(tree)
    #     return tree

    # tree = build_lxml_tree(text_html)
    # result = tree.xpath('/html/body/div[1]/div[2]/div/div/div[3]/main/div/div[1]/div[2]/div[1]/span')
    # print(result)



    # preco = parser.xpath('//*[@id="__next"]/div[2]/div/div/div[3]/main/div/div[1]/div[2]/div[1]/span')
    # price = parser.find_all('span', {'class': 'chart-info-val ng-binding'})

    # print(preco)

    # assets = Asset.objects.all()
    # for asset in assets:

    #     url = f'https://economia.uol.com.br/cotacoes/bolsas/acoes/bvsp-bovespa/{asset.ticker.lower()}-sa/'
    #     headers = {
    #     'User-agent': 'Mozilla/5.0',
    #     }
    #     response  = requests.get(url, headers=headers)

    #     print(response)

    # print(f'Done! ======> {datetime.datetime.now()}')


        # if response.status_code == 200:

        #     parser = html.fromstring(response.text)
        #     price = parser.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')

        #     if price == [] or price[0].text == None:
        #         print(asset)
        #     else:
        #         price_hist = AssetPriceHistory(asset=asset, price=price[0].text)
        #         if price_hist:
        #             price_hist.save()


    # print(f'Done! ======> {datetime.datetime.now()}')



# def test_y():
#     assets = Asset.objects.all()
#     print(f'Starting =====> {datetime.datetime.now()}')
#     for asset in assets:

#         url = f'https://finance.yahoo.com/quote/{asset}.SA'
#         headers = {
#         'User-agent': 'Mozilla/5.0',
#         }
#         response  = requests.get(url, headers=headers)

#         if response.status_code == 200:

#             parser = html.fromstring(response.text)
#             price = parser.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]')

#             if price == [] or price[0].text == None:
#                 print(asset)
#             else:
#                 price_hist = AssetPriceHistory(asset=asset, price=price[0].text)
#                 if price_hist:
#                     price_hist.save()


#     print(f'Done! ======> {datetime.datetime.now()}')





# RETURN HTML CONTENT
# def soup_content(url):
#     session      = requests.Session()
#     html_content = session.get(url).text
#     return BeautifulSoup(html_content, 'html.parser')


# def num_of_pages():
#     url = 'https://www.ivalor.com.br/empresas/listagem#'
#     pagination = soup_content(url).find_all('ul', {'class':'pagination'})[0]
#     return int(pagination.find_all('li')[-2].text)


# def update_assets():
#     assets       = Asset.objects.all()
#     max_pages    = num_of_pages()
#     current_page = 1

#     while current_page <= max_pages:
#         current_url = f'https://www.ivalor.com.br/empresas/listagem?p={current_page}'
#         soup        = soup_content(current_url)
#         dom         = etree.HTML(str(soup))


#         print(table.text)

        # for r in row:
        #     name = r.find_all('td')[2].text
        #     tick = r.find_all('b')
        #     for t in tick:
        #         if assets.filter(ticker = t.text):
        #             print(f'{t} Already Exists!')
        #         else:
        #             print(f'Creating ====>  |{t.text}| !')
        #             asset = Asset(company_name = name, ticker = t.text)
        #             if asset:
        #                 asset.save()
        #                 print(f'Empresa:{name} | ticker:{t.text} -> Created!')
        #             else:
        #                 print('fuck')

        # current_page += 1

    # print('Update Done!')


# def save_price_history():
#     assets = Asset.objects.all()
#     for asset in assets:
#         data = requests.get(f'https://api.hgbrasil.com/finance/stock_price?key=3ebed24b&symbol={asset.ticker}').json()['results'][asset.ticker]
#         if 'error' in data:
#             asset.delete()
#             asset.save
#             print('{asset.ticker} Deleted!')
        # else:
        #     print(data['price'])
        # asset_price = AssetPriceHistory(asset=asset , price=data['price'])
        # print(data.price)
        # if asset_price:
        #     asset_price.save()
        #     print(f'{asset_price.asset.ticker} Created!')
        # else:
        #     print('asset price not saved')
