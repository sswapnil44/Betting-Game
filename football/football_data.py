__author__ = 'Swapnil'

import requests
import json
import datetime
import pickle

def all_match_updates():
    # Getting matches info:- All recent and upcoming matches details
    all_matches = requests.get("https://api.crowdscores.com/api/v1/matches", headers={"x-crowdscores-api-key":apiKey}).json()

    leag_wise_match = {}
    for league in all_leagues:
        leag_wise_match[league['dbid']] = []

    for match in all_matches:
        leag_wise_match[match['competition']['dbid']].append({'dbid':match['dbid'], 'homeTeam':match['homeTeam']['name'], 'awayTeam':match['awayTeam']['name'], 'matchTime':match['start']})


    return leag_wise_match


def league_matches_list(leag_wise_match, input_league_id):
    league_matches = {'recentMatches':{}, 'upcomingMatches':{}}

    index=0; s_no=1
    total_matches = len(leag_wise_match[input_league_id])

    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(leag_wise_match[input_league_id][index]['matchTime'])/1000)

        if(match_time > datetime.datetime.now()):
            break

        league_matches['recentMatches'][s_no] = {}
        league_matches['recentMatches'][s_no]['homeTeam'] = leag_wise_match[input_league_id][index]['homeTeam']
        league_matches['recentMatches'][s_no]['awayTeam'] = leag_wise_match[input_league_id][index]['awayTeam']
        league_matches['recentMatches'][s_no]['dbid'] = leag_wise_match[input_league_id][index]['dbid']
        league_matches['recentMatches'][s_no]['matchTime'] = match_time

        s_no += 1
        index += 1

    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(leag_wise_match[input_league_id][index]['matchTime'])/1000)

        league_matches['upcomingMatches'][s_no] = {}
        league_matches['upcomingMatches'][s_no]['homeTeam'] = leag_wise_match[input_league_id][index]['homeTeam']
        league_matches['upcomingMatches'][s_no]['awayTeam'] = leag_wise_match[input_league_id][index]['awayTeam']
        league_matches['upcomingMatches'][s_no]['dbid'] = leag_wise_match[input_league_id][index]['dbid']
        league_matches['upcomingMatches'][s_no]['matchTime'] = match_time

        s_no += 1
        index += 1

    return league_matches


def matchSelection(match_dict):

    if(match_dict['matchTime']>datetime.datetime.now()):
        pass
    else:
        chosen_match = requests.get("https://api.crowdscores.com/api/v1/matches/"+str(match_dict['dbid']), headers={"x-crowdscores-api-key":apiKey}).json()
        match_dict['winner'] = chosen_match['outcome']['winner']
        match_dict['homeGoals'] = chosen_match['homeGoals']
        match_dict['awayGoals'] = chosen_match['awayGoals']

    return match_dict


if __name__ == "__main__":
    # Reading api_key
    apiKey = open('api_key2', 'r').read()

    # Getting leagues info:- All leagues and competitions detail
    league_file = open('all_leagues', 'rb')
    all_leagues = pickle.load(league_file)

    leag_wise_match = all_match_updates()
    print(leag_wise_match)
    league_matches = league_matches_list(leag_wise_match,145)
    print(league_matches)
    print(matchSelection({'homeTeam': 'Crucero del Norte', 'dbid': 53289, 'awayTeam': 'Club Atlético Paraná', 'matchTime': datetime.datetime(2016, 2, 22, 1, 30)}))


