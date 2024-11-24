# Отримує дані про трамвайні зупинки та створює словник з трамвайними маршрутами та зупинками
def get_tram_data_and_stops_dict():
    tram_data = tram_stops_info()
    tram_stops_dict = get_routes_dict(tram_data)
    return (tram_data, tram_stops_dict)

# Створює словник маршрутів для кожної зупинки, який містить інформацію про сусідні зупинки, до яких можна дістатися
def get_routes_dict(tram_data):
    routes_dict = routes_direction(tram_data)
    tram_stops_dict = dict()
    for stop in routes_dict.keys():
        tram_stops_dict[stop] = dict()
    for stop in routes_dict.keys():
        for next_stop in routes_dict.keys():
            if stop == next_stop:
                continue
            tram_stops_dict[stop][next_stop] = get_tram_route(tram_data, routes_dict, stop, next_stop)
    return tram_stops_dict

# Зчитує дані з файлу і створює словник, який містить інформацію про трамвайні маршрути та їх зупинки
def tram_stops_info():
    tram_data = dict()
    try:
        with open("stations.txt", encoding="utf-8") as file:
            tram = 0
            is_route = False
            while True:
                line = file.readline()
                if line == "":
                    break
                line = line.strip("\n")
                if tram == 0:
                    tram = int(line)
                    tram_data[tram] = {"start": [],"end": [],"stops": {}}
                else:
                    if line == "--------------------------------------------------":
                        tram_data[tram]["end"] = tram_data[tram]["start"].copy()
                        tram_data[tram]["end"].reverse()
                        tram_data[tram]["stops"] = set(tram_data[tram]["start"])
                        tram = 0
                    else:
                        tram_data[tram]["start"].append(line)
    except FileNotFoundError:
        print("File not found!")
        exit()
    return tram_data

# Створює словник маршрутів для кожної зупинки, визначаючи сусідні зупинки для кожного маршруту
def routes_direction(tram_data):
    stop_set = set()
    for tram in tram_data:
        stop_set = stop_set.union(tram_data[tram]["stops"])
    routes_dict = dict()
    for stop in stop_set:
        routes_dict[stop] = list()
    for stop in stop_set:
        for tram in tram_data:
            if stop in tram_data[tram]["stops"]:
                idx = tram_data[tram]["start"].index(stop)
                if idx == 0:
                    routes_dict[stop].append({tram_data[tram]["start"][1]})
                elif idx == len(tram_data[tram]["start"]) - 1:
                    routes_dict[stop].append({tram_data[tram]["start"][-2]})
                else:
                    routes_dict[stop].append({tram_data[tram]["start"][idx - 1], tram_data[tram]["start"][idx + 1]})
        routes_dict[stop] = list(set.union(*routes_dict[stop]).difference({stop}))
    return routes_dict

# Знаходить шлях між двома зупинками в словнику маршрутів
def get_path(routes_dict, start_stop, end_stop, path=[]):
    path = path + [start_stop]
    if start_stop == end_stop:
        return path
    if not start_stop in routes_dict:
        return None
    for fn in routes_dict[start_stop]:
        if fn not in path:
            new_path = get_path(routes_dict, fn, end_stop, path)
            if new_path: return new_path
    return None

# Знаходить шлях між двома зупинками з можливістю пересадки на інші маршрути
def get_path_with_changes(routes_dict, start_stop, end_stop, path=[]):
    path = path + [start_stop]
    if start_stop == end_stop:
        return path
    if not start_stop in routes_dict:
        return None
    shortest = None
    for fn in routes_dict[start_stop]:
        if fn not in path:
            new_path = get_path_with_changes(routes_dict, fn, end_stop, path)
            if new_path:
                if not shortest or len(new_path) < len(shortest):
                    shortest = new_path
    return shortest

# Визначає маршрут трамвая без пересадок між двома зупинками
def get_tram_route_without_change(tram_data, tram, start_stop, end_stop):
    try:
        number_of_stops = tram_data[tram]["start"].index(end_stop) - tram_data[tram]["start"].index(start_stop)
        if number_of_stops > 0:
            direction_info = {"from": tram_data[tram]["start"][0], "to": tram_data[tram]["start"][-1]}
        else:
            direction_info = {"from": tram_data[tram]["end"][0], "to": tram_data[tram]["end"][-1]}
        number_of_stops = abs(number_of_stops)
    except ValueError:
        number_of_stops = tram_data[tram]["end"].index(end_stop) - tram_data[tram]["end"].index(start_stop)
        direction_info = { "from": tram_data[tram]["end"][0], "to": tram_data[tram]["end"][-1]}

    return {"tram": tram, "stops": number_of_stops, "direction": direction_info}

