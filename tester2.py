from mouseFunctions import Mouse
import os
import time
from verification import Verifyer
from universalMethods import Uni

# def countFiles(folderPath:str):

#     fileCount = 0

#     for _,_, files in os.walk(folderPath):
#         fileCount += len(files)
        
#     return fileCount

# folderPath = "img/salmonBankRunImgs/leftSpot"

# totalFiles = countFiles(folderPath)
# print(totalFiles)
# mouse = Mouse()
# time.sleep(3)
# while True:
#     for i in range(totalFiles):
#         filePath = f"img/salmonBankRunImgs/leftSpot/{i+1}.png"
#         result = mouse.imgMapWalker(filePath, 0.75)
#         print(i+1, result)
#         time.sleep(0.5)
        
# ver = Verifyer


# text = ver.getTextEasyOCR(None,0,0,289,66)
# print(text)

uni = Uni()
time.sleep(3)
verificationText = "Bank Bank Booth"
result = uni.verifyBankBooth(verificationText)
print(result)