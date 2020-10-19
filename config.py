import configparser

config = configparser.ConfigParser()
config.read('prod.conf')

def model() -> str:
    return config.get('default', 'model')

def mongo_uri() -> str:
    return config.get('mongo', 'uri')