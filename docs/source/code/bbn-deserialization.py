import json

from pybbn.lg.graph import Bbn

# deserialize from JSON file
with open('simple-bbn.json', 'r') as f:
    d = json.loads(f.read())
    bbn = Bbn.from_dict(d)
