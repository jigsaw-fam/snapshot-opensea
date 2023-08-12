import os
import requests

slug        = "faceless-portraits"
chain       = "ethereum" # https://docs.opensea.io/reference/supported-chains
limit       = 50 # max api limit
next_page   = ""
key         = os.environ["KEY_OPENSEA"] # https://docs.opensea.io/reference/api-keys
headers     = {
    "accept": "application/json",
    "X-API-KEY": key,
}

# https://docs.opensea.io/reference/api-overview
API_COLLECTION = "https://api.opensea.io/v2/collection/{}/nfts?limit={}&next={}"
API_NFT_INFO   = "https://api.opensea.io/v2/chain/{}/contract/{}/nfts/{}"

def req(url, check_key):
    resp = requests.get(url, headers=headers)
    data = resp.json()
    try:
        data[check_key]
        return data
    except:
        print(".")
        return req(url, check_key)

while (next_page is not None):
    a1 = API_COLLECTION.format(slug, limit, next_page)
    d1 = req(a1, "nfts")
    nfts = d1["nfts"]
    next_page = d1.get("next")

    for nft in nfts:
        a2 = API_NFT_INFO.format(chain, nft["contract"], nft["identifier"])
        d2 = req(a2, "nft")["nft"]

        print(d2["name"])
        for owner in d2.get("owners", []):
            print(" * {} -> {}".format(owner["address"], owner["quantity"]))
