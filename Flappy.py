import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports
import os


# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'assets/sprites/bird.png'
BACKGROUND = 'assets/sprites/background.png'
PIPE = 'assets/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    try:
        with open('assets\high_score.txt') as f:
            high_score = f.read()
            if high_score == '':
                high_score = 0
            else:
                high_score = int(high_score)
    except:
        high_score = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                scoreDisplay(high_score, SCREENHEIGHT*0.72)
                # pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    # playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # This function will return true if the player is crashed
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        # The Game Over function will be called after crashing over here
        if crashTest:
            updateHighScore(score)
            SCREEN.blit(
                GAME_SPRITES['over'],
                (int(
                    (SCREENWIDTH - GAME_SPRITES['over'].get_width())/2), int(SCREENHEIGHT*0.13))
            )
            scoreDisplay(score)
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                # print(f"Your score is {score}") # Debugging purpose
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        scoreDisplay(score)
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    playerWidth = GAME_SPRITES['player'].get_width()

    # The game will be over if the player hit's the ceiling or the base of the Game screen
    if playery > GROUNDY - playerWidth or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    # Collision with upper pipes
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < playerWidth):
            GAME_SOUNDS['hit'].play()
            return True

    # Collision with lower pipes
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < playerWidth:
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    '''
    Generate positions of two pipes(one bottom straight and one top rotated) for blitting on the screen
    '''
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/4
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                   GAME_SPRITES['base'].get_height() - 1.2*offset)) + 10
    # y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipex = SCREENWIDTH + 20
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},  # Upper Pipe
        {'x': pipex, 'y': y2}  # Lower Pipe
    ]
    return pipe


def updateHighScore(score: int):
    with open('assets\high_score.txt', 'r') as f:
        current_high_score = f.read()
        if current_high_score == '':
            current_high_score = 0
        else:
            current_high_score = int(current_high_score)
    high_score = max(current_high_score, score)
    with open('assets\high_score.txt', 'w') as f:
        f.write(str(high_score))
    return


def scoreDisplay(score, scorey=SCREENHEIGHT*0.12):
    myDigits = [int(x) for x in list(str(score))]
    width = 0
    for digit in myDigits:
        width += GAME_SPRITES['numbers'][digit].get_width()
    Xoffset = (SCREENWIDTH - width)/2

    for digit in myDigits:
        SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, scorey))
        Xoffset += GAME_SPRITES['numbers'][digit].get_width()
    pygame.display.update()


# Getting the exe to one file
# https://stackoverflow.com/a/13790741
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
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
    GAME_SPRITES['numbers'] = tuple([pygame.image.load(
        image_path).convert_alpha() for image_path in number_images])

    # Base image
    GAME_SPRITES['base'] = pygame.image.load('assets/sprites/base.png')

    # Loading the message image
    GAME_SPRITES['message'] = pygame.image.load(
        'assets/sprites/message.png').convert_alpha()

    # Pipe images, Up and Down
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE)
    )

    # Background Image Loading
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    # Player image
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Some final screen
    GAME_SPRITES['over'] = pygame.image.load(
        'assets\sprites\over.png').convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')

    # Game Loop
    while True:
        welcomeScreen()  # Shows Welcome Screen until a button is pressed
        mainGame()  # This is the main game function
