import pandas as pd
import requests
from io import StringIO

#***********************************************************************************************************#

flag = True
count = 0
analysis = ""
while (flag):
    analysis = input('Enter type (skaters/goalies/teams): \n')

    if analysis in ["skaters", "goalies", "teams"]:
        print(f"Proceeding with type: {analysis}\n")
        flag = False
    else:
        print("Invalid type")

flag = True
count = 0
year = ""
while (flag):
    year = input('Enter year (2008-2024): \n')

    if int(year) >= 2008 and int(year) <= 2024:
        print(f"Proceeding with year: {year}\n")
        flag = False
    else:
        print("Invalid year")

flag = True
count = 0
time = ""
while (flag):
    time = input('Regular season (R) or Playoffs (P): \n')

    if time.upper() == 'R':
        time = "regular"
        print(f"Proceeding with: {time} (R)\n")
        flag = False
    elif time.upper() == 'P':
        time = "playoffs"
        print(f"Proceeding with: {time} (P)\n")
        flag = False
    else:
        print("Invalid input")

#***********************************************************************************************************#

# Did not make this
url = f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{year}/{time}/{analysis}.csv"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
else:
    print(f"Error: {response.status_code}")

#***********************************************************************************************************#

if analysis == "skaters":
    flag = True
    count = 0
    while (flag):
        players = input('Enter skaters (Fname Lname/Fname Lname): \n')

        if '/' in players:
            player1, player2 = players.split('/')
        else:
            print("Please re-enter in a proper format\n")

        # print(len(df[df['name'].isin([player1, player2])]))

        # Check to see if the number of instances is 1 or 2 players (5 per for each situation)
        if len(df[df['name'].isin([player1, player2])]) <= 5:
            print("Name error: please re-enter names")
        else:
            flag = False

    players = df[df['name'].isin([player1, player2])]

    player_metrics = [
        "name", "situation", "gameScore", "onIce_xGoalsPercentage", "onIce_corsiPercentage", "I_F_xGoals", 
        "I_F_goals", "I_F_primaryAssists", "I_F_points", "I_F_shotsOnGoal", 
        "I_F_highDangerxGoals", "penaltiesDrawn"
    ]

    flag = True
    count = 0
    situation = ""
    while (flag):
        situation = input('Enter situation (5on5/4on5/5on4/other/all): \n')

        if situation in ["5on5", "4on5", "5on4", "other", "all"]:
            print(f"Proceeding with situation: {situation}\n")
            flag = False
        else:
            print("Invalid situation")

    newPlayers = players[player_metrics]
    newPlayers = newPlayers[newPlayers['situation'] == situation]

    playerMetrics = []
    playerScores = []

    def scores(p1Row, p2Row):
        # these are kind of arbitrary, just based on my opinion and their definition
        importance = {
            "gameScore": 2.5,
            "onIce_xGoalsPercentage": 2,
            "onIce_corsiPercentage": 2,
            "I_F_xGoals": 2,
            "I_F_goals": 2,
            "I_F_primaryAssists": 2,
            "I_F_points": 1.5,
            "I_F_shotsOnGoal": 1.5, 
            "I_F_highDangerxGoals": 2, 
            "penaltiesDrawn": 1.5,
        }

        p1Score = 0
        p2Score = 0
        
        for stat, weight in importance.items():
            p1Score += p1Row[stat] * weight
            p2Score += p2Row[stat] * weight

            playerScores.append([p1Score, p2Score])
            playerMetrics.append(stat)
        
        if p1Score > p2Score:
            return f"Prediction: {p1Row['name']} is favored with {p1Score:.2f} over {p2Score:.2f}."
        elif p2Score > p1Score:
            return f"Prediction: {p2Row['name']} is favored with {p2Score:.2f} over {p1Score:.2f}."
        else:
            return "Even Prediction"

    p1Data = newPlayers[newPlayers["name"] == player1]
    p2Data = newPlayers[newPlayers["name"] == player2]

    if p1Data.empty:
        print(f"No data for {player1}, {player2} is favoured")
    elif p2Data.empty:
        print(f"No data for {player2}, {player1} is favoured")
    else:
        print(scores(p1Data.iloc[0], p2Data.iloc[0]))
    
    print(newPlayers.head(10))

