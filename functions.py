import pygame
import random
import sys
from globalVariables import *
FPSCLOCK = pygame.time.Clock()

def welcomeScreen():
    birdX = int(SCREEN_WIDTH / 5)
    birdY = int((SCREEN_HEIGHT - GAME_SPRITES['bird'].get_height()) / 2 )
    massageX = int((SCREEN_WIDTH - GAME_SPRITES['massage'].get_width()) / 2 )
    massageY =  int(-8)
    baseX = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['bird'],(birdX,birdY))
                SCREEN.blit(GAME_SPRITES['massage'],(massageX,massageY))
                SCREEN.blit(GAME_SPRITES['base'],(baseX,GROUND))
                
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getRandomPipe():
    # creating pip for upper and lower screen 
    pipeHeight = GAME_SPRITES['pips'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(0, int((SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()) - 1.2 * offset))
    x = SCREEN_WIDTH + 10
    y1 = (pipeHeight - y2)+offset
    
    pipe = [
        {"x": x, "y": -y1},
        {"x": x, "y": y2}
    ]
    return pipe

def isCollide(birdX, birdY, upperPipes, lowerPipes):
    birdWidth = GAME_SPRITES['bird'].get_width()
    birdHeight = GAME_SPRITES['bird'].get_height()

    for pipe in upperPipes:
        if (
            birdX < pipe['x'] + GAME_SPRITES['pips'][0].get_width() and
            birdX + birdWidth > pipe['x'] and
            birdY < pipe['y'] + GAME_SPRITES['pips'][0].get_height() and
            birdY + birdHeight > pipe['y']
        ):
            GAME_SOUND['die'].play()
            welcomeScreen()
            return True
        

    for pipe in lowerPipes:
        if (
            birdX < pipe['x'] + GAME_SPRITES['pips'][1].get_width() and
            birdX + birdWidth > pipe['x'] and
            birdY < pipe['y'] + GAME_SPRITES['pips'][1].get_height() and
            birdY + birdHeight > pipe['y']
        ):
            GAME_SOUND['die'].play()
            welcomeScreen()
            return True
        

    if birdY >= GROUND - birdHeight:
        GAME_SOUND['die'].play()
        welcomeScreen()
        return True

    return False

def mainGame():
    score = 0
    birdX = int(SCREEN_WIDTH / 3)
    birdY = int(SCREEN_HEIGHT / 2)
    baseX = 0
    
    # creating 2 pipe 
    newPip1 = getRandomPipe() 
    newPip2 = getRandomPipe() 
    
    # making upper pipe
    upperPipes = [
        {"x":SCREEN_WIDTH + 200, 'y': newPip1[0]['y']},
        {"x":SCREEN_WIDTH +200+(SCREEN_WIDTH/2), 'y': newPip2[0]['y']}
    ]
    # making lower pipe
    lowerPipes = [
        {"x":SCREEN_WIDTH + 200, 'y': newPip1[1]['y']},
        {"x":SCREEN_WIDTH +200+(SCREEN_WIDTH/2), 'y': newPip2[1]['y']}
    ]
    
    pipeVelX = -4
    
    birdVelY = -9
    birdMaxVelY = 10
    birdMinVelY = -8
    birdAccY = 1
    
    birdFlapAccV = -8
    birdFlapped  = False
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                
                if birdY > 0:
                    birdVelY = birdFlapAccV
                    birdFlapped = True
                    GAME_SOUND['wing'].play()
        
        crashTest = isCollide(birdX, birdY,upperPipes,lowerPipes)
        
        if crashTest:
            return
        
        # score part
        birdMidPosition = (birdX + GAME_SPRITES['bird'].get_width())/2
        
        for pipe in upperPipes:
            
            pipeMidPosition = (pipe["x"] + GAME_SPRITES['pips'][0].get_width())/2
            
            if pipeMidPosition <= birdMidPosition < pipeMidPosition+4:
                score += 1
                GAME_SOUND['point'].play()
            
            if birdVelY < birdMaxVelY and not birdFlapped:
                birdVelY += birdAccY
                
            if birdFlapped:
                birdFlapped = False
                
            birderHeight =GAME_SPRITES['bird'].get_height()
            
            birdY = birdY + min(birdVelY, GROUND - birdY - birderHeight)
            
            # move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX
            
            # add a new pipe to the left
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])
            
            # remove pipe from game
            if upperPipes[0]['x'] < -GAME_SPRITES['pips'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            SCREEN.blit(GAME_SPRITES["background"],(0,0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES["pips"][0],(upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_SPRITES["pips"][1],(lowerPipe['x'], lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['base'],(baseX,GROUND))
            SCREEN.blit(GAME_SPRITES['bird'],(birdX,birdY))
            
            digit_num = [int(x) for x in list(str(score))]
            
            width = 0
            for digit in digit_num:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = ((SCREEN_WIDTH - width)/2)
            
            for digit in digit_num:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREEN_WIDTH * 0.3))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)