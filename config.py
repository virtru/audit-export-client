try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os.path


class Config:

    def __init__(self, configfile):
        self.config = ConfigParser.ConfigParser()
        self.config.read(configfile)

    def __getattr__(self, name):
        return self.config.get('ApiInfo', name)

    def bookmarkexists(self):
        return os.path.isfile('bookmark.ini')

    def setbookmark(self, value):
        with open('bookmark.ini', 'w') as f:
            f.write(value)

    def getbookmark(self):
        with open('bookmark.ini', 'r') as f:
            bookmark = read_data = f.read()
        return bookmark
