import pygame
from constants import *


# Reinforcements
def identify_reinforcement_units(turn, american_units):
    '''
    identify reinforcements for the current turn and update their coordinates to draw in the appropriate spot
    return a list of just those units
    '''
    reinforcement_units = [unit for unit in american_units if unit.reinforcement_turn == turn]

    for index, unit in enumerate(reinforcement_units):
        unit.rect.x = 1020 + ((index % 6) * 60)
        unit.rect.y = 605
    
    # print(reinforcement_units)
    return reinforcement_units

def place_reinforcement(selected_unit, area, reinforcement_units):
#     '''
#     check if conditions are met for selected unit in selected area
#     return the selected unit (None if the move was made), and message if move wasn't made
#     '''
    message = None
    if area.identifier in selected_unit.setup:
        if area.control == 'American':
            message = area.add_unit_to_area(selected_unit)
            if not message:
                selected_unit.reinforcement = False
                selected_unit.reinforcement_turn = None
                reinforcement_units.remove(selected_unit)
                selected_unit = None
        else:
            message = 'Area not American controlled'  
    else:
        message = 'Not allowed to deploy to that area'

    return selected_unit, message




# def place_reinforcement_in_map_area(selected_unit, area, reinforcement_units):
#     '''
#     check if conditions are met and then place selected unit in selected area
#     return the selected unit (None if the move was made)
#     '''
#     if area.identifier in selected_unit.setup:
#         if (area.stack_limit and len(area.american_units) < area.stack_limit) or not area.stack_limit:
#             if area.control == 'American':
#                 area.american_units.append(selected_unit)
#                 area.update_american_unit_positions()
#                 reinforcement_units.remove(selected_unit)
#                 selected_unit = None
#             else:
#                 # these prints can be changed to returns to put them on the screen if i want
#                 print('Not an American controlled Area')
#         else:
#             print('Area is already at Stacking Limit')
#     else:
#         print('Not allowed to deploy to that Area')

#     return selected_unit

def place_turn_6_reinforcements(american_units, map_areas):
    '''
    place the 2 turn 6 armor units in the appropriate map areas
    '''
    reinforcement_units = [unit for unit in american_units if unit.reinforcement and unit.reinforcement_turn == 6]
    for unit in reinforcement_units:
        for area in map_areas:
            if unit.setup == area.identifier:
                area.add_unit_to_area(unit)

# withdrawal
def withdrawal(turn, unit, map_areas, out_of_action_units, morale, permanent=False):
        for area in map_areas:
            if unit in area.american_units[:]:
                area.remove_unit_from_area(unit)
        if unit in out_of_action_units[:]:
            morale.adjust_morale(-1)
            if permanent:
                out_of_action_units.remove(unit)

        if not permanent:
            unit.reinforcemnt_turn = turn + 1
            unit.setup = [1, 2]                

            
