import os
import pygame
import random
from constants import *
from pieces import AmericanUnit, JapaneseUnit, create_units

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
american_units, japanese_units = create_units() 
test_unit1 = random.choice(american_units)
test_unit2 = random.choice(japanese_units)




def main():
    running = True

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        screen.blit(surface, (0,0))

        # test_unit1.draw(surface) # remove this
        test_unit1.draw(surface)
        test_unit2.draw(surface)

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




