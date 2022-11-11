from pathlib import Path
import json


# Function to read the qgames.log file
def read_file():
    directory = Path(__file__).parents[1]
    log_file = str(directory) + "/qgames.log"
    with open(log_file) as log:
        log = log.readlines()

    return log


# Function to extract and group game data from each match (players and death causes)
def group_game_data_by_match(log):
    init_game = ["InitGame"]
    kill_game = ["Kill"]
    game_list = []
    count = 0

    for line in log:
        for init in init_game:
            if init in line:
                count = count + 1
                game_list.append("game_" + str(count))
                break
        for kill in kill_game:
            if kill in line:
                game_list.append(line)
                break

    game_dictionary = {}
    game_id = ""
    match = 0
    for game in game_list:
        if "game" in game:
            game_dictionary[game] = {}
            game_id = game
            match = 0
        if "Kill" in game:
            match = match + 1
            match_id = "match_" + str(match)
            game_dictionary[game_id][match_id] = {}
            game_split = game.split(":")
            game_match = game_split[3]
            game_split = game_match.split("killed")
            player_a = game_split[0]
            game_split = game_split[1].split("by")
            player_b = game_split[0]
            death_cause = game_split[1]

            game_dictionary[game_id][match_id]['player_a'] = player_a
            game_dictionary[game_id][match_id]['player_b'] = player_b
            game_dictionary[game_id][match_id]['death_cause'] = death_cause

    return game_dictionary


# Function to read the dictionary extracted from log file and return a json format as result
def collect_kill_data(game_dictionary):
    game_grouped_information = {}

    for game in game_dictionary:

        game_grouped_information[game] = {}

        match_item_list = game_dictionary[game]
        player_list = []
        total_kills = 0
        kills = {}
        for match_id in match_item_list:
            match = match_item_list[match_id]
            total_kills = total_kills + 1

            player = match['player_a'].strip()
            if "<world>" not in player:
                if player not in player_list:
                    player_list.append(player)

            player = match['player_b'].strip()
            if "<world>" not in player:
                if player not in player_list:
                    player_list.append(player)

        for player in player_list:
            kills[player] = 0

        for match_id in match_item_list:
            match = match_item_list[match_id]
            player_count = match['player_a'].strip()

            if player_count in player_list:
                value = kills[player_count]
                value = value + 1
                kills[player_count] = value

        game_grouped_information[game]['players'] = player_list
        game_grouped_information[game]['total_kills'] = total_kills
        game_grouped_information[game]['kills'] = kills

    return game_grouped_information


logs = read_file()
dictionary = group_game_data_by_match(logs)
kill_data = collect_kill_data(dictionary)
output = json.dumps(kill_data, indent=3)
print(output)
