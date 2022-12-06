from typing import Optional
from utils import parse_config_file
import sys
import feedparser
from urllib.parse import urlencode


from parser import Entry


CONFIG_FILE = '../config.toml'
DEFAULT_TRACKERS = 'trackers.txt'


def parse_rss_feeds(feeds, params: Optional[dict[str, str]] = None) -> list[Entry]:
    '''Parse RSS feeds from the config file.'''
    params_str = '&' + urlencode(params) if params else ''
    entries = []
    for rss_label, rss_feed in feeds.items():
        print(f'Getting {rss_label} feed...')
        feed = feedparser.parse(rss_feed + params_str)
        print(rss_feed + params_str)
        entries.extend([Entry.from_dict(e) for e in feed.entries])
    return entries


def main() -> None:
    config = parse_config_file(CONFIG_FILE)
    rss_feeds: dict[str, str] = config.get('Feeds', {})

    while True:
        params = {}
        params['q'] = input('Search for an anime: ').strip()
        entries = parse_rss_feeds(rss_feeds, params)
        if len(entries) == 0:
            sys.exit('No entries found in RSS feeds.')

        results = sorted(entries, key=lambda e: int(e.nyaa_seeders), reverse=True)
        for e in results[:20]:
            p = e.parsed
            if isinstance(p.episode_number, list):
                p.episode_number = '-'.join(map(str, p.episode_number))
            print(
                ' - '.join(
                    [e.nyaa_seeders, p.release_group, p.anime_title, p.short, e.nyaa_size, e.link]
                )
            )


if __name__ == '__main__':
    main()
