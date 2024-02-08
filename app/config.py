import tomllib
def load():
    with open("config.toml", "rb") as f:
        return tomllib.load(f)

config = load()
