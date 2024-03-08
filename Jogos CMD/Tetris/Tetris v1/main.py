# -*- coding: utf-8 -*-
import keyboard
from math import ceil
from time import sleep
from random import choice, randint
from os import system, get_terminal_size
#import pygame
#pygame.init()

class Piece():
    def __init__(self,string):
        self.shape = string
        self.Pos = 0
        self.deb = False

        self.pls = self.shape.splitlines()
        self.width = checkLargest(self.pls)
        self.height = len(self.pls)
        self.spacing = randint(0,(gameWidth-2)-self.width)

    def update(self):
        self.pTopPos = self.Pos - ceil(self.height / 2)
        self.pBottomPos = self.Pos + ceil(self.height / 2)

        #self.deb = not self.deb
        #if self.deb:
        #    self.Pos += 1

        if keyboard.is_pressed("s"):
            self.Pos += 1

        if len(listOfPieces) > 0:
            overlapL,overlapR = False, False
            for p in listOfPieces:
                a,b = checkOverlap(p)
                if not overlapL and a:
                    overlapL = a
                
                if not overlapR and b:
                    overlapR = b

            #print("L: " + str(overlapL))
            #print("R: " + str(overlapR))
        
            if (keyboard.is_pressed('a') and self.spacing > 0) and not overlapL:
                self.spacing -= 1
            elif (keyboard.is_pressed('d') and self.spacing < ((gameWidth-2) - self.width)) and not overlapR:
                self.spacing += 1
        else:
            if (keyboard.is_pressed('a') and self.spacing > 0):
                self.spacing -= 1
            elif (keyboard.is_pressed('d') and self.spacing < ((gameWidth-2) - self.width)):
                self.spacing += 1

class Line():
    def __init__(self,id,string,piecesOnLine):
        self.lineId = id
        self.string = string
        self.containingPieces = {}

        for piece in piecesOnLine:
            for ls,content in enumerate(piece.pls):
                pTopPos = piece.Pos - ceil(piece.height / 2)
                if pTopPos + ls == self.lineId:
                    self.containingPieces[piece] = [ls,removeLineBreaks(content)]



FPS = 10
listOfPieces = []
listOfLines = {}
groundLevel = 15
gameWidth = 20
gameHeight = groundLevel + 2
currentPiece = None
points = 0
lines = 0

pSymbol = '■'
leftup = '╔'
rightup = '╗'
leftdown = '╚'
rightdown = '╝'
horizontalline = '═'
verticalline = '║'

pieceBlueprints = [
    '***\n***',
    '**\n**',
    '***\n***\n***',
    #'*',
    '*\n*'
]

def checkLargest(pls):
    largest = 0
    for ls in pls:
        ls = removeLineBreaks(ls)
        if len(ls) > largest:
            largest = len(ls)

    return largest

def removeLineBreaks(s):
    return ''.join(s.splitlines())

def checkOverlap(p):
    overlapL = currentPiece.spacing <= p.spacing + p.width and currentPiece.spacing + currentPiece.width >= p.spacing + p.width
    overlapR = currentPiece.spacing + currentPiece.width >= p.spacing and currentPiece.spacing <= p.spacing
    overlapY = currentPiece.Pos > p.Pos - p.height and currentPiece.Pos < p.Pos + p.height

    if not overlapY:
        overlapL = False
        overlapR = False

    return overlapL,overlapR

def onLineFilled(line):
    global points, lines
    points += gameWidth - 2
    lines += 1
    for piece,info in line.containingPieces.items():
        pTopPos = piece.Pos - ceil(piece.height / 2)
        pBottomPos = piece.Pos + ceil(piece.height / 2)
        if line.lineId >= pTopPos and line.lineId <= pBottomPos:
            s = piece.shape.splitlines()
            for index,_ in enumerate(s):
                if index == info[0]:
                    s.pop(index)
            
            newShape = ''
            for shape in s:
                newShape += shape

            piece.shape = newShape

    for _,l in listOfLines.items():
        if l.lineId < line.lineId:
            for piece,_ in l.containingPieces.items():
                piece.Pos += 1


def formPiece():
    global currentPiece
    currentPiece = Piece(choice(pieceBlueprints).replace('*',pSymbol))
    #pieceColors[currentPiece] = choice(colors)

