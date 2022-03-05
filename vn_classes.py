import pygame
from pygame.locals import *

offset_col = (91, 79, 107)
highlight = (11, 175, 151)

# create sfx
pygame.mixer.init()
getNoise = pygame.mixer.Sound("music/get.wav")
shockNoise = pygame.mixer.Sound("music/surprise.wav")


# CLASSES
# textbox object to display dialogue on
class Textbox ():
    def __init__(self, screen, icon, name):
        self.screen = screen
        self.icon = pygame.image.load(icon)
        self.name = name

    # draw textbox
    def draw(self):
        # draw textbox shape
        box = Rect(208, 131, 458, 175)
        border = Rect(215, 138, 444, 161)
        pygame.draw.rect(self.screen, (58, 120, 156), box)
        pygame.draw.rect(self.screen, (255, 255, 255), border, 2)
        # draw box for icon
        box2 = Rect(142, 61, 140, 140)
        border2 = Rect(149, 68, 126, 126)
        pygame.draw.rect(self.screen, offset_col, box2)
        pygame.draw.rect(self.screen, (255, 255, 255), border2, 2)
        # draw icon
        self.screen.blit(self.icon, (160, 78))
        # add name
        # set up text/font
        font = pygame.font.Font("images/font.ttf", 18)
        text = font.render(self.name + ":", True, (255, 255, 255))
        textRect = text.get_rect()
        text_width, text_height = font.size(self.name)
        textRect.center = (300+text_width/2, 162) 
        # display name
        self.screen.blit(text, textRect)
        # draw a line under the name
        pygame.draw.line(self.screen, (255, 255, 255), (290, 180), ((310+text_width), 180), 3)


class Dialogue:
    def __init__(self, screen, words, fake_screen, screen1, newSize):
        self.words = words
        self.screen = screen
        self.fake_screen = fake_screen
        self.screen1 = screen1
        self.newSize = newSize
        
        # create font
        font = pygame.font.Font("images/font.ttf", 14)
        self.font = pygame.font.Font("images/font.ttf", 14)
        # set size, split by word
        text_width, text_height = font.size(self.words)
        self.height = text_height
        self.wordList = words.split(" ")
        i = 0
        newWords = ""
        self.lines = []
        
        while i < len(self.wordList):
            newWords = newWords + " " + self.wordList[i]
            newWidth, newHeight = font.size(newWords)
            if newWidth > 400:
                lastWordList = newWords.split(" ")
                lastWord = len(lastWordList)
                del lastWordList[lastWord-1]
                newWords = ""
                for word in lastWordList:
                    newWords = newWords + " " + word
                self.lines.append(newWords)
                i = i-1
                newWords = ""
            i = i+1
        self.lines.append(" "+newWords)

# write dialogue
    def write(self):
        index = 0
        # detect if dialogue is spoken (printed in white) or thought (printed in blue)
        if self.lines[0][2] == "(":
            col = (88, 227, 237)
        else:
            col = (255, 255, 255)
            
        # have text appear letter by letter
        for line in self.lines:
            for i in range(len(line)):
                letter = self.font.render(line[i], True, col)
                self.screen.blit(letter, Rect((230 + self.font.size(line[:i])[0]), 210+self.height*1.5*index, 208, self.height))
                self.fake_screen.blit(self.screen, (0, 0))
                self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))
                pygame.display.update()
                # pause longer after ending a sentence
                if line[i] == "." or line[i] == "!" or line[i] == "?":
                    pygame.time.wait(200)
                else:
                    pygame.time.wait(50)
            index = index + 1


class Choice:
    def __init__(self, screen, choice, options, fake_screen, screen1, newSize):
        self.screen = screen
        self.choice = choice
        self.options = options
        self.boxes = []
        self.texts = []
        self.fake_screen = fake_screen
        self.screen1 = screen1
        self.newSize = newSize
    
    def display(self):
        font = pygame.font.Font("images/font.ttf", 16)
        # box for choice
        choiceBox = Rect(200, 0, 400, 40)
        pygame.draw.rect(self.screen, offset_col, choiceBox)
        # choice text
        choiceText = font.render(self.choice, True, (255, 255, 255))
        text_width, text_height = font.size(self.choice)
        cTextbox = Rect(0, 0, text_width, text_height)
        cTextbox.center = (400, 20)
        self.screen.blit(choiceText, cTextbox)
        # box for each option
        i = 1
        for option in self.options:
            optionbox = Rect(200, 65*i, 400, 40)
            pygame.draw.rect(self.screen, (58, 120, 156), optionbox)
            self.boxes.append(optionbox)
            # options text
            oText = font.render(option, True, (255, 255, 255))
            text_width, text_height = font.size(option)
            # box around option
            oTextbox = Rect(0, 0, 0, 0)
            oTextbox.center = (400-(text_width/2), (65*i)+(text_height/2+4))
            self.screen.blit(oText, oTextbox)
            self.texts.append((oText, oTextbox))
            i = i + 1
    
