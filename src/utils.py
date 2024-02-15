from datetime import date

from src.data_type import Track

START_DATE = date(2002, 1, 1)


def found_track_by_name(name: str, data: list[Track]) -> Track | None:  # INFO: works
    for track in data:
        if track.track_name == name:
            return track


def slavic_lang(name: str) -> bool:
    slavic = "йцукенгшщзхъфывапролджэячсмитьбю".lower()
    return any([char.lower() in slavic for char in name])


def count_artist_tracks(data: list[Track]) -> dict[str, int]:
    ret = {}
    track_was = []
    for track in data:
        if track.track_name not in track_was:
            ret[track.artist_name] = ret.get(track.artist_name, 0) + 1
            track_was.append(track.track_name)
    return ret


def insertion_sort(a: list[Track]) -> list[Track]:  # INFO: works
    for i in range(1, len(a)):
        k = a[i]
        j = i - 1
        while j >= 0 and k.release_date < a[j].release_date:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = k
    return a