# Знаходить можливі маршрути трамвая між двома зупинками з урахуванням можливості пересадки
def get_tram_routes(tram_data, path):
    tram_data_copy = tram_data.copy()
    idx = 0
    tram_routes = list()
    if path is None:
        return {}
    for i in range(len(path)):
        keys_to_delete = list()
        for key in tram_data_copy.keys():
            _set = set(path[idx:i + 1])
            if not _set.intersection(tram_data_copy[key]["stops"]) == _set:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            tram_data_copy.pop(key)
        if i == len(path) - 1 and len(tram_data_copy) == 0:
            start_stop = path[idx]
            end_stop = path[i - 1]
            for tram in tram_data:
                if tram_data[tram]["stops"].intersection({start_stop, end_stop}) == {start_stop, end_stop}:
                    tram_routes.append(get_tram_route_without_change(tram_data, tram, start_stop, end_stop))
                    break
            start_stop = path[i - 1]
            end_stop = path[i]
            for tram in tram_data:
                if tram_data[tram]["stops"].intersection({start_stop, end_stop}) == {start_stop, end_stop}:
                    tram_routes.append(get_tram_route_without_change(tram_data, tram, start_stop, end_stop))
                    break
            break
        if i == len(path) - 1:
            start_stop = path[idx]
            end_stop = path[i]
            for tram in tram_data:
                if tram_data[tram]["stops"].intersection({start_stop, end_stop}) == {start_stop, end_stop}:
                    tram_routes.append(get_tram_route_without_change(tram_data, tram, start_stop, end_stop))
                    break
            break
        if len(tram_data_copy) == 0:
            start_stop = path[idx]
            end_stop = path[i - 1]
            for tram in tram_data:
                if tram_data[tram]["stops"].intersection({start_stop, end_stop}) == {start_stop, end_stop}:
                    tram_routes.append(get_tram_route_without_change(tram_data, tram, start_stop, end_stop))
                    break
            idx = i - 1
            tram_data_copy = tram_data.copy()
    return tram_routes

# Знаходить маршрути трамвая з можливістю пересадки між двома зупинками
def get_tram_routes_with_change(tram_data, routes_dict, start_stop, end_stop):
    path = get_path_with_changes(routes_dict, start_stop, end_stop)
    return get_tram_routes(tram_data, path)

# Знаходить маршрут трамвая між двома зупинками, враховуючи можливість пересадки
def get_tram_route(tram_data, routes_dict, start_stop, end_stop):
    tram_routes = list()
    for tram in tram_data:
        if tram_data[tram]["stops"].intersection({start_stop, end_stop}) == {start_stop, end_stop}:
            tram_routes.append(get_tram_route_without_change(tram_data, tram, start_stop, end_stop))
    if len(tram_routes) > 0:
        return {"withTramChange": False, "routes": routes_dict}
    return {"withTramChange": True, "routes": get_tram_routes_with_change(tram_data, routes_dict, start_stop, end_stop)}

# Виводить на екран меню опцій для користувача
def tram_options():
    print("🧩 Available options:")
    print('\t1: Which trams have a route through the stops <name_of_stop> and <name_of_stop>?')
    print('\t2: How many stops from the stop <name_of_stop> to the stop <name_of_stop>?')
    print('\t3: Is it possible to get from the stop <name_of_stop> to the stop <name_of_stop>?')
    print('\t4: Which trams can get to the stop <name_of_stop>?')
    print('\t5: How to get from stop <name_of_stop> to stop <name_of_stop>?')

# Визначає трамвай, який має маршрут через задані зупинки, вводьте назви зупинок, для завершення введіть 0
def option1(tram_data, tram_stops_routes_dict):
    print("\tWhich trams have a route through the stops?")
    stations = []
    while True:
        station = input('\tInput stop name(0 to finish): ')
        if station == "0":
            break
        else:
            stations.append(station)
    stations = set(stations)
    trams_numbers = []
    for tram in tram_data:
        if all(x in tram_data[tram]["stops"] for x in stations):
            trams_numbers.append(str(tram))
    if trams_numbers:
        print("\t✅ It`s tram: ", ", ".join(trams_numbers))
    else:
        print("\t❌ Does`t have such a route")



