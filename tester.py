import time
import pyautogui
import numpy as np
import multiprocessing

# def search_color_in_region(region, target_color):
#     im = pyautogui.screenshot(region=region)
#     im_arr = np.array(im)
#     matching_pixels = []
#     for i in range(len(im_arr)):
#         for j in range(len(im_arr[i])):
#             if np.array_equal(im_arr[i][j], target_color):
#                 matching_pixels.append((i + region[0], j + region[1]))  # Adjust coordinates to account for region offset
#     return matching_pixels

# def test_func(region):
#     target_color = (0, 255, 255)
#     color_array = np.array(target_color)
    
#     # Create a multiprocessing Pool
#     num_processes = multiprocessing.cpu_count()
#     pool = multiprocessing.Pool(processes=num_processes)
    
#     # Split the region into smaller chunks
#     screen_width, screen_height = region[2], region[3]
#     chunk_width = screen_width // num_processes
#     regions = [(region[0] + chunk_width * i, region[1], chunk_width, screen_height) for i in range(num_processes)]
    
#     # Apply search_color_in_region function to each region in parallel
#     results = [pool.apply_async(search_color_in_region, (reg, color_array)) for reg in regions]
    
#     # Get the results from each process
#     all_matching_pixels = []
#     for result in results:
#         matching_pixels = result.get()
#         all_matching_pixels.extend(matching_pixels)
    
#     # Close the multiprocessing Pool
#     pool.close()
#     pool.join()
    
#     return all_matching_pixels

# if __name__ == "__main__":
#     # Define the region of the screenshot (left, top, width, height)
#     start_time = time.time()
#     region = (0, 0, 900, 900)
    
#     matching_pixels = test_func(region)
#     print("Matching pixels:", matching_pixels)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(elapsed_time)


def testFunc():
    #im = pyautogui.screenshot(region=(0,0,900,900))
    im = pyautogui.screenshot()
    imArr = np.array(im)
    #print(imArr)

    print(len(imArr))

    # print(imArr[0][0])

    targetColor = (0,255,255)
    colorArray = np.array(targetColor)

    # for i in range(len(imArr)):
    #     for j in range(len(imArr[i])):
    #         if np.array_equal(imArr[i][j], colorArray):
    #             return i, j

    matchingPixel = np.argwhere(np.all(imArr == targetColor, axis=-1))

    print(matchingPixel)
            
start_time = time.time()
testFunc()
end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)