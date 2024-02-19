import pygame
from pygame.locals import *
from globalVariables import *
from functions import *

if __name__ == "__main__":
    
    pygame.init()
    pydis.set_caption("Flappy Bird By CoderBoy M J H Nahid")
    
    # storing point image in game sprites variables
    point_list = []
    for point in range(10):
        point_list.append(pygame.image.load(f"images/{point}.png").convert_alpha())
    
    GAME_SPRITES['numbers'] = tuple(point_list)
    GAME_SPRITES['base'] = pygame.image.load("images/base.png").convert_alpha()
    GAME_SPRITES['pips'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['bird'] = pygame.image.load(BIRD).convert_alpha()
    GAME_SPRITES['massage'] = pygame.image.load("images/welcome.png").convert_alpha()
    
    # storing sounds in game sounds variable
    GAME_SOUND['die'] = pygame.mixer.Sound('audio/die.wav')    
    GAME_SOUND['hit'] = pygame.mixer.Sound('./audio/hit.wav')    
    GAME_SOUND['point'] = pygame.mixer.Sound('./audio/point.wav')    
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('./audio/swoosh.wav')  
    GAME_SOUND['wing'] = pygame.mixer.Sound('./audio/wing.wav')  

    while True:
        welcomeScreen()
        mainGame()
    


