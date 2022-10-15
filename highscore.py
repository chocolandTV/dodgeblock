import urllib.request
import time
import requests
import json
from datetime import datetime

### example /add/Choco/2096/0.1/2022.10.15###


class HighscoreManager():
    def __init__(self):
        self.privateCode = "zkK4Eqp9-EGpNsaTi9fahA4kPpG5kOvESDAKDqhQkV4A"
        self.publicCode = "634a62228f40bb11d8b929c0"
        self.weburl = "http://dreamlo.com/lb/"
        self.database_highscore = []
        self.PlayerHighscore = 6666

    def load(self):

        response = requests.get(self.weburl + self.publicCode + "/json")
        response = response.json()
        for x in response["dreamlo"]["leaderboard"]["entry"]:
            self.database_highscore.append(
                (x["name"], x["score"], x["seconds"], x["text"], x["date"]))
        print(self.database_highscore)

    def save(self, _username, _score, _version, _time):
        # read DB if any entry with the same name, delete if new Highscore is better
        # save new Highscore
        response = requests.get(self.weburl + self.privateCode + "/add/" +
                                _username + "/" + str(_score) + "/" + str(_time) + "/" + _version)
        print(response)
        # update db
        for x in self.database_highscore:
            if x[0] == _username:
                if int(x[1]) < _score:
                    x[1] = _score
                    x[2] = _time
                    x[3] = _version

    def highscorestring(self):
        result=[]
        for index in range(0, len(self.database_highscore)):
            result.append("Name: {} Score: {} Totaltime: {} Version: {} Date: {}".format(
                self.database_highscore[index][0], self.database_highscore[index][1], self.database_highscore[index][2], self.database_highscore[index][3], self.database_highscore[index][4]))
        return result
