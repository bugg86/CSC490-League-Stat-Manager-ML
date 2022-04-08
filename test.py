import json

with open('item.json') as f:
    summoners = json.load(f)
f.close()

for item in summoners :
    item['key'] = int(item['key'])

with open('item.json', 'w') as f:
    json.dump(summoners, f)
f.close()