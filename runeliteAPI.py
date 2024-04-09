import requests
import json
import time
from verification import Verifyer

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
    inventJSON = None
    inventArray = None

    def __init__(self):

        response = requests.get(self.baseAPIUrl)

        # if response.status_code == 200:

        #     print("API connected")
        # else:
        #     print("Unable to connect to runelite API")

    def getEventData(self):

        response = requests.get(self.baseAPIUrl + self.eventEndpoint)

        if response.status_code == 200:
            self.eventsJSON = response.text
            self.eventsDict = json.loads(self.eventsJSON)

    def getInventoryData(self):
        response = requests.get(self.baseAPIUrl + self.inventoryEndpoint)

        if response.status_code == 200:
            self.inventJSON = response.text
            self.inventArray = json.loads(self.inventJSON)

    def findItemInventory(self, itemID):
        #might be better to use numpy here, but it should never be too big since there's only 28 invent slots
        self.getInventoryData()
        for i,item in enumerate(self.inventArray):
            if item['id'] == itemID:
                return i

    def getItemQuantityInInventory(self,itemPosition):

        self.getInventoryData()
        item = self.inventArray[itemPosition]
        quantity = item['quantity']
        return quantity
    
    def getItemQuantityComplete(self,itemId):
        #same output as above but assumes you don't know it's position will return position and quantity
        self.getInventoryData()
        itemPos = self.findItemInventory(itemId)
        quantity = self.getItemQuantityInInventory(itemPos)

        return itemPos, quantity
    
    def getRunEnergy(self):
        self.getEventData()
        self.runEnergy = self.eventsDict["run energy"]/100
        return self.runEnergy

    def getNPCinfo(self):
        self.getEventData()
        npcName = self.eventsDict["npc name"]
        npcHealth = self.eventsDict["npc health "]/10
        return npcName, npcHealth
    
    def getCurrentWorldPosition(self):
        self.getEventData()
        worldArray = self.eventsDict["worldPoint"]
        x = worldArray["x"]
        y = worldArray["y"]
        return (x, y)

    

if __name__ == "__main__":
    api = RuneLiteApi()

    # api.getInventoryData()

    # result = api.inventArray

    # for item in result:
    #     print(item)


    # print(type(api.getItemQuantityInInventory(1)))

    verifyer = Verifyer()
    while True:
        worldPos = api.getCurrentWorldPosition()
        #result = verifyer.verifyInArea(api, (3177, 3296), 11)
        #print(result)
        
        # print(api.eventsDict["latest msg"])

        print(worldPos)
        time.sleep(0.6)
        
       
