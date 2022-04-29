from distutils.log import error
import pandas as pd
import numpy as np
import os
cwd = os.getcwd()

df_name = ''

column_list =[]

def mkdf(df_name,column_list):
  keys = column_list
  values = np.zeros(len(column_list))
  values[:] = np.nan
  dictionary = dict(zip(keys, values))
  df = pd.DataFrame(dictionary, index=[0])
  df.to_csv(f'{df_name}_start.csv',index=False)

  print(f'''
  successfully created df in your current directory. \n
  {cwd}
  ''')

mkdf(df_name, column_list)