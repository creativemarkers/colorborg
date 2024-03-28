import requests
import json

class RuneLiteApi():
    #uses "MORG HTTP API plugin on the plugin hub"
    baseAPIUrl = "http://localhost:8081"
    eventEndpoint = "/events"
    inventoryEndpoint = "/inv"
    statsEndpoint = "/stats"
    equipEndpoint = "equip"
    eventsJSON = None
    runEnergy = None
    eventsDict = None

    def __init__(self):

        response = requests.get(self.baseAPIUrl)

        if response.status_code == 200:

            print("API connected")
        else:
            print("Unable to connect to runelite API")

    def getEventData(self):

        response = requests.get(self.baseAPIUrl + self.eventEndpoint)

        if response.status_code == 200:
            self.eventsJSON = response.text
            self.eventsDict = json.loads(self.eventsJSON)

    def getRunEnergy(self):
        self.getEventData()
        self.runEnergy = self.eventsDict["run energy"]/100
        return self.runEnergy

    def getNPCinfo(self):
        self.getEventData()
        npcName = self.eventsDict["npc name"]
        npcHealth = self.eventsDict["npc health "]/10
        return npcName, npcHealth