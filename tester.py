import time


# def format_time(seconds):

#     seconds = int(seconds)
#     # Calculate hours, minutes, and seconds
#     hours = seconds // 3600
#     seconds %= 3600
#     minutes = seconds // 60
#     seconds %= 60
#     # Format the time as HH:MM:SS
#     formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
#     return formatted_time

# currentTime = time.time()

# print(format_time(currentTime))


current_time = time.time()

# Convert the current time to a local time struct
local_time = time.localtime(current_time)

# Format the local time as a string
time_string = time.strftime("%H:%M:%S", current_time)

print("Current time:", time_string)