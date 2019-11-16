import json
import pandas as pd

with open('comparison/key1.json') as js1:
    json1 = json.load(fp = js1)

with open('comparison/key2.json') as js2:
    json2 = json.load(fp = js2)

div1_1 = {value: key for key, value in json1.items()}
div1_2 = {value: key for key, value in json2.items()}

new_dict = {}

for i in range(1,164):
    if div1_1[i] != div1_2[i]:
        value = [div1_1[i], div1_2[i]]

    else:
        value = [div1_1[i]]
    new_dict[i] = value

with open('comparison/numeric.json', 'w') as filehandle:
    json.dump(
        obj = new_dict,
        fp = filehandle,
        indent = 4
    )