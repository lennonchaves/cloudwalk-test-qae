# importing the module
import log_parser
import json


# Function to read the log file and group data by match
def parser():
    # read the file
    logs = log_parser.read_file()
    # extract the game information (players, kill, death cause)
    game_dictionary = log_parser.group_game_data_by_match(logs)
    return game_dictionary


# Function to collect kill data from the dictionary created
def group_deaths_information(game_dictionary):
    deaths_grouped_information = {}

    for game in game_dictionary:

        deaths_grouped_information[game] = {}

        match_item_list = game_dictionary[game]

        death_list = []
        kills_by_means = {}
        for match_id in match_item_list:
            match = match_item_list[match_id]
            death = match['death_cause'].strip()

            if death not in death_list:
                death_list.append(death)

        for death in death_list:
            kills_by_means[death] = 0

        for match_id in match_item_list:
            match = match_item_list[match_id]
            death = match['death_cause'].strip()

            if death in death_list:
                value = kills_by_means[death]
                value = value + 1
                kills_by_means[death] = value

        deaths_grouped_information[game]['kills_by_means'] = kills_by_means
    return json.dumps(deaths_grouped_information, indent=3)


# Function to get deaths information grouped by match
def execute():
    dictionary = parser()
    output = group_deaths_information(dictionary)
    print(output)
