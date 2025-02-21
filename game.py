import os
import pygame
from constants import *
from pieces import AmericanUnit

# pygame setup
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Manila - The Savage Streets, 1945')
game_board = pygame.image.load('./images/map_only.png')
game_board = pygame.transform.smoothscale_by(game_board, 0.8)
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # need this for creating transparent rect
clock = pygame.time.Clock()

# remove this test unit
test_unit = AmericanUnit('1_5', '1st Cav', 'infantry', 5, 6, 2, '1_5_fresh.png', '1_5_spent.png')


def main():
    running = True

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        screen.blit(surface, (0,0))

        test_unit.draw(surface) # remove this

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




