import cv2 as cv
import numpy as np
import os
from time import time
import win32gui
import win32ui
import win32con
import pyautogui

# haystack_img = cv.imread('img/testscreenshot.png', cv.IMREAD_UNCHANGED)
# needle_img = cv.imread('img/test.png', cv.IMREAD_UNCHANGED)

# result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# min_val,max_val, min_loc,max_loc = cv.minMaxLoc(result)

# # cv.imshow('Result', result)
# # cv.waitKey()

# # print(max_loc)
# # print(max_val)

# needle_w = needle_img.shape[1]
# needle_h = needle_img.shape[0]

# top_left = max_loc
# botom_right = (top_left[0]+needle_w, top_left[1]+needle_h)

# cv.rectangle(haystack_img, top_left, botom_right,
#                 color=(0,255,0),thickness=2, lineType=cv.LINE_4)

# cv.imshow('Result', haystack_img)


# cv.waitKey()
def window_capture():

    w = 1920
    h = 1080

    #hwnd = None
    windowname = 'Runelite'
    hwnd = win32gui.FindWindow(None, windowname)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (w,h), dcObj, (0,0), win32con.SRCCOPY)

    #save the screenshot
    #dataBitMap.SaveBitmapFile(cDC,'debug.bmp')

    #gets bitMapData ready for return
    signIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signIntsArray, dtype='uint8')
    img.shape = (h,w,4)

    #Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[...,:3]


    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109

    img = np.ascontiguousarray(img)

    return img


loop_time = time()
while True:

    # screenshot = window_capture()
    # #screenshot = np.array(screenshot)
    # # screenshot = screenshot[:,:,::-1].copy()
    # # same as below converts RGB to BGR, BGR being how OpenCv prefers reading images
    # #creenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    # needleImg = cv.imread("img/featherText.bmp", cv.IMREAD_UNCHANGED)

    # result = cv.matchTemplate(screenshot, needleImg, None)

    # # min_val,max_val, min_loc,max_loc = cv.minMaxLoc(result)

    # # print(max_loc)
    # # print(max_val)


    # threshold = 0.8

    # locations = np.where(result >= threshold)
    # print(locations)
    # # print('FPS {}'.format(1 / (time() - loop_time)))
    # # loop_time = time()



    # cv.imshow('Computer Vision', screenshot)

    # if cv.waitKey(1) == ord('q'):
    #     cv.destroyAllWindows
    #     break

    #screenshot = pyautogui.screenshot(region=(0,0, 900,900))
    try:
        for pos in pyautogui.locateAllOnScreen('img/featherText.png',confidence=0.6):
            print(pos)
    except:
        print("...")
        continue


