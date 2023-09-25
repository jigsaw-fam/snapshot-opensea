import os, time
import requests

slug        = "xprimntz-chronicle"
chain       = "ethereum" # https://docs.opensea.io/reference/supported-chains
limit       = 50 # max api limit
next_page   = ""
key         = os.environ["KEY_OPENSEA"] # https://docs.opensea.io/reference/api-keys
headers     = {
    "accept": "application/json",
    "X-API-KEY": key,
}
out_path    = "./xprimntz_chronicle.csv"

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
        print("⚠️")
        time.sleep(1)
        return req(url, check_key)

# init chunk for collect data
chunk = {}

# fetch every pages
while (next_page is not None):
    a1 = API_COLLECTION.format(slug, limit, next_page)
    d1 = req(a1, "nfts")
    nfts = d1["nfts"]
    next_page = d1.get("next")

    # fetch owners for each NFT
    for nft in nfts:
        a2 = API_NFT_INFO.format(chain, nft["contract"], nft["identifier"])
        d2 = req(a2, "nft")["nft"]

        print(d2["name"])
        for owner in d2.get("owners", []):
            addr = owner["address"]
            qty = owner["quantity"]
            print(" * {} -> {}".format(addr, qty))

            # collect data
            cur_qty = chunk.get(addr, 0)
            chunk[addr] = cur_qty + qty

# shape chunk to sorted list
chunk = sorted(list(chunk.items()), key=lambda x: x[1], reverse=True)

# write to file
# https://docs.manifold.xyz/v/manifold-studio/references/audiences#manually-via-csv
out = "address,value\n"
out += "\n".join([ ",".join([ r[0], str(r[1]) ]) for r in chunk ])
with open(out_path, "w") as f:
    f.write(out)
