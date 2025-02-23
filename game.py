import os
import pygame
import random
from constants import *
from pieces import AmericanUnit, JapaneseUnit, create_units
from game_board import MapArea, create_map

# pygame setup
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Manila - The Savage Streets, 1945')
game_board = pygame.image.load('./images/map_only.png')
game_board = pygame.transform.smoothscale_by(game_board, 0.8)
# surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # might not actually need this
clock = pygame.time.Clock()

# all testing areas - may get removed later
american_units, japanese_units = create_units() 
test_unit1 = random.choice(american_units)
test_unit2 = random.choice(japanese_units)

map_areas = create_map()




def main():
    running = True

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        # screen.blit(surface, (0,0)) # remove this if determine don't need
        pos = pygame.mouse.get_pos()

        # testing - remove
        test_unit1.draw(screen)
        test_unit2.draw(screen)
        # for area in map_areas:
        #     if area.rect.collidepoint(pos):
        #         print(area.area_title) # This works!!!!!

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pos)

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




