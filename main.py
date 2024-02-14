import csv
import datetime
from datetime import timedelta
from typing import List, Tuple, Any

START_DATE = datetime.date(2002, 1, 1)


def read_data(file_path: str):
    """Читает данные из файла <file_path> формата csv с разделителем <;>
    file_path - путь до читаемого файла
    """
    ret = []

    with open(file_path, "r") as file:
        wr = csv.DictReader(file, delimiter=';')

        [
            ret.append(
                (
                    int(i['\ufeffstreams']),
                    i["artist_name"],
                    i["track_name"],
                    datetime.date(*map(int, i["date"].split('.')[::-1])))
            ) for i in wr
        ]

    return ret


def count_listenings(name, track, data):
    """Считает кол-во прослушиваний по специальной формуле

    :param name: име артиста
    :param track: название трека
    :param data: дата выпуска трека
    :return: количество прослушиваний
    """
    return abs((START_DATE - data).days) / (len(name) + len(track))


def insertion_sort(a):
    """Сортировка вставками по последнему аргументу многомерно <nxm> массива
    :param a: массив размерами 2xn
    :return: отсортиорванный массив
    """
    for i in range(1, len(a)):
        k = a[i]
        j = i - 1
        while j >= 0 and k[-1] < a[j][-1]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = k
    return a


def get_data(file_path: str):
    """Получает информацию и преобразует её по алгорпитму:
    1. Чтение
    2. Убрать все треки выпущенные после START_DATA
    3. Отсортировать
    :param file_path: путь до файла с данными
    :return:
    """
    data = read_data(file_path)
    data = list(filter(lambda x: x[-1] < START_DATE, data))
    data = insertion_sort(data)
    return data


def write_data(file_path: str, data: List[Tuple[Any, Any, timedelta]]):
    """Запись многомерного массива в файл
    :param file_path: путь до файла
    :param data: данные : <Название песни>, <Артист>, <дата выхода>
    :return:
    """
    with open(file_path, "w") as file:
        file.write(
            '-'.join(("Название песни", "артист", "кол-во прослушиваний"))
        )
        [
            file.write('-'.join(list(map(str, track))) + '\n')
            for track in data
        ]


def convert_data(data) -> List[Tuple[Any, Any, int]]:
    """Добавление количества прослушиваний если они не определены
    :param data:
    :return:
    """
    ret = []
    for song in data:
        if song[0] == 0:
            ret.append((song[2], song[1], int(count_listenings(song[1], song[2], song[3]))))
        else:
            ret.append((song[2], song[1], song[0]))
    return ret


def write(file_path: str, data):
    """Запись многомерного массива в файл
    :param file_path: путь до файла
    :param data: данные : streams;artist_name;track_name;date
    :return:
    """
    with open(file_path , 'w') as file:
        file.write("streams;artist_name;track_name;date")
        file.writelines(
            [
                ';'.join(list(map(str, track))) + '\n' for track in data
            ]
        )


def found_track_by_name(name: str, data):
    """Поиск трека по имени
    :param name: название трека
    :param data: массив поиска
    :return:
    """
    for track in data:
        if track[2] == name:
            return track


def slavic_lang(name):
    """Проверка неа наличие славянских букв в слове
    :param name:
    :return:
    """
    slavic = "йцукенгшщзхъфывапролджэячсмитьббю".lower()
    return any([char.lower() in slavic for char in name])


def get_artists(data):
    """Получение имн артистов из многомерно массива
    :param data:
    :return:
    """
    return [track[1] for track in data]


def ex1_program():
    """Перва программа
    Дата обращения: 12.05.23

    К нам обратилась компания, которая хочет получить все песни по
    дате выхода не позже 01.01.2002. Пока мы не доделали
    весь функционал нашей БД - найдите необходимые песни
    и предоставьте их в виде отчета в формате:
    “<Название песни> - <артист> - <кол-во прослушиваний>”.

    В процессе поиска вы увидели, что не у всех песен есть
     кол-во прослушиваний(те равное нулю), а так сдавать отчет нельзя,
      поэтому перед тем как отдать отчет предоставленный
      выше измените данные в таблице songs.csv
      (https://drive.google.com/file/d/1RFUsY4sX86ikdavcDTj00XdPchEAMzYG/view?usp=drive_link)
      исходя из правила. Кол-во прослушиваний рассчитывается по формуле:
    Измененные данные запишите в таблицу songs_new.csv

    В задаче запрещено использование сторонних библиотек(Pandas и др)
    """
    data = get_data("songs.csv")
    data = convert_data(data)
    write_data("songs_new.csv", data)


