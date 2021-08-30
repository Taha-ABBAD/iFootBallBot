import json
from telegram.update import Update
import requests


class apiFootBall:

    # Calling Constructor
    def __init__(self, update: Update):
        self.update = update

    def standingPyId(self, id: str):

        url = "https://api-football-v1.p.rapidapi.com/v3/standings"

        querystring = {"season": "2021", "league": id}

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "75ad31e3admsh5d0185612636abep1edc73jsn517fc88a1307"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        jsonObj = json.loads(response.text)
        table = jsonObj['response'][0]['league']['standings'][0]
        lines = '# ' + '|' + 'Club name' + ' ' * 13 + '| Pt' + '\n'
        lines = lines + '-' * 29 + "\n"
        for teamObj in table:
            teamPosition = teamObj['rank']
            teamName = teamObj['team']['name']
            teamPoint = teamObj['points']
            if teamPosition < 10:
                s = 1
            else:
                s = 0
            space = 22 - len(teamName)
            line = str(teamPosition) + ' ' * s + '|' + str(teamName) + \
                ' '*space + '|' + ' ' + str(teamPoint)
            lines = lines + str(line) + "\n"
        return self.preFormattedStr(lines)

    def scorersPyId(self, id: str):
        url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"

        querystring = {"league": id, "season": "2021"}

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "75ad31e3admsh5d0185612636abep1edc73jsn517fc88a1307"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        jsonObj = json.loads(response.text)
        table = jsonObj['response']
        lines = '# ' + '|' + 'Name' + ' ' * 16 + '|Goals' + '\n'
        lines = lines + '-' * 29 + "\n"
        n = 0
        for playerObj in table:
            playerPosition = n+1
            playerName = playerObj['player']['name']
            playerGoals = playerObj['statistics'][0]['goals']['total']
            if playerPosition < 10:
                s = 1
            else:
                s = 0
            space = 20 - len(playerName)
            line = str(playerPosition) + ' ' * s + '|' + str(playerName) + \
                ' '*space + '|' + ' ' * 2 + str(playerGoals)
            lines = lines + str(line) + "\n"
        return self.preFormattedStr(lines)

    def assistsPyId(self, id: str):
        url = "https://api-football-v1.p.rapidapi.com/v3/players/topassists"

        querystring = {"league": id, "season": "2021"}

        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "75ad31e3admsh5d0185612636abep1edc73jsn517fc88a1307"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        jsonObj = json.loads(response.text)
        table = jsonObj['response']
        lines = '# ' + '|' + 'Name' + ' ' * 16 + '|Assists' + '\n'
        lines = lines + '-' * 31 + "\n"
        n = 0
        for playerObj in table:
            n = n+1
            playerPosition = n
            playerName = playerObj['player']['name']
            playerGoals = playerObj['statistics'][0]['goals']['assists']
            if playerPosition < 10:
                s = 1
            else:
                s = 0
            space = 20 - len(playerName)
            line = str(playerPosition) + ' ' * s + '|' + str(playerName) + \
                ' '*space + '|' + ' ' * 2 + str(playerGoals)
            lines = lines + str(line) + "\n"
        return self.preFormattedStr(lines)

    def preFormattedStr(self, s: str):
        s = str(s.strip())
        s = '```python\n' + s + '\n```'
        return str(s)