# Визначає кількість зупинок між двома заданими зупинками
def option2(tram_data, tram_stops_routes_dict):
    print("\tHow many stops from the stop <name_of_stop> to the stop <name_of_stop>?")
    first_pos = str(input('\tInput start station: '))
    last_pos = str(input('\tInput the destination station: '))
    print("\tAnswer: ", end="")
    if tram_stops_routes_dict[first_pos][last_pos]["withTramChange"]:
        number_of_stations = sum([route["stops"] for route in tram_stops_routes_dict[first_pos][last_pos]["routes"]])
        print(f'{number_of_stations} stops with change')
    else:
        print(f'{tram_stops_routes_dict[first_pos][last_pos]["routes"][0]["stops"]} stops without changes.')


# Визначає можливість дістатися з однієї зупинки до іншої з можливістю пересадки
def option3(tram_data, tram_stops_routes_dict):
    print("\tIs it possible to get from the stop <name_of_stop> to the stop <name_of_stop>?")
    first_pos = str(input('\tInput the starting station: '))
    last_pos = str(input('\tInput the end station: '))
    print("\tAnswer: ", end="")

    if tram_stops_routes_dict[first_pos][last_pos]["withTramChange"]:
        if len(tram_stops_routes_dict[first_pos][last_pos]["routes"]) > 0:
            trams = [str(route["tram"]) for route in tram_stops_routes_dict[first_pos][last_pos]["routes"]]
            print(("✅ It is possible, with a change transport. Get on the tram №{0} ").format(", then ".join(trams)))
        else:
            print("❌ It`s impossible.")
    else:
        if len(tram_stops_routes_dict[first_pos][last_pos]["routes"]) > 0:
            trams = [str(route["tram"]) for route in tram_stops_routes_dict[first_pos][last_pos]["routes"]]
            print(("✅ You can get on the tram №{0}.").format(" or ".join(trams)))
        else:
            print("❌ It`s impossible.")


# Визначає, якими трамваями можна дістатися до заданої зупинки
def option4(tram_data, tram_stops_routes_dict):
    print("\tWhich trams can take you to the stop <name_of_stop>?")
    station = str(input('\tInput the station name:  '))
    print("\tAnswer: ", end="")
    trams_numbers = []
    for tram in tram_data:
        if station in tram_data[tram]["stops"]:
            trams_numbers.append(str(tram))
    print(", ".join(trams_numbers))


# Визначає шлях із однієї зупинки до іншої та виводить інструкції з пересадками
def option5(tram_data, tram_stops_routes_dict):
    print("\tHow to get from stop <name_of_stop> to stop <name_of_stop>?")
    first_pos = str(input('\tInput the starting station: '))
    last_pos = str(input('\tInput the end station: '))
    print("\tAnswer: ", end="")

    if not tram_stops_routes_dict[first_pos][last_pos]["withTramChange"]:
        routes_cnt = len(tram_stops_routes_dict[first_pos][last_pos]["routes"])
        for i in range(routes_cnt):
            if i > 0:
                print("or")
            tram_numb = tram_stops_routes_dict[first_pos][last_pos]["routes"][i]["tram"]
            number_of_stations = tram_stops_routes_dict[first_pos][last_pos]["routes"][i]["stops"]
            direction_info = tram_stops_routes_dict[first_pos][last_pos]["routes"][i]["direction"]
            print(
                f'Go to the stop {first_pos} tram №{tram_numb}. Get on the tram №{tram_numb} in direction {direction_info["from"]}-{direction_info["to"]}. Take the tram {number_of_stations} stops. See route diagram in this tram ')
    else:
        isStart = True
        for route in tram_stops_routes_dict[first_pos][last_pos]["routes"]:
            tram_numb = route["tram"]
            number_of_stations = route["stops"]
            direction_info = route["direction"]
            if isStart:
                isStart = False
                print(
                    f'Go to stop {first_pos} tram №{tram_numb}. Get on the tram №{tram_numb} in direction {direction_info["from"]}-{direction_info["to"]}. ', end='')
            else:
                print(f'Get on the tram №{tram_numb} in direction {direction_info["from"]}-{direction_info["to"]}. ', end='')
            print(f'Take the tram {number_of_stations} stops. ', end='')
        print(f'See route diagram in this tram. {last_pos} the stop will be yours.')


# Головна функція, яка взаємодіє з користувачем та обробляє вибрані опції
def get_tram_menu(tram_data, tram_stops_routes_dict):
    tram_options()
    options = {"1": option1, "2": option2, "3": option3, "4": option4, "5": option5}
    while True:
        action = str(input('\nChoose an option: '))
        try:
            options[action](tram_data, tram_stops_routes_dict)
        except KeyError:
            print("\t❌ Invalid input.")

def main():
    tram_data, tram_stops_routes_dict = get_tram_data_and_stops_dict()
    get_tram_menu(tram_data, tram_stops_routes_dict)

if __name__ == "__main__":
    main()