def ex2_program():
    """Вторая программа
    Чтобы в дальнейшем нам было удобнее работать
     с данными из нашей таблицы(songs.csv) отсортируйте
     их по столбцу дата в порядке возрастания с помощью
      быстрой сортировки (в задаче нельзя использовать
      встроенные функции сортировок!). Из полученных данных
      выведите топ-5 самых ранних песен. Формат каждой строки:
      “<№> <Название песни>, <Артист>, <дата выхода>”,
      где № - место в рейтинге.

    :return:
    """
    full_data = read_data("songs.csv")
    insertion_sort(full_data)
    write("songs_dump.csv", full_data)


def ex3_program():
    """ Третья программа

    Пришло время сделать наработку для интерфейса, который
    будет взаимодействовать с базой данных. Для этого
    Вам необходимо написать консольную программу, которая
    будет запрашивать у пользователей имя артиста, а на
    выход будет выдавать его одну любую песню, если ничего
    не найдено будет выводить:
     “К сожалению, ничего не удалось найти”.
     Программа должна всегда запрашивать имя.
      Прекратить свою работу она сможет только после ввода “0”.

    Поиск необходимо осуществить с помощью алгоритма с асимптотической сложностью O(n).

    Формат ответа на запрос пользователя: “У <артист> найдена песня: <название песни>”

    Поиск необходимо осуществлять в файле songs.csv

    Не забудьте сделать комментарии к коду согласно стандартам
     документирования кода выбранного языка.
     После выполнения необходимо сделать локальные
     и удаленные изменения Вашего репозитори

    :return:
    """
    data = read_data("songs.csv")
    name = input()
    while name != '0':
        track = found_track_by_name(name, data)
        if track is not None:
            print(f"У {track[1]} найдена песня: {name}")
        name = input()


def ex4_program():
    """4 программа
    Компания хочет провести статистику каких исполнителей
    в базе данных больше - зарубежных или отечественных.
    Для того чтобы решить это задание, создайте два списка
    - один должен содержать имена исполнителей на русском
    языке (russian_artists), второй - на остальных (foreign_artists).
     Имена исполнителей относятся к исполнителям на русском языке в случае,
      если в названии исполнителя есть хотя бы одна русская буква.
       Выведите информацию о количестве элементов в каждом
       из созданных списков в следующем формате:

    Количество российских исполнителей: {длина списка russian_artists}
    (https://drive.google.com/file/d/1wK_FbEUID_5Y_tHWNveiqhc7butER22Z/view?usp=drive_link)

    Количество иностранных исполнителей: {длина списка foreign_artists}
    (https://drive.google.com/file/d/12p4X5JYqaA5rloR4u9mXP0Hl6_CyNAJD/view?usp=drive_link)

    Обратите внимание, что каждый из исполнителей должен встречаться
     в списке только ОДИН раз.

    Запишите содержимое списков в файлы russian_artists.txt и
     foreign_artists.txt соответственно.

    Не забудьте сделать комментарии к коду согласно стандартам
    документирования кода выбранного языка. После выполнения
    необходимо сделать локальные и удаленные изменения Вашего репозитория


    :return:
    """
    data = read_data("songs.csv")
    data = get_artists(data)
    data = set(data)
    ru_artists = list(filter(slavic_lang, data))
    print(f'Количество российских исполнителей: {len(ru_artists)}')
    print(f'Количество иностранных исполнителей: {len(data) - len(ru_artists)}')


def count_artist_tracks(data):
    """Посчитать количество треков которые исполнел тоот или иной исполнитель
    :param data: многомерный массив
    :return: dict[str, int]
    """
    ret = {}
    track_was = []
    for track in data:
        if track[2] not in track_was:
            ret[track[1]] = ret.get(track[1], 0) + 1
            track_was.append(track[2])
    return ret

def ex5_program():
    """5 program
    Компании нужно понять, какой исполнитель в
    базе данных является наиболее популярным.
     Для решения этой задачи реализуйте хэш-таблицу,
      в которой ключом будет являться имя исполнителя,
      а значением количество его песен в базе данных.
      В случае, если один и тот же трек исполняется несколькими артистами,
       необходимо посчитать этот трек для того артиста, который указан первым.
       Выведите первые 10 артистов из полученной таблицы в формате

    <Название исполнителя> выпустил <количество песен> песен.

    Не забудьте сделать комментарии к
    коду согласно стандартам документирования кода выбранного языка.
    После выполнения необходимо сделать локальные
     и удаленные изменения Вашего репозитория
    :return:
    """
    data = read_data("songs.csv")
    artist_count = count_artist_tracks(data)
    best = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for art in best:
        print(f"{art[0]} выпустил {art[1]} песен.")


def main():
    ex1_program()