from src.data_type import Track
from src.utils import START_DATE


def count_listenings(track: Track) -> int:  # INFO: works
    return int(
        abs((START_DATE - track.release_date).days)
        / (len(track.track_name) + len(track.artist_name))
    )


def convert_data(data: list[Track]) -> list[Track]:  # INFO: works
    ret = []
    for track in data:
        if track.streams == 0:
            track.streams = count_listenings(track)
        ret.append(track)
    return ret


def data_circumcision(data: list[Track], fieldnames: list[str]) -> list[dict]:
    circumcision = list(map(lambda x: x.__dict__, data))
    return [{key: track[key] for key in fieldnames} for track in circumcision]
