import tomllib
import sys


class cached_classproperty(property):
    def __get__(self, _, owner):
        attr = self.fget(owner)
        setattr(owner, self.fget.__name__, attr)
        return attr


def parse_config_file(path: str):
    '''Parse the config file.'''
    with open(path) as f:
        config = tomllib.loads(f.read())

    if not config.get('Feeds'):
        sys.exit('No RSS feeds found in config file.')
    if not config.get('Watchlist'):
        print('No watchlist found in config file.')
    return config
