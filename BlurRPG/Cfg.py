import configparser
import json

class Cfg(object):
    config_loader = None
    path = 'config.ini'

    initialized = False

    @classmethod
    def initialize(cls):
        if not cls.config_loader:
            cls.config_loader = configparser.ConfigParser()
            cls.config_loader.read(cls.path)
            cls.initialized = True

    @classmethod
    def get(cls, key):
        if not cls.initialized:
            cls.initialize()

        if not ('CONFIG' in cls.config_loader) or not (key in cls.config_loader['CONFIG']):
            return None

        return cls.config_loader['CONFIG'][key]

    @classmethod
    def getLines(cls, key):
        if not cls.initialized:
            cls.initialize()

        return cls.config_loader.get('CONFIG', key).split("\n")