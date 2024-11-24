def prepare_data(stations):
    unique = []
    for key in stations.keys():
        lst = stations[key]
        unique.extend(lst)
        stations[key] = {
            "forward": lst,
            "backward": lst[::-1],
        }
    stations["unique"] = set(unique)
    return stations


def are_valid_stations(station1, station2, stations):
    return station1 in stations["unique"] and station2 in stations["unique"]


def is_valid_query(query):
    ...


def extract_stations(query):
    return "1", "2"


def compute_query_1(station1, station2):
    return "result"


def compute_query_2(station1, station2):
    return "result"


def compute_query(query_number, station1, station2):
    ...

    if query_number == 1:
        compute_query_1(station1, station2)
    elif query_number == 2:
        compute_query_2(station1, station2)


def process_query(query):
    # possible_queries = [
    #     f'Чи можна потрапити від зупинки <{}> на зупинку <{}>?',
    #     f"Скільки зупинок від зупинки 'Погулянка' до зупинки 'Магнус'?"
    # ]
    if not is_valid_query(query):
        return ""

    station1, station2 = extract_stations(query)

    if not are_valid_stations(station1, station2, stations):
        return ""


if __name__ == '__main__':
    import json
    from pprint import pprint

    with open("stations.json", "r") as f:
        stations = json.load(f)

    pprint(prepare_data(stations))
