from unicodedata import name
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
        self.weburl= "http://dreamlo.com/lb/"
        self.database_highscore=[]
        self.PlayerHighscore = 6666

    def load(self):
        
        response = requests.get(self.weburl + self.publicCode + "/json")
        response = response.json()
        for x in response["dreamlo"]["leaderboard"]["entry"]:
            self.database_highscore.append(dreamloData(x["name"],x["score"],x["seconds"],x["text"],x["date"]))
        print(self.database_highscore)

    def save(self,_username,_score,_version,_time):
        #read DB if any entry with the same name, delete if new Highscore is better
        #save new Highscore
        response = requests.get(self.weburl + self.privateCode + "/add/" + _username + "/" + str(_score) +"/"+ str(_time) +"/" + _version)
        print (response)
        # update db
        for x in self.database_highscore:
            if x.username == _username:
                if int(x.score) < _score:
                    x.score = _score
                    x.time = _time
                    x.version = _version
                    # Returns a datetime object containing the local date and time
                    dateTimeObj = datetime.now()
                    # get the time object from datetime object
                    timeObj = dateTimeObj.time()
                    x.date = ('%d-%d-%d %d:%d:%d' % (
timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))

    def display(self):
        pass
    def highscorestring(self):
        string = ""
        for index in self.database_highscore:
            string += ('Playername: % \t Score: % \t totaltime: % \t version: % \t date: % \n' (self.database_highscore[index]["name"], self.database_highscore[index]["score"], self.database_highscore[index]["version"], self.database_highscore[index]["time"], self.database_highscore[index]["date"]))
        return string
        
class dreamloData():
    def __init__(self,_username,_score,_version,_time, _date):
        self.username = _username
        self.score = _score
        self.version= _version
        self.time = _time
        self.date = _date