def processGame():
    for line in range(gameHeight):
        toRender = ''
        allPieces = listOfPieces.copy()
        objectsOrderedFromLeftToRight = []
    
        if currentPiece != None:
            allPieces.append(currentPiece)

            sorted = []
            for otherPiece in allPieces:
                sorted.append(otherPiece.spacing)

            sorted.sort()

            for spacingNumber in sorted:
                for otherPiece in allPieces:
                    if spacingNumber == otherPiece.spacing and not otherPiece in objectsOrderedFromLeftToRight:
                        objectsOrderedFromLeftToRight.append(otherPiece)

            piecesOnLine = []
            # lastOnLine = None
            # for p in objectsOrderedFromLeftToRight:
            #     if line >= p.pTopPos and line <= p.pBottomPos: # piece is on this line?
            #         piecesOnLine.append(p)
            #         for ls,content in enumerate(p.pls):
            #             content = removeLineBreaks(content)
            #             if p.pTopPos + ls == line:
            #                 if lastOnLine != None:
            #                     toRender += (' ' * abs(p.spacing - len(toRender))) + content
            #                 else:
            #                     toRender += (' ' * p.spacing) + content
            #                 lastOnLine = p

            lastOnLine = None
            for p in objectsOrderedFromLeftToRight:
                pTopPos = p.Pos - ceil(p.height / 2)
                pBottomPos = p.Pos + ceil(p.height / 2)
                if line >= pTopPos and line <= pBottomPos:
                    piecesOnLine.append(p)
                    pls = p.shape.splitlines()
                    for ls in range(1,len(pls)+1):
                        content = removeLineBreaks(pls[ls-1])
                        if pTopPos + ls == line:
                            if lastOnLine != None:
                                toRender += (' ' * abs(p.spacing - len(toRender))) + content
                            else:
                                toRender += (' ' * (p.spacing)) + content
                            lastOnLine = p
            
            if toRender == '':
                toRender = (' ' * (gameWidth-2))
            else:
                toRender += (' ' * ((gameWidth-2) - len(toRender)))

            lineObj = Line(line,toRender,piecesOnLine)
            listOfLines[line] = lineObj


def drawGame():
    columns = get_terminal_size().columns
    print('T E T R I S'.center(columns))
    print((leftup + horizontalline * (gameWidth-2) + rightup).center(columns))
    for i,line in listOfLines.items():
        spacing = "\t\t"
        if i == 0:
            extra = spacing + leftup + (horizontalline * 6) + rightup
        elif i == 1:
            extra = spacing + verticalline + "Pontos" + verticalline
        elif i == 2:
            spoints = str(points)
            extra = spacing + verticalline + ("0"*(6-len(spoints))) + spoints + verticalline
        elif i == 3:
            extra = spacing + verticalline + (" " * 6) + verticalline
        elif i == 4:
            extra = spacing + verticalline + "Linhas" + verticalline
        elif i == 5:
            slines = str(lines)
            extra = spacing + verticalline + ("0"*(6-len(slines))) + slines + verticalline
        elif i == 6:
            extra = spacing + leftdown + (horizontalline * 6) + rightdown
        else: 
            extra = ""
        print((verticalline + line.string + verticalline).center(columns).rstrip() + extra)
    print((leftdown + horizontalline * (gameWidth-2) + rightdown).center(columns))


#music = pygame.mixer.Sound('Tetris/Sounds/music.mp3')
#music.set_volume(0.1)
#music.play(loops=-1)

while True:
    if currentPiece == None:
        for _,line in listOfLines.items():
            if line.string == pSymbol * (gameWidth-2):
                onLineFilled(line)

        formPiece()

    currentPiece.update()

    processGame()
    drawGame()

    for p in listOfPieces:
        touchingX = (currentPiece.spacing + currentPiece.width > p.spacing) and (currentPiece.spacing < p.spacing + p.width)
        touchingY = currentPiece.Pos == p.Pos - p.height
        #print('está a tocar? (X): '  + str(touchingX))
        #print('está a tocar? (Y): '  + str(touchingY))
        #print("-"*25)
        if touchingX and touchingY:
            #print("pousou em peça")
            listOfPieces.append(currentPiece)
            currentPiece = None
            break
    #print(currentPiece.Pos,currentPiece.pBottomPos)
    if currentPiece != None and currentPiece.Pos >= groundLevel:
        #print('bateu no chao')
        listOfPieces.append(currentPiece)
        currentPiece = None
        
    sleep(1/FPS)
    system('cls')