# go through options
    def selection(self):
        pos = 0
        s = False
        oldSize = self.newSize
        pygame.draw.rect(self.screen, highlight, self.boxes[pos])
        self.screen.blit(self.texts[pos][0], self.texts[pos][1])
        self.fake_screen.blit(self.screen, (0, 0))
        self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))
        pygame.display.flip()

        while s is False:
            for event in pygame.event.get():
                # resize screen event
                if event.type == VIDEORESIZE:
                    self.newSize = event.dict['size']
                    if self.newSize[0] != oldSize[0]:
                        scaleFactor = self.newSize[0]/oldSize[0]
                    else:
                        scaleFactor = self.newSize[1]/oldSize[1]
                    self.newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
                    self.screen1 = pygame.display.set_mode(self.newSize, RESIZABLE)
                    self.fake_screen.blit(self.screen, (0, 0))
                    self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))  # event.dict['size']
                    pygame.display.flip()
                    oldSize = self.newSize
                # press enter event
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RETURN:
                        s is True
                        return pos
                    
                    elif event.key == K_DOWN:
                        # erase highlight on current box
                        pygame.draw.rect(self.screen, (58, 120, 156), self.boxes[pos])
                        self.screen.blit(self.texts[pos][0], self.texts[pos][1])
                        if pos + 1 > (len(self.boxes)-1):
                            pos = 0
                        else:
                            pos = pos + 1
                        # highlight new box
                        pygame.draw.rect(self.screen, highlight, self.boxes[pos])
                        self.screen.blit(self.texts[pos][0], self.texts[pos][1])
                        self.fake_screen.blit(self.screen, (0, 0))
                        self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))
                        pygame.display.flip()

                    elif event.key == K_UP:
                        # erase highlight on current box
                        pygame.draw.rect(self.screen, (58, 120, 156), self.boxes[pos])
                        self.screen.blit(self.texts[pos][0], self.texts[pos][1])
                        if pos - 1 < 0:
                            pos = (len(self.boxes)-1)
                        else:
                            pos = pos - 1
                            
                        # highlight new box
                        pygame.draw.rect(self.screen, highlight, self.boxes[pos])
                        self.screen.blit(self.texts[pos][0], self.texts[pos][1])
                        self.fake_screen.blit(self.screen, (0, 0))
                        self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))
                        pygame.display.flip()


# inventory items
class Evidence:
    def __init__(self, screen, name, desc, fake_screen, screen1, newSize):
        self.name = name
        self.desc = desc
        self.screen = screen
        self.fake_screen = fake_screen
        self.screen1 = screen1
        self.newSize = newSize
    
    def receive(self):
        # draw box
        box = Rect(100, 167, 600, 40)
        pygame.draw.rect(self.screen, (58, 120, 156), box)
        
        # text
        font = pygame.font.Font("images/font.ttf", 16)
        string = self.name + " acquired!"
        text = font.render(string, True, (255, 255, 255))
        text_width, text_height = font.size(string)
        textbox = Rect(0, 0, 0, 0)
        textbox.center = (400-(text_width/2), 167 + (text_height/2+4))
        self.screen.blit(text, textbox)
        self.fake_screen.blit(self.screen, (0, 0))
        self.screen1.blit(pygame.transform.scale(self.fake_screen, self.newSize), (0, 0))
        pygame.display.flip()
        pygame.mixer.Sound.play(getNoise)


# fade effect (out)
def fadeout(screen, fake_screen, screen1, newSize):
    surface = pygame.Surface((800, 375))
    surface.fill((0, 0, 0))
    for a in range(0, 50):
        surface.set_alpha(a)
        screen.blit(surface, (0, 0))
        screen1 = pygame.display.set_mode(newSize, RESIZABLE)
        fake_screen.blit(screen, (0, 0))
        screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
        pygame.display.flip()
        pygame.time.wait(30)


# fade effect (in)
def fadein(screen, background, fake_screen, screen1, newSize):
    surface = pygame.Surface((800, 375))
    surface.fill((0, 0, 0))
    for a in range(-300, 0):
        surface.set_alpha(-a)
        screen.blit(background, (0, 0))
        screen.blit(surface, (0, 0))
        screen1 = pygame.display.set_mode(newSize, RESIZABLE)
        fake_screen.blit(screen, (0, 0))
        screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)


