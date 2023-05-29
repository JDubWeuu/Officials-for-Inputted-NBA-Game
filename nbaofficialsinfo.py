import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

referee_data = pd.read_csv('officials.csv', usecols=['game_id', 'first_name', 'last_name'])

game_data = pd.read_csv('game.csv')

game_data['game_date'] = game_data['game_date'].str.split(' ').str[0]

game_id_dict = dict(zip(zip(game_data['team_name_home'], game_data['team_name_away'], game_data['game_date']), game_data['game_id']))

referees_dict = {}
for _, row in referee_data.iterrows():
    game_id = row['game_id']
    referee = row['first_name'] + ' ' + row['last_name']
    if game_id in referees_dict:
        referees_dict[game_id].append(referee)
    else:
        referees_dict[game_id] = [referee]

def get_game_info(home_team, away_team, game_date):
    game_key = (home_team, away_team, game_date)
    if game_key in game_id_dict:
        game_id = game_id_dict[game_key]

        if game_id in referees_dict:
            referees = referees_dict[game_id]

            # Retrieve other information from game_data based on game ID
            game_info = game_data.loc[game_data['game_id'] == game_id, ['team_name_home', 'team_name_away', 'game_date']].values[0]

            refs = ', '.join(referees)

            return f'The referees for the game between the {game_info[0]} and the {game_info[1]} on {game_info[2]} were {refs}'
        else:
            return "No referee information found for the given game ID."
    else:
        return "No game information found for the given input."
    

#Example: 'Los Angeles Lakers', 'New Orleans Pelicans', '2022-11-02'
home_team, away_team, game_date = input('Please insert the home team name, away team name, and game_date (YYYY-MM-DD) with commas. ').split(', ')

print(home_team.capitalize())

try:
    game_info = get_game_info(home_team.title(), away_team.title(), game_date)
except:
    print('Sorry, one of your inputs was not put in the correct format, please try again.')
print(game_info)

