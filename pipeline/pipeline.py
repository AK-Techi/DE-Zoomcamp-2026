import sys
print("print", sys.argv)

month = sys.argv[1]
print(f"the month passed in argument is taken from first place {month}")

#######################

import pandas as pd 

df= pd.DataFrame({"X": [2,3,4], "Y": [5,6,7]})
print (df.head())

df.to_parquet(f"output_{month}.parquet")