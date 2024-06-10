import logging
import os
import shutil
from datetime import datetime
from utils.fernsUtils import calculateDaysSinceAD1

logger = logging.getLogger(__name__)

class LogOrganizer():

    def __init__(self, name:str)->None:
        self.name = name
        self.logfolderName = self.name + "-logs"
        self.cwd = os.getcwd()
        self.items = os.listdir(self.cwd)
        self.todaysDate = datetime.now()

    def isLogFile(self, fileName:str)->bool:
        for i, char in enumerate(fileName):
            if char == '.' and i != 0:
                fileType = fileName[i:]
                #print(fileType)
                if fileType == ".log":
                    return True
        return False
    
    def checkForLogs(self)->bool:
        for item in self.items:
            if self.isLogFile(item):
                return True
        return False
    
    def checkForLogFolder(self):
        #print(self.logfolderName)
        if self.logfolderName in self.items:
            return True
        else:
            return False
    
    """
    DEPERECATED
    """
    # def checkForName(self, fileName, targetName):
    #     #look up KMP and Boyer-Moore for other, better path finding algorithms
    #     if len(fileName) < len(targetName)+4:
    #         return False
    #     t = 0    
    #     for i in range(len(fileName)):
    #         if t > 0 and fileName[i] != targetName[t]:
    #             t = 0
            
    #         if fileName[i] == targetName[t]:
    #             t += 1
    #             if t == len(targetName):
    #                 return True
    #     return False
    
    def checkForTodaysLogFolder(self, dirName:str)->bool:
        logDir = self.cwd + "\\" + self.logfolderName
        logDirFolders = os.listdir(logDir)
        if dirName in logDirFolders:
            return True
        return False
    
    def createTodaysLogFolder(self)->None:
        self.todaysLogFolderPath = self.logfolderName + "\\" + self.todaysLogFolderName
        try:
            os.mkdir(self.todaysLogFolderPath)
        except FileExistsError:
            logger.info(f"Todays {self.name} log folder already exsist")
            print(f"Todays {self.name} log folder already exsist")

    """
    DEPERECATED
    """
    # def moveOldLogFiles(self, oldLogsPath):
    #     #making my own algo to find the log extensions
    #     for item in self.items:
    #         if self.isLogFile(item) and self.checkForName(item,self.name):
    #             shutil.move(item, oldLogsPath)

    def setupDirectory(self):

        if self.checkForLogFolder():
            self.todaysLogFolderName = self.todaysDate.strftime("date_%m_%d_%Y")
            if not self.checkForTodaysLogFolder(self.todaysLogFolderName):
                self.createTodaysLogFolder()
            self.todaysLogFolderPath = self.logfolderName + "\\" + self.todaysLogFolderName
        else:
            os.mkdir(self.logfolderName)

    def getTodaysLogFolderPath(self):
        if not self.todaysLogFolderPath:
            raise AttributeError("todaysLogFolderPath not set, please makre sure setupDirectory method has been run first")
        return self.todaysLogFolderPath
    
    def extractDate(self, folderName):
        """
        using .split() would be more efficient, but i wanted to write my own function for practice
        """
        m,d,y = None, None, None
        l = 0
        for i, char in enumerate(folderName):
            if i == len(folderName) - 1:
                y = int(folderName[l:])
            if char == '_':
                if l == 0:
                    l = i+1
                else:
                    if m == None:
                        m = int(folderName[l:i])
                        l = i+1
                    else:
                        d = int(folderName[l:i])
                        l = i+1
        return m,d,y                  

    def deleteLogsAfterSetDays(self, maxAgeOfFolder:int)->None:
        """
        TODO:
        need to add a check for bad folder names
        """

        logFolders = os.listdir(self.logfolderName)

        for folder in logFolders:
            m,d,y = self.extractDate(folder)
            daysSinceCreation = calculateDaysSinceAD1(date=self.todaysDate.strftime("%Y_%m_%d")) - calculateDaysSinceAD1(y,m,d)

            if daysSinceCreation >= maxAgeOfFolder:
                try:
                    logger.info(f"DELETING OLD LOG FOLDER: {folder}")
                    shutil.rmtree(f"{self.logfolderName}\\{folder}")
                except FileNotFoundError:
                    logger.info(f"ERROR DELETING {folder}, file not found, ensure running from correct directory")
                        

    

def main():
    log = LogOrganizer("test")
    # # log.checkForLogs()
    # log.setupDirectory()
    # result = None
    # result = log.checkForLogFolder()
    # result = log.checkForName("fyishettityfishfsdsfdffisssshhheefiishfisheherr_log.log","fisher")

    # result = log.checkForTodaysLogFolder("date_06_06_24_time_10_53_logs")
    # result = log.checkForTodaysLogFolder("date_06_06_24_time_10_53_log")
    # print(result)
    # result = log.isLogFile(log)

    # log.deleteLogsAfterSetDays(1)
    log.deleteLogsAfterSetDays(90)
    # m,d,y = log.extractDate("date_06_06_2024")
    # print(m)
    # print(d)
    # print(y)
    # print(result)
    # strftime("date_%m_%d_%y")
    # print(datetime.now().strftime("%Y_%m_%d"))
    
if __name__ == "__main__":
    main()