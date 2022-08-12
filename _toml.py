import toml
from pprint import pprint
with open('config.toml','r') as f:
    parsed_toml = toml.loads(f.read())
    print(parsed_toml['foo'])