import logging
import os
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

class Logger():

    def __init__(self, name):

        self.name = name
        self.logfolderName = self.name + "-logs"
        cwd = os.getcwd()
        self.items = os.listdir(cwd)

    def checkForLogFolder(self):
        #print(self.logfolderName)
        if self.logfolderName in self.items:
            return True
        else:
            return False
        
    def createOldLogsFolder(self)->str:
        currentDate = datetime.now()
        newFolderName = currentDate.strftime("date_%m_%d_%y_time_%H_%M_logs")

        if not self.checkForLogFolder():
            try:
                os.mkdir(self.logfolderName)
            except FileExistsError:
                logger.warning("Warning:Folder Might exsist already but has the wrong capitals somewhere")

        mkNewFolderPath = self.logfolderName + "/" + newFolderName

        try:
            os.mkdir(mkNewFolderPath)
            return mkNewFolderPath
        except FileExistsError:
            return mkNewFolderPath
    
    def isLog(self, fileName):
        for i, char in enumerate(fileName):
            if char == '.' and i != 0:
                fileType = fileName[i:]
                #print(fileType)
                if fileType == ".log":
                    return True
        return False
        
    def checkForLogs(self)->bool:
        for item in self.items:
            if self.isLog(item):
                return True
        return False
    
    def checkForName(self, fileName, targetName):
        if len(fileName) < len(targetName)+4:
            return False
        
        t = 0    
        for i in range(len(fileName)):
            if t > 0 and fileName[i] != targetName[t]:
                t = 0
            
            if fileName[i] == targetName[t]:
                t += 1
                if t == len(targetName):
                    return True
        
        return False
                
    def moveOldLogFiles(self, oldLogsPath):
        #making my own algo to find the log extensions
        for item in self.items:
            if self.isLog(item) and self.checkForName(item,self.name):
                shutil.move(item, oldLogsPath)

    def setupDirectory(self):
        if self.checkForLogs():
            newDirPath = self.createOldLogsFolder()
            self.moveOldLogFiles(newDirPath)
        elif not self.checkForLogFolder():
            os.mkdir(self.logfolderName)

def main():
    log = Logger("fisher")
    # log.checkForLogs()
    log.setupDirectory()
    result = None
    result = log.checkForLogFolder()
    result = log.checkForName("fyishettityfishfsdsfdffisssshhheefiishfisheherr_log.log","fisher")
    print(result)
    

if __name__ == "__main__":
    main()