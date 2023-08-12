import os, time
import requests
from pprint import pprint as pp

slug        = "faceless-portraits"
chain       = "ethereum" # https://docs.opensea.io/reference/supported-chains
limit       = 50 # max api limit
next_page   = ""
key         = os.environ["KEY_OPENSEA"] # https://docs.opensea.io/reference/api-keys
headers     = {
    "accept": "application/json",
    "X-API-KEY": key,
}

API_COLLECTION = "https://api.opensea.io/v2/collection/{}/nfts?limit={}&next={}"
API_NFT_INFO   = "https://api.opensea.io/v2/chain/{}/contract/{}/nfts/{}"

while (next_page is not None):
    a1 = API_COLLECTION.format(slug, limit, next_page)
    r1 = requests.get(a1, headers=headers)
    d1 = r1.json()
    time.sleep(1) # api cooldown

    nfts = d1["nfts"]
    next_page = d1.get("next")

    for nft in nfts:
        a2 = API_NFT_INFO.format(chain, nft["contract"], nft["identifier"])
        r2 = requests.get(a2, headers=headers)
        d2 = r2.json()["nft"]
        time.sleep(1) # api cooldown

        print(d2["name"])
        print(d2["owners"])
