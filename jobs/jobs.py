from django.conf import settings
import requests
import json
from base.models import Asset
import datetime

# RETURN HTML CONTENT
def soup_content(url):
    from bs4 import BeautifulSoup
    session      = requests.Session()
    html_content = session.get(url).text
    return BeautifulSoup(html_content, 'html.parser')


def num_of_pages():
    url = 'https://www.ivalor.com.br/empresas/listagem#'
    pagination = soup_content(url).find_all('ul', {'class':'pagination'})[0]
    return int(pagination.find_all('li')[-2].text)


def update_assets():
    assets       = Asset.objects.all()
    max_pages    = num_of_pages()
    current_page = 1

    while current_page <= max_pages:
        current_url = f'https://www.ivalor.com.br/empresas/listagem?p={current_page}'
        soup        = soup_content(current_url)
        table       = soup.find('tbody')
        row         = table.find_all('tr')

        for r in row:
            name = r.find_all('td')[2].text
            tick = r.find_all('b')
            for t in tick:
                if assets.filter(ticker = t.text):
                    print(f'{t} Already Exists!')
                else:
                    print(f'Creating ====>  |{t.text}| !')
                    asset = Asset(company_name = name, ticker = t.text)
                    if asset:
                        asset.save()
                        print(f'Empresa:{name} | ticker:{t.text} -> Created!')
                    else:
                        print('fuck')

        current_page += 1

    print('Update Done!')
