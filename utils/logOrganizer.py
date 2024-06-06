import logging
import os
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

class LogOrganizer():

    def __init__(self, name:str)->None:
        self.name = name
        self.logfolderName = self.name + "-logs"
        self.cwd = os.getcwd()
        self.items = os.listdir(self.cwd)

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
        """
        instead of making a logfolder for each minute, make it for the whole day and rename the files according to their start time.
        """
        if self.checkForLogFolder():
            
            self.todaysDate = datetime.now()
            self.todaysLogFolderName = self.todaysDate.strftime("date_%m_%d_%y")
            if not self.checkForTodaysLogFolder(self.todaysLogFolderName):
                self.createTodaysLogFolder()
            self.todaysLogFolderPath = self.logfolderName + "\\" + self.todaysLogFolderName

            # self.moveOldLogFiles(self.todaysLogFolderPath)

        else:
            os.mkdir(self.logfolderName)

    def getTodaysLogFolderPath(self):
        if not self.todaysLogFolderPath:
            raise AttributeError("todaysLogFolderPath not set, please makre sure setupDirectory method has been run first")
        return self.todaysLogFolderPath
    
    def extractDate(self, folderName):
        #wanted to write my own function to practice my data structures and algorithms instead of using .split()
        m = None
        d = None
        y = None
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

    def deleteLogsAfterSetDays(self, days:int)->None:
        """
        get list of folders
        get date of ea folder
        get date difference
        if older then date deletes folder
        """

        logFolders = os.listdir(self.logfolderName)
        # self.todaysDate

        for folder in logFolders:
            month,day,year = self.extractDate(folder) 

        # print(self.logFolders)

        pass
        


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
    m,d,y = log.extractDate("date_06_06_24")
    print(m)
    print(d)
    print(y)
    # print(result)
    
if __name__ == "__main__":
    main()