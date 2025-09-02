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

url = f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{year}/{time}/teams.csv"
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
    print("selected skaters")
    print(df.head(10))

if analysis == "goalies":
    print("selected goalies")
    print(df.head(10))

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

    metrics = [
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

    newTeams = teams[metrics]
    newTeams = newTeams[newTeams['situation'] == situation]

    teamMetrics = []
    teamScores = []

    def scores(t1Row, t2Row):
        importance = {
            "xGoalsPercentage": 2, 
            "corsiPercentage": 1.5, 
            "fenwickPercentage": 1.5, 
            "highDangerxGoalsFor": 1.5, 
            "highDangerxGoalsAgainst": -1, 
            "goalsFor": 1.5, 
            "goalsAgainst": -1.5, 
            "penaltiesFor": 1, 
            "penaltiesAgainst": -1, 
            "takeawaysFor": 1, 
            "giveawaysAgainst": -1
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