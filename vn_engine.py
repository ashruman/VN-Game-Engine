import pygame
import sys
import os
from vn_classes import *
from pygame.locals import *
import shelve
pygame.init()
# This is the main file that runs the game.

# create the display screen
screen1 = pygame.display.set_mode((800, 375), RESIZABLE)
fake_screen = screen1.copy()
screen = pygame.surface.Surface((800, 375))

# title screen (displays every time you start the game)
background = pygame.image.load("images/yellowbg.png")
bg = "images/yellowbg.png"
newSize = (800, 375)
screen.blit(background, (0, 0))
new_load = Choice(screen, "Welcome to my game!", ("NEW GAME", "LOAD GAME"), fake_screen, screen1, newSize)
new_load.display()
choose = new_load.selection()

# start a new game
if choose == 0:
    playMusic("briggs.wav")
    currentMusic = "briggs.wav"
    selficon = charaSelect(screen, background)  # ask player to choose character
    nextValue = 1
    courtRecord = []  # inventory
    linkNum = 0
    DONEcount = 0
# load saved game
else:
    if os.path.isfile('saved_game_file.dir') is False:  # file does not exist
        choose = 0
        bg = "images/yellowbg.png"
        background = pygame.image.load("images/yellowbg.png")
        playMusic("briggs.wav")
        currentMusic = "briggs.wav"
        selficon = charaSelect(screen, background)
        nextValue = 1
        courtRecord = []
        linkNum = 0
        DONEcount = 0
    else:
        shelfFile = shelve.open('saved_game_file')
        selficon = shelfFile['selficon']
        currentMusic = shelfFile['currentMusic']
        courtRecord = shelfFile['courtRecord']
        bg = shelfFile['bg']
        nextValue = shelfFile['nextValue']
        d1 = shelfFile['d1']
        d2 = shelfFile['d2']
        shelfFile.close()
        playMusic(currentMusic)

# init text boxes for each character
Chara1 = Textbox(screen, "images/taimir.png", "Character 1")
Chara2 = Textbox(screen, "images/izzyrr.png", "Character 2")
Chara3 = Textbox(screen, "images/caelanr.png", "Character 3")
Chara4 = Textbox(screen, "images/meredithr.png", "Character 4")
Chara5 = Textbox(screen, "images/roryr.png", "Character 5")
Player = Textbox(screen, selficon, "Player")

# game data (inventory, dialogue options, dialogue)
allInventory = {1: ("Apple", 1),
                2: ("Banana", 1),
                3: ("Orange", 1)
                }
choices = {1: ["Change the music?", ["Yes, change it!", "Stop the music.", "Fade out the music.", "Keep playing this song."], [8, 9, 10, 11]],
           2: ("Which item should I look at?", ["n/a", "n/a"], [26, 27, 28, 29])
           }

data = {0: ("MUSIC", "briggs.wav", 1),
        1: (Player, "Hello! Welcome to the VN game engine demo! Let's go over what the program can do. Press enter to advance the dialogue.", 2),
        2: (Player, "(If text is between parentheses, it will display in blue to indicate that the character is thinking...)", 3),
        3: (Player, "Cool, right? Don't you agree, other characters?", 4),
        4: (Player, "(A quick note: one of the characters in this demo will have the same icon as me. This is not a bug, there's just only 5 character portraits in this demo game.)", 5),
        5: (Chara1, "I agree.", 6),
        6: (Chara2, "So do I. Can I change the music, though?", 7),
        7: (Player, "(Should I let them change the music...?)", "CHOICE", 1),
        8: ("MUSIC", "Tolbi.wav", 11),
        9: ("MUSIC", "STOP", 11),
        10: ("MUSIC", "FADE", 11),
        11: (Player, "See, you can let the player choose different options, and control the background music.", 12),
        12: (Player, "By the way, you can also use sound effects (without turning off the music). Let's play one right now. Are you ready? 3...2...1...", 13),
        13: ("SFX", shockNoise, 14),
        14: (Player, "You can also make the screen fade to black and then back in.", 15),
        15: ("FADE", "n/a", 16),
        16: (Player, "See? You can also use this to transition between different backgrounds. Let's do that now.", 17),
        17: ("FADE", "images/bluebg.png", 18),
        18: (Player, "Nice. Now let's demo the inventory system. We'll collect some items from other characters.", 19),
        19: (Chara3, "Hi! Here's an apple.", 20),
        20: ("CR", 1, 21),
        21: (Chara4, "Have a banana.", 22),
        22: ("CR", 2, 23),
        23: (Chara5, "And here's an orange.", 24),
        24: ("CR", 3, 25),
        25: (Player, "Now I have all the items! Let's open the inventory.", "ECHOICE", 2),
        "DONE": [Player, "I already looked at that.", "CHOICE", 2],
        26: (Player, "This is the apple.", 29),
        27: (Player, "This is the banana.", 29),
        28: (Player, "This is the orange.", 29),
        29: (Player, "That about covers the main features. Thanks for playing!", 30),
        30: ("FADE", "images/blackbg.png", 31),
        31: ("B")
        }

