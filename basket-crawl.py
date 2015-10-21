# Joe Siebert
# This program uses the NBA's API to get players' stats.

import requests
import json
import pandas as pd


debug = True

def main():
    # Get player name
    top5_scorers = {
                    "Russell Westbrook" : 201566,
                    "James Harden" : 201935,
                    "Lebron James" : 2544,
                    "Anthony Davis" : 203076,
                    "Demarcus Cousins" : 202326}

    # Array for player data
    players = []

    # Get stats
    for key in top5_scorers:
        stats = grab_stats(key, top5_scorers[key])
        players.append(stats.copy())

    # Print averages
    for i in range(len(players)):
        for key in players[i]:
            print(key, ':', players[i][key])

# The grab_stats function
def grab_stats(name, player_id):
    shots_url = get_url(player_id)

    player_data = parse_json(shots_url)

    return create_dictionary(name, player_data)

# The get_url function
def get_url(id_num):
    url = 'http://stats.nba.com/stats/playerdashptshotlog?' + \
    'DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&' + \
    'Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&' + \
    'PlayerID=' + str(id_num) + '&Season=2014-15&SeasonSegment=&'+ \
    'SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='

    return url

# The parse_json function
def parse_json(url):
    # Request URL and parse JSON
    response = requests.get(url)
    response.raise_for_status() # Raise exception if invalid response
    data = json.loads(response.text)

    return data

# The create_dictionary function
def create_dictionary(name, data):
    avg_def, avg_dribbles, avg_shot_distance, avg_touch_time = create_dataframe(data)

    # Dictionary for individual stats
    player_stats = {
            'name' : name,
            'avg_dribbles' : avg_dribbles,
            'avg_touch_time' : avg_touch_time,
            'avg_shot_distance' : avg_shot_distance,
            'avg_defender_distance' : avg_def}

    return player_stats

# The create_dataframe function
def create_dataframe(data):
    headers = data['resultSets'][0]['headers']
    shot_data = data['resultSets'][0]['rowSet']
    data_frame = pd.DataFrame(shot_data, columns=headers)
    avg_def = data_frame['CLOSE_DEF_DIST'].mean()
    avg_dribbles = data_frame['DRIBBLES'].mean()
    avg_shot_distance = data_frame['SHOT_DIST'].mean()
    avg_touch_time = data_frame['TOUCH_TIME'].mean()

    return avg_def, avg_dribbles, avg_shot_distance, avg_touch_time

main()
