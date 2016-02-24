__author__ = 'Swapnil'

import requests
import datetime
import pickle
import json
import os
from MakeABet.settings import BASE_DIR

api_key = open(os.path.join(BASE_DIR, 'football', 'api_key'), 'r').read()

def all_match_updates():
    # Getting matches info:- All recent and upcoming matches details
    # Getting leagues info:- All leagues and competitions detail

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


def league_matches_list(leag_wise_match, input_league_id):
    league_matches = {'recentMatches': [], 'upcomingMatches': []}

    index=0
    total_matches = len(leag_wise_match[input_league_id])

    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(leag_wise_match[input_league_id][index]['matchTime'])/1000)

        if(match_time > datetime.datetime.now()):
            break

        league_matches['recentMatches'].append({
            'homeTeam' : leag_wise_match[input_league_id][index]['homeTeam'],
            'awayTeam' : leag_wise_match[input_league_id][index]['awayTeam'],
            'dbid' : leag_wise_match[input_league_id][index]['dbid'],
            'matchTime' : match_time,
        })


        index += 1

    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(leag_wise_match[input_league_id][index]['matchTime'])/1000)

        league_matches['upcomingMatches'].append({
            'homeTeam' : leag_wise_match[input_league_id][index]['homeTeam'],
            'awayTeam' : leag_wise_match[input_league_id][index]['awayTeam'],
            'dbid' : leag_wise_match[input_league_id][index]['dbid'],
            'matchTime' : match_time,
        })
        index += 1

    return league_matches


def matchSelection(match_id):
    chosen_match = requests.get("https://api.crowdscores.com/api/v1/matches/"+str(match_id)+"?api_key="+api_key).json()
    match_dict = {}
    match_dict['matchTime'] = datetime.datetime.fromtimestamp(int(chosen_match['start'])/1000)
    match_dict['homeTeam'] = chosen_match['homeTeam']['name']
    match_dict['awayTeam'] = chosen_match['awayTeam']['name']

    if(match_dict['matchTime']>datetime.datetime.now()):
        pass
    else:
        match_dict['winner'] = chosen_match['outcome']['winner']
        match_dict['homeGoals'] = chosen_match['homeGoals']
        match_dict['awayGoals'] = chosen_match['awayGoals']

    return match_dict


if __name__ == "__main__":
    # Getting leagues info:- All leagues and competitions detail
    league_file = open('all_leagues', 'rb')