if analysis == "goalies":
    flag = True
    count = 0
    while (flag):
        goalies = input('Enter goalies (Fname Lname/Fname Lname): \n')

        if '/' in goalies:
            goalie1, goalie2 = goalies.split('/')
        else:
            print("Please re-enter in a proper format\n")

        # print(len(df[df['name'].isin([goalie1, player2])]))

        # Check to see if the number of instances is 1 or 2 players (5 per for each situation)
        if len(df[df['name'].isin([goalie1, goalie2])]) <= 5:
            print("Name error: please re-enter names")
        else:
            flag = False

    goalies = df[df['name'].isin([goalie1, goalie2])]

    goalie_metrics = [
        "name", "situation", "goals", "highDangerGoals", "icetime", "xRebounds", "flurryAdjustedxGoals", "penalityMinutes"
    ]

    flag = True
    count = 0
    situation = ""
    while (flag):
        situation = input('Enter situation (5on5/4on5/5on4/other/all): \n')

        if situation in ["5on5", "4on5", "5on4", "other", "all"]:
            print(f"Proceeding with situation: {situation}\n")
            flag = False
        else:
            print("Invalid situation")

    newGoalies = goalies[goalie_metrics]
    newGoalies = newGoalies[newGoalies['situation'] == situation]

    goalieMetrics = []
    goalieScores = []

    def scores(g1Row, g2Row):
        # these are kind of arbitrary, just based on my opinion and their definition
        # add goal scores (x and actual combined)
        importance = {
            "goals": 2.5,
            "highDangerGoals": 2,
            "icetime": 1.5,                 
            "xRebounds": -1.5,
            "flurryAdjustedxGoals": -2,
            "penalityMinutes": -0.5
        }

        g1Score = 0
        g2Score = 0
        
        for stat, weight in importance.items():
            g1Score += g1Row[stat] * weight
            g2Score += g2Row[stat] * weight

            goalieScores.append([g1Score, g2Score])
            goalieMetrics.append(stat)
        
        if g1Score > g2Score:
            return f"Prediction: {g1Row['name']} is favored with {g1Score:.2f} over {g2Score:.2f}."
        elif g2Score > g1Score:
            return f"Prediction: {g2Row['name']} is favored with {g2Score:.2f} over {g1Score:.2f}."
        else:
            return "Even Prediction"

    g1Data = newGoalies[newGoalies["name"] == goalie1]
    g2Data = newGoalies[newGoalies["name"] == goalie2]

    if g1Data.empty:
        print(f"No data for {g1Data}, {g2Data} is favoured")
    elif g2Data.empty:
        print(f"No data for {g2Data}, {g1Data} is favoured")
    else:
        print(scores(g1Data.iloc[0], g2Data.iloc[0]))
    
    print(newGoalies.head(10))

if analysis == "teams":

    abbreviations = [
        "ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL","CBJ", 
        "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", 
        "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJS", 
        "STL", "TBL", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG"
    ]

    flag = True
    count = 0
    while (flag):
        teams = input('Enter teams (team/team), AB for abbreviations: \n')

        if teams.lower() == 'ab':
            print(abbreviations)
        else: 
            if '/' in teams:
                team1, team2 = teams.split('/')
                team1 = team1.upper()
                team2 = team2.upper()
                if team1 in abbreviations and team2 in abbreviations:
                    print(f"Proceeding with teams: {team1} and {team2}\n")
                    flag = False
                else:
                    print("One or more invalid teams\n")
            else:
                print("Please re-enter in a proper format\n")


    teams = df[df['team'].isin([team1, team2])]

    team_metrics = [
        "team", "situation", "xGoalsPercentage", "corsiPercentage", "fenwickPercentage", 
        "highDangerxGoalsFor", "highDangerxGoalsAgainst", "goalsFor", "goalsAgainst", 
        "penaltiesFor", "penaltiesAgainst", "takeawaysFor", "giveawaysAgainst"
    ]

    flag = True
    count = 0
    situation = ""
    while (flag):
        situation = input('Enter situation (5on5/4on5/5on4/other/all): \n')

        if situation in ["5on5", "4on5", "5on4", "other", "all"]:
            print(f"Proceeding with situation: {situation}\n")
            flag = False
        else:
            print("Invalid situation")

    newTeams = teams[team_metrics]
    newTeams = newTeams[newTeams['situation'] == situation]

    teamMetrics = []
    teamScores = []

    def scores(t1Row, t2Row):
        # these are kind of arbitrary, just based on my opinion and their definition
        importance = {
            "xGoalsPercentage": 2.5, 
            "corsiPercentage": 2, 
            "fenwickPercentage": 2, 
            "highDangerxGoalsFor": 2, 
            "highDangerxGoalsAgainst": -2, 
            "goalsFor": 1.5, 
            "goalsAgainst": -1.5, 
            "penaltiesFor": 1.5, 
            "penaltiesAgainst": -1.5, 
            "takeawaysFor": 1.5, 
            "giveawaysAgainst": -1.5
        }

        t1Score = 0
        t2Score = 0
        
        for stat, weight in importance.items():
            t1Score += t1Row[stat] * weight
            t2Score += t2Row[stat] * weight

            teamScores.append([t1Score, t2Score])
            teamMetrics.append(stat)
        
        if t1Score > t2Score:
            return f"Prediction: {t1Row['team']} is favored with {t1Score:.2f} over {t2Score:.2f}."
        elif t2Score > t1Score:
            return f"Prediction: {t2Row['team']} is favored with {t2Score:.2f} over {t1Score:.2f}."
        else:
            return "Even Prediction"

    t1Data = newTeams[newTeams["team"] == team1]
    t2Data = newTeams[newTeams["team"] == team2]

    if t1Data.empty:
        print(f"No data for {team1}, {team2} is favoured")
    elif t2Data.empty:
        print(f"No data for {team2}, {team1} is favoured")
    else:
        print(scores(t1Data.iloc[0], t2Data.iloc[0]))
    
    print(newTeams.head(10))

