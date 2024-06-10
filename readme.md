# Fern's Colorborg

ColorBorg is an automation platform for Old School RuneScape. Instead of using injection to interact with the game, ColorBorg employs a mix of color detection, image recognition, optical character recognition(OCR), and a local API to navigate the game successfully. The platform is developed in Python with a focus on modularity and ban evasion. Throughout its development, I designed the bot to mimic human behavior, enhancing its natural appearance and reducing the risk of detection.

Unfortunately running the bot isn't as simple as opening an exe, due to runelite removing the plugin i was relying on from the plugin hub. Inorder to now run the bot you will need to build your own version of runelite with [slyautomation's http plug](https://github.com/slyautomation/httpplug). Here's a [video guide](https://www.youtube.com/watch?v=ldfJfNhXKhI) by sly himself on how to do it. Once you build your own version of runelite with his plugin makesure to change his http server to point to port 8081, or change it in my sourcecode. Once you've done that you're ready to follow the rest of the instructions below. If you're using a jagex account make sure to follow this guide provided by [runelite](https://github.com/runelite/runelite/wiki/Using-Jagex-Accounts). To learn more about this project and me please head to [colorborg.com](https://www.colorborg.com/)

# Features
    -Human like mouse movements, using bezier curves
    -Fully Stable F2P fishing scripts(shrimp, Barbarian Village Fly Fisher)
    -Detailed Logging
    -Info GUI
    -Break System
    -Walker
    -Banking
    -To Come: Random Event Handling, and finished chicken killer to fuel all your fly fishing needs

# Instructions

    Currently only works on windows, and a minimum a 1080p screen.
    The bot does take full control of your mouse it is reccomended to run it on
    a VM

    1) install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) to your systems PATH folder
    2) Make sure you're character is at the respective skilling spots
    3) If you're not using a jagex account, make sure to already be logged in
    4) Run 'python main.py' and the bot should begin.

# Going forward
Due to the major change in runelites pluginhub(removing the plugin i was relying on) and by proxy the accessability of the program, it has deterred me heavily from truly expanding and working on the bot any further. Besides finishing some of the major goals like random event handling. I will more then likely abandon the project for a while until i find motivation again to continue working on it.

# Road Map: Before Abandonment
1) add random event handler
2) finish chicken killer
3) add instructions how to setup the built in plugins for random event handler and the chicken killer
4) software diagram

# Random Event NPC Names to highlight
    Below is a list of all the RandomEvent NPCs That will need to be highlighted

    Bee Keeper, Capt' Arnav, Niles, Miles, Giles, Count Check, Sergeant Damient, Drunken dwarf, Evil Bob, Servant, Postie Pete, Molly,, Freaky Forester, Genie, Leo, Dr Jekyll, Prince, Princess, Mysterious Old Man, Flippa, Tilt, Quiz Master, Rick Turpentine, Sandwich Lady, Strange Plant,
    Dunce, Mr. Mordaut
