__author__ = 'Swapnil'

import requests
import json
import datetime

def leagueSelection():
    # Getting matches info:- All recent and upcoming matches details
    all_matches = requests.get("https://api.crowdscores.com/api/v1/matches", headers={"x-crowdscores-api-key":apiKey}).json()

    # Associated league id
    input_league_id = league_id[sorted(league_id.keys())[input_league-1]]

    # Making list for every league so that matches can be arranged accordingly
    leag_wise_match = {}
    for league in all_leagues:
        leag_wise_match[league['dbid']] = []

    # Arranging matches by their leagues
    for match in all_matches:
        leag_wise_match[match['competition']['dbid']].append(match['dbid'])

    match_id = []
    index=0; s_no=1
    total_matches = len(all_matches)
    print("\nRECENT MATCHES\n")

    # Recent Matches
    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(all_matches[index]['start'])/1000)

        if(match_time > datetime.datetime.now()):
            break

        if(all_matches[index]['competition']['dbid']==input_league_id):
            match_id.append(all_matches[index]['dbid'])
            print(s_no, all_matches[index]['homeTeam']['name']+" vs "+all_matches[index]['awayTeam']['name'], all_matches[index]['dbid'], match_time)
            s_no += 1
        index += 1

    print("\nUPCOMING MATCHES\n")

    # Upcoming Matches
    while(index < total_matches):
        match_time = datetime.datetime.fromtimestamp(int(all_matches[index]['start'])/1000)

        if(all_matches[index]['competition']['dbid']==input_league_id):
            match_id.append(all_matches[index]['dbid'])
            print(s_no, all_matches[index]['homeTeam']['name']+" vs "+all_matches[index]['awayTeam']['name'], all_matches[index]['dbid'], match_time)
            s_no += 1
        index += 1
    print("\n")

    return match_id, s_no


def matchSelection():
    # Associated match id
    input_match_id = match_id[input_match - 1]

    chosen_match = requests.get("https://api.crowdscores.com/api/v1/matches/"+str(input_match_id), headers={"x-crowdscores-api-key":apiKey}).json()

    if(input_match >= s_no):
        print("Team \'A\'.", chosen_match['homeTeam']['name'])
        print("\n           vs\n")
        print("Team \'B\'.", chosen_match['awayTeam']['name'], "\n\n")

        print("\nYOU CAN BET ON FOLLOWING CHOICES (points are shown against every choice):\n\n")
        print("1 Whether team \'A\' win or \'B\': if correct +1 else -1\n")
        print("2 Result would be draw: if correct +5 else -5\n")
        print("3 Goal difference: if correct +10 else -5\n")
        print("4 Exact score: if correct +50 else -5\n")

    else:
        print("\nMATCH SUMMARY:\n")

        print("Team \'A\'.", chosen_match['homeTeam']['name'])
        print("           vs")
        print("Team \'B\'.", chosen_match['awayTeam']['name'], "\n")

        if(chosen_match['outcome']['winner'] == 'draw'):
            print("* Result: DRAW\n")
        else:
            if(chosen_match['outcome']['winner'] == 'home'):
                print("* Result: Team \'A\'.", chosen_match['homeTeam']['name'], "won")
            else:
                print("* Result: Team \'A\'.", chosen_match['awayTeam']['name'], "won\n")
        print("* Match Score:", chosen_match['homeGoals'], "-", chosen_match['awayGoals'])


# Reading api_key
apiKey = open('api_key', 'r').read()

# Getting leagues info:- All leagues and competitions detail
all_leagues = requests.get("https://api.crowdscores.com/api/v1/competitions", headers={"x-crowdscores-api-key":apiKey}).json()


# Assigning id to every league
league_id = {}
for league in all_leagues:
    league_id[league['name']] = league['dbid']

# Displaying leagues for choices
s_no = 1
for league in sorted(league_id.keys()):
    print(s_no, league)
    s_no += 1


# Taking league input from user
input_league = int(input())
match_id, s_no = leagueSelection()

# Taking match input from user
input_match = int(input())
matchSelection(match_id)
