import os
from opensea import *

key         = os.environ["KEY_OPENSEA"] # https://docs.opensea.io/reference/api-keys
slug        = "faceless-portraits"
out_path    = "./faceless_portraits.csv"

chunk = query_data(slug, key)
chunk = sort_by_qty(chunk)
save_to_file(chunk, out_path)
