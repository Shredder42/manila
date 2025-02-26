import os
import pygame
import random
from constants import *
from pieces import AmericanUnit, JapaneseUnit, create_units, create_morale, create_control_marker, create_supply
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
legend_control_marker = create_control_marker(32, 695)
morale = create_morale()
supply = create_supply()
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
    areas_controlled = 3 # this will need to be updated by a function whenever an area flips to American control

    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        pygame.draw.rect(screen, BAY_COLOR, (30, 695, 230, 290))
        legend_control_marker.draw(screen)
        for support_unit in support_units:
            support_unit.draw(screen)
        morale.draw(screen)
        supply.draw(screen)
        text_on_screen(90, 710, str(areas_controlled), 'black', 30)
        text_on_screen(90, 770, str(morale.count), 'black', 30)
        text_on_screen(90, 830, str(support_units[0].count), 'black', 30)
        text_on_screen(90, 890, str(support_units[1].count), 'black', 30)
        text_on_screen(90, 950, str(supply.count), 'black', 30)
        text_on_screen(LEFT_EDGE_X, 20, f'Turn {TURNS[turn_index][0]}: {TURNS[turn_index][1]}, 1945', 'white', 30)
        # screen.blit(surface, (0,0)) # remove this if determine don't need
        pos = pygame.mouse.get_pos()

        # testing - remove
        # test_unit1.draw(screen)
        # test_unit2.draw(screen)
        for area in map_areas:
            if area.rect.collidepoint(pos):
                # make everything below it's own function probably
                # informational text
                text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, area.area_title, 'white', HEADER_SIZE)
                if area.identifier in (1, 2, 30):
                    text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'{area.control} controlled', 'white', LINE_SIZE)
                else:
                    if area.contested:
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'{area.control} controlled', 'white', LINE_SIZE)
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, 'Area Contested!', 'red', LINE_SIZE)
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', LINE_SIZE)
                    else:
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'{area.control} controlled', 'white', LINE_SIZE)
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', LINE_SIZE)
                
                # display japanese_unit
                if area.japanese_unit:
                    area.japanese_unit.draw(screen)
                # display american_units
                for unit in area.american_units:
                    unit.draw(screen)

        if legend_control_marker.rect.collidepoint(pos):
            control_message_1 = 'Automatic Victory if every Area is American controlled'
            control_message_2 = 'Operational Victory if Americans control:'
            text_on_screen(LEFT_EDGE_X, 80, f'Areas controlled by American Forces', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, control_message_1, 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, control_message_2, 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, '- At least 34 Areas', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_4_Y, '- Intramuros (Area 37)', 'white', LINE_SIZE)

        for support_unit in support_units:
            if support_unit.rect.collidepoint(pos):
                text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, support_unit.type.title(), 'white', HEADER_SIZE)
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'+{support_unit.attack} to Attack Value', 'white', LINE_SIZE)
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, f'Supply Cost: {support_unit.cost} Point(s)', 'white', LINE_SIZE)
                if support_unit.type == 'engineer support':
                    support_unit_message = 'Required for Combined Arms Bonus in Urban and Fort Areas'
                    text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, support_unit_message, 'white', LINE_SIZE)

        if morale.rect.collidepoint(pos):
            morale_message_1 = '+1 to Attack Value if Strong'
            morale_message_2 = '+1 to Defense Value if Shaken'
            morale_message_3 = 'Americans lose if Morale drops to 0 after any Combat Phase'
            text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, 'Morale', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, morale_message_1, 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, morale_message_2, 'white', LINE_SIZE)
            if morale.count > 3:
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, morale_message_3, 'white', LINE_SIZE)
            else:
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, morale_message_3, 'red', LINE_SIZE)

        if supply.rect.collidepoint(pos):
            text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, 'Total Supply available', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, 'Supply Costs:', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, f'- Artillery Support: {SUPPLY_COSTS["artillery support"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, f'- Engineer Support: {SUPPLY_COSTS["engineer support"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_4_Y, f'- Recover Infantry Unit: {SUPPLY_COSTS["recover infantry"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_5_Y, f'- Recover Armor Unit: {SUPPLY_COSTS["recover armor"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_6_Y, f'- Increase Morale: {SUPPLY_COSTS["increase morale"]}', 'white', LINE_SIZE)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pos)

        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




