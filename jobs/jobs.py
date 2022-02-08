from django.conf import settings
import requests
import json
from base.models import Asset


def update_assets():
    url = 'https://api-cotacao-b3.labdo.it/api/cotacao/dt/20200102/02'
    request = requests.get(url).json()
    assets = Asset.objects.all()
    # asset = Asset.objects.get(ticker="GPIV33")

    for a in request:
        if assets.filter(ticker=a["cd_acao"]) is None:
            a = Asset(ticker=str(a["cd_acao"]))
            if a:
                a.save()
            print("Asset Created!")
        #      if assets.filter(ticker=a['cd_acao']) is None:
        #     print('fuck')
        # else:
        #     print('hell yeah')
    print('Update Done')
