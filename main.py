import random  # For generating random numbers
import sys  # To close the window when user clicks on cross using sys.exit
import pygame  # The python library for making our game
from pygame.locals import *  # Basic pygame imports


# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'assets/sprites/bird.png'
BAGROUND = 'assets/sprites/background.png'
PIPE = 'assets/sprites/pipe.png'


def main():
    # Initialize all pygame's modules
    pygame.init()
    # To set a fixed FPS
    FPSCLOCK = pygame.time.Clock()
    # Window Name
    pygame.display.set_caption('Flappy Bird by lurkingryuu')
    # Loading assets for showing the score
    number_images = []
    for i in range(10):
        number_images.append("assets/sprites/"+str(i)+".png")
    
    # pygame.image.load().convert_alpha()
    # pygame.image.load().convert_()
    # These convert, convert_alpha functions are used for quick blitting of images on the screen
    GAME_SPRITES['numbers'] = tuple([pygame.image.load(image_path).convert_alpha() for image_path in number_images])
    
    # Base image
    GAME_SPRITES['base'] = pygame.image.load('assets/sprites/base.png')

    # Loading the message image
    GAME_SPRITES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()


    # Pipe images, Up and Down
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE)
    )

    # Background Image Loading
    GAME_SPRITES['background'] = pygame.image.load(BAGROUND).convert()

    # Player image
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')

    # Game Loop
    while True:
        welcomeScreen(FPSCLOCK) # Shows Welcome Screen until a button is pressed
        mainGame() # This is the main game function

def welcomeScreen(FPSCLOCK):
    '''
    Shows welcome image on the screen
    '''

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH -GAME_SPRITES['message'].get_width())/2)
    messagey = int((SCREENHEIGHT-GAME_SPRITES['message'].get_height())/2)
    basex = 0
    while True:
        for event in pygame.event.get():
            # If user clicks on cross button or clicks on escape key -> close game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                sys.exit()
            
            # If user presses space key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    pass

if __name__ == '__main__':
    main()
    
