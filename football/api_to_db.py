import sys, os, django
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
os.environ["DJANGO_SETTINGS_MODULE"] = "MakeABet.settings"
django.setup()


from football.football_data import all_match_updates
from football.models import Match

all_matches = all_match_updates()

league_ids = [ 2, 46, 47, 49, 36, 48, ]

for league_id in league_ids:
    league_match_list = all_matches[league_id]
    for match in league_match_list:

        try:
            Match.objects.get(match_id=match['dbid'])
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
