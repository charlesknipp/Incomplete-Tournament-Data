import pandas as pd
import json


pd.set_option('display.max_rows', None)

with open('sr.json') as js1:
    div1_json = json.load(js1)

with open('comparison/key2.json') as js2:
    num_json = json.load(js2)


for szn in range(2014, 2018):
    div1A = div1_json.get(str(szn))

    path = 'comparison/sports reference/sr%d.csv' % szn

    df = pd.read_csv(
        filepath_or_buffer = path,
        usecols = [
            'W','W Pts','L','L Pts'
        ]
    )

    df = df.loc[
            (df['W'].isin(div1A)) & (df['L'].isin(div1A))
        ].reset_index(drop = True)

    df['W'].replace(num_json, inplace = True)
    df['L'].replace(num_json, inplace = True)

    df_hash = []
    
    for i, d in df.iterrows():
            df_hash.append(
                1000000000 * d['W'] +
                1000000 * d['W Pts'] +
                1000 * d['L'] +
                d['L Pts']
            )
    
    df['Hash'] = df_hash
    path = 'comparison/sports reference/numbered/%d.csv' % szn

    df.to_csv(
        path_or_buf = path
    )
    