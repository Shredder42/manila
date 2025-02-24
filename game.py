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

# font_20 = pygame.font.SysFont('times new roman', 20)
# surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # might not actually need this
clock = pygame.time.Clock()

# all testing areas - may get removed later
american_units, japanese_units_clear, japanese_units_fort, japanese_units_urban = create_units() 
test_unit1 = random.choice(american_units)
# test_unit2 = random.choice(japanese_units)
turns = [(1, 'February 6-8'),
        (2, 'February 9-11'),
        (3, 'February 12-14'),
        (4, 'February 15-17'),
        (5, 'February 18-20'),
        (6, 'February 21-23'),
        (7, 'February 24-26'),
        (8, 'February 27-March 1'),
        (9, 'March 2-4')
        ]


# move all this stuff later?
def add_japanese_units(map_areas, terrain, area_units):
    for area in map_areas:
        if area.terrain == terrain:
            unit = random.choice(area_units)       
            area.japanese_unit = unit
            area_units.remove(unit)

map_areas = create_map()
add_japanese_units(map_areas, 'clear', japanese_units_clear)
add_japanese_units(map_areas, 'fort', japanese_units_fort)
add_japanese_units(map_areas, 'urban', japanese_units_urban)

print(map_areas[3].japanese_unit.terrain)
print(map_areas[35].japanese_unit.terrain)


def text_on_screen(x, y, message, color, size):
    font = pygame.font.SysFont('times new roman', size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text, text_rect)


def main():
    running = True
    turn_index = 0 # this will increment at end of every turn (one below actual turn number) 

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        text_on_screen(1020, 20, f'Turn {turns[turn_index][0]}: {turns[turn_index][1]}, 1945', 'white', 30)
        # screen.blit(surface, (0,0)) # remove this if determine don't need
        pos = pygame.mouse.get_pos()

        # testing - remove
        # test_unit1.draw(screen)
        # test_unit2.draw(screen)
        for area in map_areas:
            if area.rect.collidepoint(pos):
                # make everything below it's own function probably
                # informational text
                text_on_screen(1020, 80, f'Area {area.identifier}: {area.area_title}', 'white', 25)
                if area.identifier in (1, 2, 30):
                    text_on_screen(1030, 110, f'Control: {area.control}', 'white', 20)
                else:
                    text_on_screen(1030, 110, f'Control: {area.control}', 'white', 20)
                    text_on_screen(1030, 130, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', 20)
                
                    # display japanese_unit
                    area.japanese_unit.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pos)

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




