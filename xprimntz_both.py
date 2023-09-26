import os
from opensea import *

key         = os.environ["KEY_OPENSEA"]
slugs       = [ "xprimntz-art", "xprimntz-chronicle" ]
out_path    = "./out/xprimntz_both.csv"

chunk = {}
for slug in slugs:
    chunk = query_data(slug, key, chunk)
save_to_file(chunk, out_path, True)