d1 = data["DONE"][1]
d2 = data["DONE"][3]

# resizeable display
oldSize = pygame.Surface.get_size(screen1)
newSize = oldSize
# keep track of dialogue
data["DONE"][1] = d1
data["DONE"][3] = d2

# set up variables
background = pygame.image.load(bg)
gameLoop = True
pygame.display.set_caption("VN ENGINE DEMO")

# main game loop
while gameLoop:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    mus = False
    # progress to next dialogue/action
    position = data[nextValue]
# inventory access flag
    if position[0] == "CR":
        item = allInventory[position[1]]
        ev = Evidence(screen, item[0], item[1], fake_screen, screen1, newSize)
        ev.receive()
        courtRecord.append([item])
        nextValue = position[2]
# fade to black/possibly change background
    elif position[0] == "FADE":
        fadeout(screen, fake_screen, screen1, newSize)
        if position[1] != "n/a":
            background = pygame.image.load(position[1])
            bg = position[1]
        fadein(screen, background, fake_screen, screen1, newSize)
        nextValue = position[2]
        continue

# music controls
    elif position[0] == "MUSIC":
        mus = True
        if position[1] == "STOP":
            stopMusic()
        elif position[1] == "FADE":
            fadeMusic()
        else:
            currentMusic = position[1]
            playMusic(position[1])
        nextValue = position[2]
        continue
# sound effect flag
    elif position[0] == "SFX":
        mus = True
        SFX(position[1])
        nextValue = position[2]
        continue
    elif position[0] == "B":
        break
# regular dialogue is the default
    else:
        position[0].draw()
        text = Dialogue(screen, position[1], fake_screen, screen1, newSize)
        text.write()

    if mus is False:
        event = pygame.event.wait()
        while event.type != KEYDOWN:
            # autosave game on quit
            if event.type == pygame.QUIT:
                shelfFile = shelve.open('saved_game_file')
                shelfFile['currentMusic'] = currentMusic
                shelfFile['selficon'] = selficon
                shelfFile['courtRecord'] = courtRecord
                shelfFile['bg'] = bg
                shelfFile['nextValue'] = nextValue
                shelfFile['d1'] = d1
                shelfFile['d2'] = d2
                shelfFile.close()
                sys.exit()
            # resizable window
            elif event.type == VIDEORESIZE:
                newSize = event.dict['size']
                if newSize[0] != oldSize[0]:
                    scaleFactor = newSize[0]/oldSize[0]
                else:
                    scaleFactor = newSize[1]/oldSize[1]
                newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
                screen1 = pygame.display.set_mode(newSize, RESIZABLE)
                fake_screen.blit(screen, (0, 0))
                screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0)) 
                pygame.display.flip()
                oldSize = newSize
            event = pygame.event.wait()
            continue
# dialogue selection flag
    if position[2] == "CHOICE":
        screen.blit(background, (0, 0))
        cPosition = choices[position[3]]
        choiceData = Choice(screen, cPosition[0], cPosition[1], fake_screen, screen1, newSize)
        choiceData.display()
        pygame.display.flip()
        linkNum = 0
        for link in cPosition[2]:
            if link == "DONE":
                linkNum = linkNum + 1
        if linkNum == len(cPosition[1]):            
            nextValue = cPosition[2][-1]
            continue
        # go to the next piece of dialogue after completing all the options
        pos = choiceData.selection()
        nextValue = cPosition[2][pos]
        cPosition[2][pos] = "DONE"
# inventory selection flag
    elif position[2] == "ECHOICE":
        screen.blit(background, (0, 0))
        cPosition = choices[position[3]]
        CR = []
        for item in courtRecord:
            name = item[0][0]
            CR.append(name)
        choiceData = Choice(screen, cPosition[0], CR, fake_screen, screen1, newSize)
        choiceData.display()
        pygame.display.flip()
        p = choiceData.selection()
        nextValue = cPosition[2][p]

    else:
        if position[0] != "CR":
            nextValue = position[2]

    screen1 = pygame.display.set_mode(newSize, RESIZABLE)
    fake_screen.blit(screen, (0, 0))
    screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
    pygame.display.flip()

# quit game
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
