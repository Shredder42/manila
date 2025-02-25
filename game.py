import os
import pygame
import random
from constants import *
from pieces import AmericanUnit, JapaneseUnit, create_units, create_morale
from game_board import MapArea, create_map

# pygame setup
pygame.init()
pygame.font.init()


# To Do
    # move the message center to lower right corner and everything else up?

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Manila - The Savage Streets, 1945')
game_board = pygame.image.load('./images/map_only.png')
game_board = pygame.transform.smoothscale_by(game_board, 0.8)

# font_20 = pygame.font.SysFont('times new roman', 20)
# surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # might not actually need this
clock = pygame.time.Clock()

# all testing areas - may get removed later
american_units, japanese_units_clear, japanese_units_fort, japanese_units_urban, support_units = create_units() 
morale = create_morale()
test_unit1 = random.choice(american_units)
# test_unit2 = random.choice(japanese_units)



# move all this stuff later?
def add_japanese_units(map_areas, terrain, area_units):
    '''
    adds Japanese units to the map, randomly selecting Area for each terrain
    '''
    for area in map_areas:
        if area.terrain == terrain:
            unit = random.choice(area_units)       
            area.japanese_unit = unit
            area_units.remove(unit)

def add_american_units(map_areas, american_units):
    '''
    adds starting Amercian units to the map in designated Areas
    '''
    for area in map_areas:
        for unit in american_units:
            if unit.setup == area.identifier and not unit.reinforcement:
                area.american_units.append(unit)
        area.update_american_unit_positions()



map_areas = create_map()
american_setup_map_areas = [map_areas[0], map_areas[1], map_areas[29]]
add_japanese_units(map_areas, 'clear', japanese_units_clear)
add_japanese_units(map_areas, 'fort', japanese_units_fort)
add_japanese_units(map_areas, 'urban', japanese_units_urban)
add_american_units(american_setup_map_areas, american_units)

# print(map_areas[3].japanese_unit.terrain)
# print(map_areas[35].japanese_unit.terrain)
# print(map_areas[1].american_units)
# print(map_areas[1].american_units[3].rect.x)


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
        pygame.draw.rect(screen, BAY_COLOR, (30, 695, 230, 290))
        for support_unit in support_units:
            support_unit.draw(screen)
        morale.draw(screen)
        text_on_screen(90, 770, str(morale.total), 'black', 30)
        text_on_screen(90, 830, str(support_units[0].total), 'black', 30)
        text_on_screen(90, 890, str(support_units[1].total), 'black', 30)
        text_on_screen(1020, 20, f'Turn {TURNS[turn_index][0]}: {TURNS[turn_index][1]}, 1945', 'white', 30)
        # screen.blit(surface, (0,0)) # remove this if determine don't need
        pos = pygame.mouse.get_pos()

        # testing - remove
        # test_unit1.draw(screen)
        # test_unit2.draw(screen)
        for area in map_areas:
            if area.rect.collidepoint(pos):
                # make everything below it's own function probably
                # informational text
                text_on_screen(1020, 80, area.area_title, 'white', 25)
                if area.identifier in (1, 2, 30):
                    text_on_screen(1030, 110, f'{area.control} controlled', 'white', 20)
                else:
                    if area.contested:
                        text_on_screen(1030, 110, f'{area.control} controlled', 'white', 20)
                        text_on_screen(1030, 130, 'Area Contested!', 'red', 20)
                        text_on_screen(1030, 150, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', 20)
                    else:
                        text_on_screen(1030, 110, f'{area.control} controlled', 'white', 20)
                        text_on_screen(1030, 130, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', 20)
                
                # display japanese_unit
                if area.japanese_unit:
                    area.japanese_unit.draw(screen)
                # display american_units
                for unit in area.american_units:
                    unit.draw(screen)

        for support_unit in support_units:
            if support_unit.rect.collidepoint(pos):
                text_on_screen(1020, 80, support_unit.type.title(), 'white', 25)
                text_on_screen(1030, 110, f'+{support_unit.attack} to Attack Value', 'white', 20)
                text_on_screen(1030, 130, f'Supply Cost: {support_unit.cost} Point(s)', 'white', 20)
                if support_unit.type == 'engineer support':
                    support_unit_message = 'Required for Combined Arms Bonus in Urban and Fort Areas.'
                    text_on_screen(1030, 150, support_unit_message, 'white', 20)

        if morale.rect.collidepoint(pos):
            morale_message_1 = '+1 to Attack Value if Strong'
            morale_message_2 = '+1 to Defense Value if Shaken'
            morale_message_3 = 'Americans lose if Morale drops to 0 after any Combat Phase'
            text_on_screen(1020, 80, 'Moral', 'white', 25)
            text_on_screen(1030, 110, morale_message_1, 'white', 20)
            text_on_screen(1030, 130, morale_message_2, 'white', 20)
            if morale.total > 3:
                text_on_screen(1030, 150, morale_message_3, 'white', 20)
            else:
                text_on_screen(1030, 150, morale_message_3, 'red', 20)

            


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pos)

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




