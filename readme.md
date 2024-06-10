# Fern's Colorborg

ColorBorg is an automation platform for Old School RuneScape. Instead of using injection to interact with the game, ColorBorg employs a mix of color detection, image recognition, optical character recognition(OCR), and a local API to navigate the game successfully. The platform is developed in Python with a focus on modularity and ban evasion. Throughout its development, I designed the bot to mimic human behavior, enhancing its natural appearance and reducing the risk of detection.

Due to recent changes, running the bot requires building a custom version of RuneLite with [slyautomation's HTTP plug](https://github.com/slyautomation/httpplug). [This video guide](https://www.youtube.com/watch?v=ldfJfNhXKhI) by SlyAutomation explains the process. Ensure the HTTP server points to port 8081, or adjust it in the source code. For Jagex account users, follow [this guide](https://github.com/runelite/runelite/wiki/Using-Jagex-Accounts) by RuneLite. Visit [colorborg.com](https://www.colorborg.com/) for more information about this project and me.

## Features
    - Human like mouse movements, using Bezier curves
    - Fully Stable F2P fishing scripts(shrimp, Barbarian Village Fly Fisher)
    - Detailed Logging
    - Info GUI
    - Break System
    - Walker
    - Banking
    - To Come: Random Event Handling, and finished chicken killer to fuel all your fly fishing needs

## Instructions

Currently, ColorBorg only works on Windows with a minimum 1080p screen resolution. It is recommended to run the bot on a virtual machine (VM) as it takes full control of your mouse.

1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your system's PATH.
2. Ensure your character is at the respective skilling spots.
3. If not using a Jagex account, log in beforehand.
4. Run `python main.py` to start the bot.

## Going forward

Due to recent changes in RuneLite's plugin hub, which removed the plugin I relied on, the accessibility of the program has decreased. This has deterred me from further expanding the bot. I will focus on completing major goals like random event handling before potentially pausing development. 

## Road Map: Before Abandonment

1. Add random event handling
2. Complete chicken killer script
3. Add instructions for setting up built-in plugins for the random event handler and chicken killer
4. Upload videos of the scripts running
5. Create a software diagram

## Random Event NPC Names to highlight
Below is a list of all the RandomEvent NPCs That will need to be highlighted

    Bee Keeper, Capt' Arnav, Niles, Miles, Giles, Count Check, Sergeant Damient, Drunken dwarf, Evil Bob, Servant, Postie Pete, Molly,, Freaky Forester, Genie, Leo, Dr Jekyll, Prince, Princess, Mysterious Old Man, Flippa, Tilt, Quiz Master, Rick Turpentine, Sandwich Lady, Strange Plant,
    Dunce, Mr. Mordaut
