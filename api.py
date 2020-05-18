import datetime
from functools import cached_property
import json
import os
from pprint import pprint
import time
from urllib.parse import urljoin

import requests


base_path = os.path.dirname(__file__)


class PlanetsAPI:

    baseurl = "https://api.planets.nu"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"})

        with open(os.path.join(base_path, "config.json")) as handle:
            config = json.load(handle)
            self.username = config["username"]
            self.password = config["password"]

    def post(self, name, data):
        return self.session.post(urljoin(self.baseurl, name), data=data)

    def get(self, name, **kwargs):
        return self.session.post(urljoin(self.baseurl, name), **kwargs)

    @cached_property
    def apikey(self):
        return self.post("account/login", {"username": self.username,
                                           "password": self.password}).json()["apikey"]

    def mygames(self):
        return self.post("account/mygames", {"apikey": self.apikey}).json()

    def loadturn(self, gameid):
        return self.post("game/loadturn", {"apikey": self.apikey,
                                           "gameid": gameid}).json()

    def loadinfo(self, gameid):
        return self.post("game/loadinfo", {"apikey": self.apikey,
                                           "gameid": gameid}).json()

    def loadturnnew(self, gameid):
        time.sleep(1)
        path = urljoin(self.baseurl, "game/loadturnnew")
        result = self.session.post(path, params={"apikey": self.apikey,
                                                 "gameid": gameid,
                                                 "forsave": "true",
                                                 "activity": "true"})
        return result.json()

    def save(self, gameid, turnfile):

        with open(os.path.join(base_path, turnfile)) as handle:
            turn = json.load(handle)

        out = {}
        out["trn"] = turn["rst"]
        return self.post("game/save", {"apikey": self.apikey,
                                       "gameid": gameid,
                                       "data": turn}).json()

    def fetchturn(self, gameid):
        now = datetime.datetime.now()
        turn = self.loadturn(gameid)

        path = os.path.join(
            base_path, f"{gameid}_{now.strftime('%Y%m%d_%H%M%S')}.json")
        with open(path, "w") as handle:
            json.dump(turn, handle, indent=2)

    def getdocs(self):
        return self.post("admin/getdocs", {"apikey": self.apikey}).json()


if __name__ == "__main__":

    gameid = 369182
    planets = PlanetsAPI()
    # pprint(planets.mygames().json())
    # planets.storeturn(369182)
    # result = planets.saveturn(369182, "369182_20200412_094435.json")
    # pprint(result)
    # result = planets.loadinfo(gameid)
    result = planets.loadturnnew(gameid)
    pprint(result)
