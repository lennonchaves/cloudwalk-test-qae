# importing the module
from pathlib import Path
import json


# Function to read the qgames.log file
def read_file():
    # get the path from the current folder
    directory = Path(__file__).parents[1]
    # set the file to be read
    log_file = str(directory) + "/qgames.log"
    # read the log file
    with open(log_file) as log:
        log = log.readlines()
    # return the log read
    return log


# Function to extract and group game data from each match (players and death causes)
def group_game_data_by_match(log):
    # Initialize the variables
    init_game = ["InitGame"]
    kill_game = ["Kill"]
    game_list = []
    count = 0
    # read each line to find the current game.
    for line in log:
        for init in init_game:
            if init in line:
                count = count + 1
                game_list.append("game_" + str(count))
                break
        # find a new kill line
        for kill in kill_game:
            if kill in line:
                game_list.append(line)
                break

    game_dictionary = {}
    game_id = ""
    match = 0
    for game in game_list:
        # get the game
        if "game" in game:
            game_dictionary[game] = {}
            game_id = game
            match = 0
        # get the kills from the game
        if "Kill" in game:
            # split the line to get the player a, player b and death cause
            match = match + 1
            match_id = "match_" + str(match)
            game_dictionary[game_id][match_id] = {}
            game_split = game.split(":")
            game_match = game_split[3]
            game_split = game_match.split("killed")
            # get the player a from log file
            player_a = game_split[0]
            game_split = game_split[1].split("by")
            # get the player b from log file
            player_b = game_split[0]
            # get the death cause
            death_cause = game_split[1]
            # generate the dictionary with player a, player b and death cause
            game_dictionary[game_id][match_id]['player_a'] = player_a
            game_dictionary[game_id][match_id]['player_b'] = player_b
            game_dictionary[game_id][match_id]['death_cause'] = death_cause

    return game_dictionary


# Function to get the ranking by each game
def get_ranking(kills):
    # sort the dictionary with ranking
    ranking = dict(sorted(kills.items(), key=lambda item: item[1], reverse=True))
    return ranking


# Function to read the dictionary extracted from log file and return a json format as result
def collect_kill_data(game_dictionary):
    # Initialize the game grouped information
    game_grouped_information = {}
    # Iterate the game dictionary to count the players and numbers by match
    for game in game_dictionary:
        # Initialize the main variables
        game_grouped_information[game] = {}
        match_item_list = game_dictionary[game]
        player_list = []
        total_kills = 0
        kills = {}
        # Count the total kills in each game
        for match_id in match_item_list:
            match = match_item_list[match_id]
            total_kills = total_kills + 1
            # Set the player in the players list
            player = match['player_a'].strip()
            if "<world>" not in player:
                if player not in player_list:
                    player_list.append(player)
            player = match['player_b'].strip()
            if "<world>" not in player:
                if player not in player_list:
                    player_list.append(player)
        # Create the kills list
        for player in player_list:
            kills[player] = 0
        # Fulfill the kill list with players results
        for match_id in match_item_list:
            match = match_item_list[match_id]
            player_count = match['player_a'].strip()
            if player_count in player_list:
                value = kills[player_count]
                value = value + 1
                kills[player_count] = value

        # Format the dictionary with expected structure
        game_grouped_information[game]['players'] = player_list
        game_grouped_information[game]['total_kills'] = total_kills
        game_grouped_information[game]['kills'] = kills
        game_grouped_information[game]['ranking'] = get_ranking(kills)

    return game_grouped_information


# Function to perform the log parser and ranking from each match
def execute():
    # read the file
    logs = read_file()
    # group data by each match
    dictionary = group_game_data_by_match(logs)
    # collect the kill data and organize in a dictionary
    kill_data = collect_kill_data(dictionary)
    # print the output in json format
    output = json.dumps(kill_data, indent=3)
    print(output)
