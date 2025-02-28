import pygame
from constants import *


# Reinforcements
def update_turn_2_reinforcement_coordinates(american_units):
    '''
    set the coordinates for the turn 2 reinforcements so they can be printing in the appropriate spot
    return a list of just those units
    '''
    reinforcement_units = [unit for unit in american_units if unit.reinforcement and unit.reinforcement_turn == 2]

    for index, unit in enumerate(reinforcement_units):
        unit.rect.x = 1020 + ((index % 6) * 60)
        unit.rect.y = 605

    return reinforcement_units

def place_turn_2_reinforcement_in_map_area(selected_unit, area, reinforcement_units):
    '''
    check if conditions are met and then place selected unit in selected area
    return the selected unit (None if the move was made)
    '''
    if area.identifier in selected_unit.setup:
        if (area.stack_limit and len(area.american_units) < area.stack_limit) or not area.stack_limit:
            if area.control == 'American':
                area.american_units.append(selected_unit)
                area.update_american_unit_positions()
                reinforcement_units.remove(selected_unit)
                selected_unit = None
            else:
                # these prints can be changed to returns to put them on the screen if i want
                print('Not an American controlled Area')
        else:
            print('Area is already at Stacking Limit')
    else:
        print('Not allowed to deploy to that Area')

    return selected_unit

def place_turn_6_reinforcements(american_units, map_areas):
    '''
    place the 2 turn 6 armor units in the appropriate map areas
    '''
    reinforcement_units = [unit for unit in american_units if unit.reinforcement and unit.reinforcement_turn == 6]
    for unit in reinforcement_units:
        for area in map_areas:
            if unit.setup == area.identifier:
                area.american_units.append(unit)
                area.update_american_unit_positions()
            
