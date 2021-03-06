import sys, os, django
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "MakeABet.settings"
django.setup()

import requests
import pickle
from football.models import Bets, Match
import time
from MakeABet.settings import BASE_DIR

api_key = open(os.path.join(BASE_DIR, 'football', 'api_key2'), 'r').read()
#api_key = '7bd28a575c15404ba1e0fd9ebccfaa5d'


def football_matches():
    """ Get all the for recent matches (upto 24 hours before present time) and upcoming matches(upto 7 days from present time) """

    league_file = open(os.path.join(BASE_DIR, 'football', 'all_leagues'), 'rb')
    all_leagues = pickle.load(league_file)

    all_matches = requests.get("https://api.crowdscores.com/api/v1/matches?api_key="+api_key).json()
    leag_wise_match = {}
    for league in all_leagues:
        leag_wise_match[league['dbid']] = []

    for match in all_matches:
        try:
            leag_wise_match[match['competition']['dbid']].append({'dbid':match['dbid'], 'homeTeam':match['homeTeam']['name'], 'awayTeam':match['awayTeam']['name'], 'matchTime':match['start'], 'outcome':match['outcome'], 'homeGoals':match['homeGoals'], 'awayGoals':match['awayGoals'], 'league': match['competition']['name'] })
        except:
            pass

    return leag_wise_match

def update_match():
    """ Update match data in the database """

    all_matches = football_matches()
    league_ids = [ 2, 46, 47, 49, 36, 48, ]

    for league_id in league_ids:
        league_match_list = all_matches[league_id]
        for match in league_match_list:

            try:
                # check if given match already in database
                match_instance = Match.objects.get(match_id=match['dbid'])

                # if match result is not in db but is updated in api call then update it in database
                if match_instance.outcome is None :
                    if match['outcome'] is not None :
                        match_instance.outcome = match['outcome']['winner']
                        match_instance.home_team_goals = match['homeGoals']
                        match_instance.away_team_goals = match['awayGoals']
                        match_instance.save()

                        # Checking bets and assigning points for the match

                        bets = Bets.objects.filter(match_id__match_id=match['dbid'])
                        for bet in bets:
                            points_earned = 0

                            #for winner prediction
                            if match['homeGoals'] > match['awayGoals']:
                                if bet.winner_prediction == 0:
                                    points_earned += 5
                                else:
                                    points_earned -= 5
                            elif match['homeGoals'] == match['awayGoals']:
                                if bet.winner_prediction == 2:
                                    points_earned += 5
                                else:
                                    points_earned -=5
                            else:
                                if bet.winner_prediction == 1:
                                    points_earned += 5
                                else:
                                    points_earned -= 5

                            #for goal difference prediction
                            if bet.goal_difference == abs(match['homeGoals'] - match['awayGoals']):
                                points_earned += 10
                            else:
                                points_earned -=5

                            #for score prediction
                            if (bet.home_goals_prediction == match['homeGoals']) and (bet.away_goals_prediction == match['awayGoals']):
                                points_earned += 25
                            else:
                                points_earned -= 5

                            bet.username.points += points_earned
                            bet.username.save()
            except:
                if match['outcome'] is not None:
                    winner = match['outcome']['winner']
                else:
                    winner = None

                new_match = Match(
                    match_id = match['dbid'],
                    league = match['league'],
                    home_team = match['homeTeam'],
                    away_team = match['awayTeam'],
                    home_team_goals = match['homeGoals'],
                    away_team_goals = match['awayGoals'],
                    time = match['matchTime'],
                    outcome = winner,
                )
                new_match.save()

def start_up():
    """ Update match data every 5 minutes to database """
    while(True):
        try:
            update_match()
            print("Matches updated")
        except:
            continue

        time.sleep(299)

if __name__ == "__main__":
    update_match()