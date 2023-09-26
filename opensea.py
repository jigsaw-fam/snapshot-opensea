import time
import requests

# https://docs.opensea.io/reference/api-overview
API_COLLECTION = "https://api.opensea.io/v2/collection/{}/nfts?limit={}&next={}"
API_NFT_INFO   = "https://api.opensea.io/v2/chain/{}/contract/{}/nfts/{}"

# request: retry if data not complete
# https://docs.opensea.io/reference/api-keys
def req(url, key, check_key):
    headers = { "accept": "application/json", "X-API-KEY": key }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    try:
        data[check_key]
        return data
    except:
        print("⚠️")
        time.sleep(1)
        return req(url, key, check_key)

# chain -- https://docs.opensea.io/reference/supported-chains
# limit -- 50 = max api limit
def query_data(slug, key, chunk={}, chain="ethereum", limit=50):
    next_page = ""

    # fetch every pages
    while (next_page is not None):
        a1 = API_COLLECTION.format(slug, limit, next_page)
        d1 = req(a1, key, "nfts")
        nfts = d1["nfts"]
        next_page = d1.get("next")

        # fetch owners for each NFT
        for nft in nfts:
            a2 = API_NFT_INFO.format(chain, nft["contract"], nft["identifier"])
            d2 = req(a2, key, "nft")["nft"]

            print(d2["name"])
            for owner in d2.get("owners", []):
                addr = owner["address"]
                qty = owner["quantity"]
                print(" * {} -> {}".format(addr, qty))

                # collect data
                cur_qty = chunk.get(addr, 0)
                chunk[addr] = cur_qty + qty
    return chunk

def save_to_file(chunk, out_path, header=False):
    # shape chunk to sorted list
    chunk = sorted(list(chunk.items()), key=lambda x: x[1], reverse=True)
    # manifold header
    out = "address,value\n" if header else ""
    out += "\n".join([ ",".join([ r[0], str(r[1]) ]) for r in chunk ])
    with open(out_path, "w") as f:
        f.write(out)
