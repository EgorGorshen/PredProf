import datetime
from dataclasses import dataclass


@dataclass
class Track:
    streams: int
    artist_name: str
    track_name: str
    release_date: datetime.date
