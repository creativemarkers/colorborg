# Fern's Ultimate Colorbot


#### I CHANGED THE PYAUTOGUI MINIMUM ITS LOWER NOW CAN CAUSE UNEXPECTED BEHAVIOR NEEDS TESTING, time between clicks is too damn high

# Instructions
    1. Open runelite and have your login details saved
    2. make sure at desired botting location
    3. make sure the necessary runelite plugins are turned on (run plugin checker, doesn't exsist yet)
    4. Run main.py from command line

# Install Instructions

1) install tesseract OCR to path if not done manually?
    could add a verification step on exe?
    https://github.com/tesseract-ocr/tesseract
    https://github.com/UB-Mannheim/tesseract/wiki
2) once tesseract is installed add it's file path, to system PATH in windows


# RuneLite Extension
    -Required
1) Morg HTTP Client
    creates a local api end point
    localhost:8081
    make sure to allow it on the firewall

# Road Map

these will be in no particular order

0) ~~fully stable fisher~~
1) Website for clients to log in and download the bot
2) fleshed out database to auth my users and check licenses (sql, apache, azure hosted)
3) fully working f2p fisher, in theory get you to 1-99 fishing on f2p, with full ban evasion
4) include ~~shrimp~~, ~~trout/salmon~~, anglerfish
5) ~~walker~~
5.5) pathfinding
6) ~~bank~~ - semi done, will need to fully test once a script actually needs to do it (anglerfish)
7) instructions on how to setup the bot (runelite plugins mostly)
8) nice looking gui, include pause and play button, as well as stop. 
9) automatic tesseract install 
10) can take extended break(for ban evasion)
11) f2p miner
12) f2p woodcutter

20) real strecth goal: is to incorporate bezier curves for mouse movements

# TO-DO
0) MORE BAN EVASION
   * RANDOM POWER DROPPER 
        - make it seem like it was user was afk before powerdropping mean of 5-10 seconds
        - need to make it misclick
        - follow a pattern but it be random kinda of 
  
   * ADD MISSED CLICKS
   * ADD MORE ROBUST CAMERA MOVEMENTS
   * RANDOM ZOOM INS?

    # needs more testing
   * MULTIPLE MOUSE CLICKS
        - first implementation done, along with more robost verification if fishing
   * MOVE MOUSE OFF CLIENT TO SIMULATE AFK
        - implemented
   * Better detection of objects (start from center of player then move outwards)
        - implemented new image finder that looks for images from center of character
   * BETTER BREAK SYSTEM maybe based on timezone
        * AFK LOGOUTS
   * RIGHT CLICK OCCASSIONALY
        - right click now implemented if first verification of text fails, might do it too frequently
        - shrimper needs to be updated with right click tech
    
1) ~~Random stat checker~~
    * BETTER STAT CHECKER
2) ~~LOGOUT FUNCTION add the logged in checker to the logout function~~
3) ~~auto sleep for ban evasion~~
4) script to install all my dependency on new machines
5) notification ping if bot fails or gets stuck (prob would need to count fishes)
6) GUI popup for fatal errors if user error inform user


# PRIORITY


-finish the website
-add more ban evasion
-loginer doesn't account for f2p or members world
-hasbait isn't destroying the the gui properly due to root.destroy killing everything in it's tracks


# Random Event NPC Names to highlight
    Bee Keeper, Capt' Arnav, Niles, Miles, Giles, Count Check, Sergeant Damient, Drunken dwarf, Evil Bob, Servant, Postie Pete, Molly,, Freaky Forester, Genie, Leo, Dr Jekyll, Prince, Princess, Mysterious Old Man, Flippa, Tilt, Quiz Master, Rick Turpentine, Sandwich Lady, Strange Plant,
    Dunce, Mr. Mordaut
