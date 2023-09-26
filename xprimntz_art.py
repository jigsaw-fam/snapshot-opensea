import os
from opensea import *

key         = os.environ["KEY_OPENSEA"]
slug        = "xprimntz-art"
out_path    = "./out/xprimntz_art.csv"

chunk = query_data(slug, key)
save_to_file(chunk, out_path, True)
