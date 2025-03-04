import pygame
from constants import *
import random


# Reinforcements
def identify_reinforcement_units(turn, american_units, reinforcement_units):
    '''
    identify reinforcements for the current turn and update their coordinates to draw in the appropriate spot
    return a list of just those units
    '''
    for unit in american_units:
        if unit.reinforcement_turn == turn:
            reinforcement_units.append(unit)

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
    print(reinforcement_units)
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
        message = 'Not allowed to deploy to this area'

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

# leader mortality
def leader_mortality(turn, out_of_action_units):
    for unit in out_of_action_units:
        if unit.unit_type == 'leader':
            mortality = random.choice(['kia', 'lightly wounded', 'healthy'])
            if mortality == 'kia':
                out_of_action_units.remove(unit)
            elif mortality == 'lightly wounded':
                out_of_action_units.remove(unit)
                unit.reinforcement_turn = turn + 1
                # returns now following same as those returning from supply (needs to have some helper functions set up)
            else:
                pass
                # returns now following same as those returning from supply (needs to have some helper functions set up)
    return mortality # for message about what happened

# supply
def get_supply(turn, event):
    if event in ('Kembu Group Offensive', 'Shimbu Group Offensive'):
        supply = sum([random.randint(1,6), random.randint(1,6)])
    else:
        supply = sum([random.randint(1,6), random.randint(1,6), random.randint(1,6), random.randint(1,6)])
    if turn == 1:
        supply = max(supply, 12)
    return supply

def update_return_areas(selected_unit, map_areas):
    possible_areas = []
    if selected_unit.organization == '37th Inf':
        possible_areas.append(1)
    elif selected_unit.organization == '1st Cav':
        possible_areas.append(2)
    elif selected_unit.organization == '11th Air':
        possible_areas.append(30)

    for area in map_areas:
        if area.american_units:
            for unit in area.american_units:
                if unit.organization == selected_unit.organization:
                    possible_areas.append(area.identifier)

    selected_unit.setup = possible_areas




            
