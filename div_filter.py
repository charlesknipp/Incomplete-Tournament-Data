import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import html5lib
import json


# dictionary to translate observations between data sets
div1_dict = {}

with open('comparison/key1.json') as js:
    key1_r = json.load(js)

with open('comparison/key2.json') as js:
    key2_r = json.load(js)

# sports reference is key 2 
key1 = {v: k for k, v in key1_r.items()}
key2 = {v: k for k, v in key2_r.items()}
key = {}

for i in range(1,164):
    key[key2[i]] = key1[i]

# iterate seasonally to extract all div 1A teams from sports reference
for szn in tqdm(range(1978, 2018)):

    url = 'https://www.sports-reference.com/cfb/years/%d-standings.html' % szn

    data = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})

    # this is where BeautifulSoup comes into play, only once this time
    soup = BeautifulSoup(data.content, 'html5lib')
    teams = soup.find('table', id='standings')
    tbody = teams.find('tbody')
    rows = tbody.find_all('tr')

    div1 = []
    div1_teams = []

    # div 1A teams are identified by the 'school_name' attribute
    for row in rows:
        cols = row.find_all('td', attrs={'data-stat':'school_name'})
        cols = [ele.text.strip() for ele in cols]
        div1.append(cols)

    head = ['school']

    df = pd.DataFrame(div1, columns=head)
    df = df.mask(df.eq('None')).dropna().reset_index(drop=True)

    # get list of div 1A teams and convert to new naming convention using key
    var = [key.get(item,item) for item in list(df['school'])]
    div1_teams.extend(var)
    div1_dict[szn] = sorted([x for i, x in enumerate(div1_teams) if i == div1_teams.index(x)])


with open('div1A2.json', 'w') as filehandle:
    json.dump(div1_dict, filehandle, indent=4)