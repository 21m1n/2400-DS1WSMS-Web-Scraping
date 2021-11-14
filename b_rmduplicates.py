import pandas as pd
import os

path = os.getcwd()
df = pd.read_csv(path+"/LinkLists1.csv") # read from LinkLists.csv

df.drop_duplicates(inplace=True) # drop the duplicated columns

df['link'].to_csv(path+"/links1.csv", index=False) # write to links.csv

print("Duplicates have been removed.")
