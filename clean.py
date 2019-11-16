import pandas as pd
from tqdm import tqdm
import numpy as np
import json


pd.set_option('display.max_columns', None)

# import the json containing a time variant dictionary of all div 1A teams

with open('div1A.json') as js1:
    div1_json = json.load(js1)

with open('numeric.json') as js2:
    num_json = json.load(js2)


# since the data is sliced into bowl games and not, I have to merge the sets

def merge(szn,simple):
    
    if szn < 2009:
        path = 'raw data/ncaa%dlines.csv' % szn

    else:
        path = 'raw data/cfb%dlines.csv' % szn
    
    columns = [
        'Date', 'Visitor', 'Visitor Score', 'Home Team', 'Home Score', 'Line'
    ]

    df_reg = pd.read_csv(
        filepath_or_buffer = path,
        usecols = columns,
        na_values = ['  ',' ',''],
        keep_default_na = True
    )

    path_bowl = 'raw data/bowl%dlines.csv' % szn

    df_bowl = pd.read_csv(
        filepath_or_buffer = path_bowl,
        usecols = columns,
        na_values = [' ',''],
        keep_default_na = True
    )

    df = pd.concat([df_reg, df_bowl], ignore_index = True)

    # sort through only div 1A teams to make the winner/loser function a bit
    # easier to handle

    div1 = div1_json.get(str(szn))
    
    df = df.loc[
        (df['Visitor'].isin(div1)) & (df['Home Team'].isin(div1))
    ].reset_index(drop = True)

    date = []
    win = []
    win_score = []
    loss = []
    loss_score = []
    line = []


    for i, rows in df.iterrows():

        date.append(rows['Date'])

        # must iterate for both home and visitors to obtain the win matrix

        if rows['Visitor Score'] > rows['Home Score']:
            win.append(rows['Visitor'])
            loss.append(rows['Home Team'])

            win_score.append(rows['Visitor Score'])
            loss_score.append(rows['Home Score'])

            line.append(df['Line'][i])

        else:
            win.append(rows['Home Team'])
            loss.append(rows['Visitor'])

            win_score.append(rows['Home Score'])
            loss_score.append(rows['Visitor Score'])

            line.append(-1 * df['Line'][i])

    df['Date'] = date
    df['Visitor'] = win
    df['Home Team'] = loss
    df['Visitor Score'] = win_score
    df['Home Score'] = loss_score
    df['Line'] = line

    # rename the columns to match the simulation code just to make it easier
    # in the long run

    df = df.rename(
        columns = {
            'Visitor': 'W',
            'Home Team': 'L',
            'Visitor Score': 'W Pts',
            'Home Score': 'L Pts'
        }
    )

    # now I want to convert my teams to a numeric format for the simulation in
    # addition to assigning a hash to each unique game; this was on a separate
    # function, but it didn't work so...


    if simple == 'n':
        
        df['W'].replace(num_json, inplace = True)
        df['L'].replace(num_json, inplace = True)
        df['W'] = pd.to_numeric(df['W'])
        df['L'] = pd.to_numeric(df['L'])

        df_hash = []

        for i, d in df.iterrows():
            df_hash.append(
                1000000000 * d['W'] +
                1000000 * d['W Pts'] +
                1000 * d['L'] +
                d['L Pts']
            )
        
        df['Date'] = df_hash
        df['Date'] = df['Date'].astype('int64')

        df = df.rename(
            columns = {
                'Date': 'Hash'
            }
        )

    return df


for szn in range(1978, 2014):

    df = merge(szn, 'n')
    print(szn, df.dtypes)
    
    path = 'clean data/%d.csv' % szn
    
    df.to_csv(
        path_or_buf = path
    )