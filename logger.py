import logging
import os
import shutil
from datetime import datetime

class Logger():

    def __init__(self, name):

        self.name = name
        self.logfolderName = self.name + "-logs"
        cwd = os.getcwd()
        self.items = os.listdir(cwd)

    def checkForLogFolder(self):

        if self.logfolderName in self.items:
            return True
        else:
            return False
        
    def createOldLogsFolder(self)->str:
        currentDate = datetime.now()
        newFolderName = currentDate.strftime("date_%m_%d_%y_time_%H_%M_logs")

        if not self.checkForLogFolder():
            os.mkdir(self.logfolderName)

        mkNewFolderPath = self.logfolderName + "/" + newFolderName

        try:
            os.mkdir(mkNewFolderPath)
            return mkNewFolderPath
        except FileExistsError:
            return mkNewFolderPath
    
    def isLog(self, fileName):
        for i, char in enumerate(fileName):
            if char == '.':
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
    
    def moveOldLogFiles(self, oldLogsPath):
        #making my own algo to find the log extensions
        for item in self.items:
            if self.isLog(item):
                shutil.move(item, oldLogsPath)

    def setupDirectory(self):
        if self.checkForLogs():
            newDirPath = self.createOldLogsFolder()
            self.moveOldLogFiles(newDirPath)
        elif not self.checkForLogFolder():
            os.mkdir(self.logfolderName)

    def createLogger(self):
        self.logger = logging.getLogger(self.name + "_log")
        self.logger.setLevel(logging.DEBUG)


    def createDebugHandler(self):
        self.debugHandler = logging.FileHandler(self.name+"_debug.log")
        self.debugHandler.setLevel(logging.DEBUG)
        debugForm = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        self.debugHandler.setFormatter(debugForm)
        self.logger.addHandler(self.infoHandler)
    
    def createInfoHandler(self):
        self.infoHandler = logging.FileHandler(self.name+"_info.log")
        self.infoHandler.setLevel(logging.INFO)
        infoFormatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        self.infoHandler.setFormatter(infoFormatter)
        self.logger.addHandler(self.infoHandler)

    def createErrorHandler(self):
        self.errorHandler = logging.FileHandler(self.name+"_error.log")
        self.errorHandler.setLevel(logging.ERROR)
        errorFormatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        self.errorHandler.setFormatter(errorFormatter)
        self.logger.addHandler(self.errorHandler)

    """
    check for previous log files
    if they exsist move them into a new folder and arrange by date
    create loggers
    set logging levels
    """

def main():
    log = Logger("Fisher")
    # log.checkForLogs()
    log.setupDirectory()
    log.createLogger()
    log.createInfoHandler()
    log.createErrorHandler()
    log.logger.info("This is an info message")
    log.logger.error("This is an error message")
    log.logger.debug("DEBUG THIS BITCH")
    log.logger.error("why am i showing up in info")
    log.logger.info("am i showing up in error?")

if __name__ == "__main__":
    main()