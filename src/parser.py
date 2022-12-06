from dataclasses import dataclass
from dataclasses_json import dataclass_json

from functools import cached_property
from utils import cached_classproperty
from urllib.parse import urlencode

import anitopy


@dataclass_json
@dataclass
class ParsedEntry:
    video_resolution: str = '0p'
    subtitles: str = 'ENG'
    language: str = ''
    episode_number: str = ''
    anime_title: str = 'No title found'
    release_group: str = 'Anonymous'
    anime_season: str = ''
    anime_type: str = ''
    source: str = ''
    anime_year: str = ''

    @cached_property
    def short(self):
        ep = f'E{e}' if (e := self.episode_number) else ''
        if isinstance(e, list):
            ep = f"E{'-'.join(e)}"
        se = f'S{s}' if (s := self.anime_season) else ''
        if isinstance(s, list):
            se = f"E{'-'.join(s)}"
        return f'{se}{ep}'


@dataclass_json
@dataclass
class Entry:
    title: str
    link: str
    published: str
    nyaa_seeders: str
    nyaa_leechers: str
    nyaa_downloads: str
    nyaa_infohash: str
    nyaa_size: str

    @cached_property
    def magnet(self):
        param_str = urlencode({'tr': Entry.trackers}, doseq=True)
        return f'magnet:?xt=urn:btih:{self.nyaa_infohash}&' + param_str

    @cached_property
    def parsed(self):
        return ParsedEntry.from_dict(anitopy.parse(self.title), infer_missing=True)

    @cached_classproperty
    def trackers(cls):
        with open('static/trackers.txt') as f:
            return f.read().splitlines()
