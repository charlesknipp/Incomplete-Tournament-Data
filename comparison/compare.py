from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import html5lib
import json
import re


# pd.set_option('display.max_rows', 1000)

for szn in range(2011, 2018):

    path1 = 'comparison/fernando/CFB%dc.xlsx' % szn

    df_f = pd.read_excel(
        io = path1,
        header = 0,
        usecols = ['W', 'W Pts', 'L', 'L Pts']
    )

    if szn < 2014:
        path2 = 'clean data/%d.csv' % szn

        df_c = pd.read_csv(
            filepath_or_buffer = path2,
            usecols = ['W', 'W Pts', 'L', 'L Pts', 'Hash']
        )

        df_hash = df_c['Hash'].tolist()

    else:
        path3 = 'comparison/sports reference/numbered/%d.csv' % szn
        df_sr = pd.read_csv(
            filepath_or_buffer = path3,
            usecols = ['W', 'W Pts', 'L', 'L Pts', 'Hash']
        )

        df_hash = df_sr['Hash'].tolist()

    # df_c_hash = df_c['Hash'].tolist()
    df_f_hash = []
    # df_sr_hash = df_sr['Hash'].tolist()

    for i, d in df_f.iterrows():
            df_f_hash.append(
                1000000000 * d['W'] +
                1000000 * d['W Pts'] +
                1000 * d['L'] +
                d['L Pts']
            )

    missing = []

    for h in df_f_hash:
        if h not in df_hash:
            missing.append(h)

    for j in df_hash:
        if j not in df_f_hash:
            missing.append(j)

    print('\n', szn, '\n')

    for i in sorted(missing):
        value = '%0*d' % (12,i)
        print(
            value[0:3], ' - ',
            value[3:6], ' - ',
            value[6:9], ' - ',
            value[9:]
        )
    
