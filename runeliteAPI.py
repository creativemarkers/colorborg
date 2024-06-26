import requests
import json
import time
import logging
from verification import Verifyer

logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

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
        #creating error logs, need to disable
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
    
    def getCameraYaw(self):
        self.getEventData()
        cameraArray = self.eventsDict["camera"]
        yaw = cameraArray["yaw"]
        return yaw

    def getMovementStatus(self):
        self.getEventData()
        aniPose = self.eventsDict["animation pose"]

        #print(aniPose)
        if aniPose == 824:
            return "running"
        elif aniPose == 819:
            return "walking"
        else:
            return "idle"
        
    def getAnimation(self):
        self.getEventData()
        animationInt = self.eventsDict["animation"]
        return animationInt

    

if __name__ == "__main__":
    api = RuneLiteApi()



    #     print(item)


    # print(type(api.getItemQuantityInInventory(1)))

    verifyer = Verifyer()
    while True:
        worldPos = api.getCurrentWorldPosition()
        # yaw = api.getCameraYaw()
        #result = verifyer.verifyInArea(api, (3177, 3296), 11)
        #print(result)
        
        # print(api.eventsDict["latest msg"])

        # result = api.findItemInventory(335)
        # print(result)

        print(worldPos)
        # yaw = api.getCameraYaw()
        # print(yaw)
        #api.getMovementStatus()
        # result = api.getAnimation()
        # print(result)
        time.sleep(0.6)


        
       
