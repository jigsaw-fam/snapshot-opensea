import os
from opensea import *

key         = os.environ["KEY_OPENSEA"]
slug        = "faceless-portraits"
out_path    = "./out/faceless_portraits.csv"

chunk = query_data(slug, key)
save_to_file(chunk, out_path)
