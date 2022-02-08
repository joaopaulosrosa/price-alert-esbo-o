from django.conf import settings
import requests
import json

def update_assets():
    url = 'https://api-cotacao-b3.labdo.it/api/cotacao/dt/20200102/02'
    request = requests.get(url).json()

    for asset in request:
        print(f'Asset {asset["cd_acao"]}')
