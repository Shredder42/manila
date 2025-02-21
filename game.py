import os
import pygame
from constants import *

# pygame setup
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Manila - The Savage Streets, 1945')
game_board = pygame.image.load('./images/map_only.png')
game_board = pygame.transform.smoothscale_by(game_board, 0.8)
clock = pygame.time.Clock()


def main():
    running = True

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




