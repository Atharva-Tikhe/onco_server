import pandas as pd
from autoplotter import run_app
from autoplotter import app
import sys

host = '0.0.0.0'

port = 8081  # default setting

# port = sys.argv[2]

csv = pd.read_csv(fr'{sys.argv[1]}')
print(sys.argv[1])

run_app(csv, 'external', host, port)