# character selection
def charaSelect(screen, background):
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0,))
    fake_screen = screen.copy()
    screen = pygame.surface.Surface((800, 375))
    screen.blit(background, (0, 0))
    oldSize = (800, 375)
    newSize = (800, 375)
    # box
    pygame.font.init()
    font = pygame.font.Font("images/font.ttf", 16)
    choiceBox = Rect(200, 0, 400, 40)
    pygame.draw.rect(screen, offset_col, choiceBox)
    # text
    choiceText = font.render("Choose your fighter!", True, (255, 255, 255))
    text_width, text_height = font.size("Choose your fighter!")
    cTextbox = Rect(0, 0, text_width, text_height)
    cTextbox.center = (400, 20)
    screen.blit(choiceText, cTextbox)

    # characters
    roryBox = Rect(191, 70, 140, 140)
    pygame.draw.rect(screen, offset_col, roryBox)
    ricon = pygame.image.load("images/roryr.png")
    rpos = (208, 87)
    screen.blit(ricon, rpos)

    mereBox = Rect(347, 70, 140, 140)
    pygame.draw.rect(screen, offset_col, mereBox)
    micon = pygame.image.load("images/meredithr.png")
    mpos = (364, 87)
    screen.blit(micon, mpos)
    
    izzyBox = Rect(503, 70, 140, 140)
    pygame.draw.rect(screen, offset_col, izzyBox)
    iicon = pygame.image.load("images/izzyrr.png")
    ipos = (520, 87)
    screen.blit(iicon, ipos)
    
    caeBox = Rect(269, 226, 140, 140)
    pygame.draw.rect(screen, offset_col, caeBox)
    cicon = pygame.image.load("images/caelanr.png")
    cpos = (286, 243)
    screen.blit(cicon, cpos)
    
    taimiBox = Rect(425, 226, 140, 140)
    pygame.draw.rect(screen, offset_col, taimiBox)
    ticon = pygame.image.load("images/taimir.png")
    tpos = (442, 243)
    screen.blit(ticon, tpos)
    
    charas = ((roryBox, ricon, rpos), (mereBox, micon, mpos), (izzyBox, iicon, ipos), (caeBox, cicon, cpos), (taimiBox, ticon, tpos))
    icons = ("images/roryr.png", "images/meredithr.png", "images/izzyrr.png", "images/caelanr.png", "images/taimir.png")
    pos = 0
    s = False
    # draw boxes to screen
    pygame.draw.rect(screen, highlight, charas[pos][0])
    screen.blit(charas[pos][1], charas[pos][2])
    screen1 = pygame.display.set_mode(newSize, RESIZABLE)
    fake_screen.blit(screen, (0, 0))
    screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
    pygame.display.flip()
    
    while s is False:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newSize = event.dict['size']
                if newSize[0] != oldSize[0]:
                    scaleFactor = newSize[0]/oldSize[0]
                else:
                    scaleFactor = newSize[1]/oldSize[1]
                newSize = (int(oldSize[0]*scaleFactor), int(oldSize[1]*scaleFactor))
                screen1 = pygame.display.set_mode(newSize, RESIZABLE)
                fake_screen.blit(screen, (0, 0))
                screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
                
            elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    s is True
                    return icons[pos]
                
                elif event.key == K_RIGHT:
                    # erase highlight on current box
                    pygame.draw.rect(screen, offset_col, charas[pos][0])
                    screen.blit(charas[pos][1], charas[pos][2])
                    if pos + 1 > (len(charas)-1):
                        pos = 0
                    else:
                        pos = pos + 1
                    # highlight new box
                    pygame.draw.rect(screen, highlight, charas[pos][0])
                    screen.blit(charas[pos][1], charas[pos][2])
                    pygame.display.flip()
                    
                elif event.key == K_LEFT:
                    # erase highlight on current box
                    pygame.draw.rect(screen, offset_col, charas[pos][0])
                    screen.blit(charas[pos][1], charas[pos][2])
                    if pos - 1 < 0:
                        pos = len(charas)-1
                    else:
                        pos = pos - 1
                    # highlight new box
                pygame.draw.rect(screen, highlight, charas[pos][0])
                screen.blit(charas[pos][1], charas[pos][2])
                screen1 = pygame.display.set_mode(newSize, RESIZABLE)
                fake_screen.blit(screen, (0, 0))
                screen1.blit(pygame.transform.scale(fake_screen, newSize), (0, 0))
                pygame.display.flip()


# music/sfx commands
def playMusic(file):
    pygame.mixer.music.load("music/" + file)
    pygame.mixer.music.play(-1)


def fadeMusic():
    pygame.mixer.music.fadeout(1700)


def stopMusic():
    pygame.mixer.music.stop()


def SFX(sound):
    pygame.mixer.Sound.play(sound)
