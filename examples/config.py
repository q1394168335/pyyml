from pyyml import load

with open('conf.yml') as f:
    raw_conf = f.read()
config = load(raw_conf)
print(config)
