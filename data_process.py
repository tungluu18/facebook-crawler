import sys
import os
import pandas as pd

filename = sys.argv[1]
filepath = os.path.join(os.getcwd(), filename)


df = pd.read_csv(filepath)
df.drop_duplicates(subset=['profile_url'], keep='last', inplace=True)
df.to_csv('_{}'.format(filename))