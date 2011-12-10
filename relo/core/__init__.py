import config

def init():
    if not config.conf.checkConfig():
        config.conf.createDefaultConfig()
    config.conf.createDefaultConfig()
    config.conf.loadConfig()