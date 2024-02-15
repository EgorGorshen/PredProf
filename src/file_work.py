import csv
import datetime

from src.data_converter import data_circumcision
from src.data_type import Track


def read_data(file_path: str, delimiter=";") -> list[Track]:  # INFO: works
    ret = []

    with open(file_path, "r") as file:
        wr = csv.DictReader(file, delimiter=delimiter)
        [
            ret.append(
                Track(
                    streams=int(i["\ufeffstreams"]),
                    artist_name=i["artist_name"],
                    track_name=i["track_name"],
                    release_date=datetime.date(
                        *map(int, i["date"].split(".")[::-1])
                    ),  # TODO: read with datatime module
                )
            )
            for i in wr
        ]

    return ret


def write_data(  # INFO: works
    file_path: str,
    data: list[Track],
    fieldnames: list[str] = list(Track.__dataclass_fields__.keys()),
    delimiter=";",
) -> None:
    writing_data = data_circumcision(data, fieldnames)

    with open(file_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(writing_data)
