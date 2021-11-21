import pandas as pd
from autoplotter import run_app
from autoplotter import app
import sys

host = '127.0.0.1'

port = 5100  # default setting

# port = sys.argv[2]

csv = pd.read_csv(fr'E:\MIT\Nilofer-project\Flask\{sys.argv[1]}')
print(sys.argv[1])

run_app(csv, 'external', host, port)
