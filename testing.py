from sportsreference.nba.schedule import Schedule
from sportsreference.nba.teams import Teams
import pandas as pd
import numpy as np


column_names = ['opp_assists',
       'opp_blocks',
        'opp_defensive_rebounds',
      'opp_field_goal_attempts',
       'opp_field_goal_percentage', 'opp_field_goals',
        'opp_free_throw_attempts',
       'opp_free_throw_percentage', 'opp_free_throws', 'opp_losses',
       'opp_minutes_played', 
        'opp_offensive_rebounds',
       'opp_personal_fouls', 'opp_points',
       'opp_steals', 
       'opp_three_point_field_goal_attempts',
       'opp_three_point_field_goal_percentage', 'opp_three_point_field_goals',
        'opp_total_rebounds',
       'opp_turnovers', 'opp_two_point_field_goal_attempts',
       'opp_two_point_field_goal_percentage', 'opp_two_point_field_goals',
       'opp_wins', 'assists', 
       'blocks',
       'defensive_rebounds',
       'field_goal_attempts', 'field_goal_percentage', 'field_goals',
     'free_throw_attempts',
       'free_throw_percentage', 'free_throws', 'losses', 'minutes_played',
       'offensive_rebounds', 'personal_fouls', 'points', 
       'steals','three_point_field_goal_attempts',
       'three_point_field_goal_percentage', 'three_point_field_goals',
       'total_rebounds',
        'turnovers',
       'two_point_field_goal_attempts', 'two_point_field_goal_percentage',
       'two_point_field_goals', 'wins', 'pace']

def getStatsTillGame(abbrev, year, gameNum):
    team = Teams(year)(abbrev)
    stats = pd.DataFrame(np.zeros((gameNum, 49)))
    stats.columns = column_names
    for gameindex in range(1, gameNum):
        gamedata = team.schedule[gameindex].boxscore.dataframe
        if (gamedata['winner'][0] == "Home" and gamedata['winning_abbr'][0] == abbrev) or (gamedata['winner'][0] == "Away" and gamedata['losing_abbr'][0] == abbrev):
            gamedata.rename(columns=lambda x: x.replace("home_", "").replace("away", "opp"), inplace=True)
        else:
            gamedata.rename(columns=lambda x: x.replace("away_", "").replace("home", "opp"), inplace=True)

        for key, value in gamedata.iteritems(): 
            if(key in stats.columns):
                if(not gameindex == 1):
                    stats[key][gameindex-1] = stats[key][gameindex-2] + value[0]
                else:
                    stats[key][gameindex-1]  = value[0]

        for key, value in stats.iteritems(): 
            if("percentage" in key or "pace" in key):
                if(not "assist" in key and not "block" in key and not "steal" in key and not "turnover" in key and not "rebound" in key and not "pace" in key):
                   stats[key][gameindex-1] = stats[key.replace("_percentage","s")][gameindex-1]/stats[key.replace("percentage","attempts")][gameindex-1]
                else:
                    if(not gameindex == 1):
                        stats[key][gameindex-1] = stats[key][gameindex-1]/gameindex

    return(stats)




x = getStatsTillGame("NYK", 2019, 6)
print(x)
