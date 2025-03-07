import pygame
from constants import *
import random

# game control
class Button:
    def __init__(self, x, y, filename):
        self.filename = filename
        self.image = self.__load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __load_image(self):
        image = pygame.image.load(f'./images/{self.filename}')
        image = pygame.transform.smoothscale(image, (70,70))
        return image
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

def advance_game(phase_index, turn_index):
    if phase_index == 4:
        phase_index = 0
        turn_index += 1
    else:
        phase_index += 1

    return phase_index, turn_index

def update_rects_for_location_change(units):
    '''
    update the rects on units to put them in the row for moving on the map
    either as reinforcements or for movement
    '''
    for index, unit in enumerate(units):
        unit.rect.x = 1020 + ((index % 6) * 60)
        unit.rect.y = 605

# Reinforcements
def identify_reinforcement_units(turn, american_units, reinforcement_units):
    '''
    identify reinforcements for the current turn and update their coordinates to draw in the appropriate spot
    return a list of just those units
    '''
    for unit in american_units:
        if unit.reinforcement_turn == turn:
            reinforcement_units.append(unit)

    update_rects_for_location_change(reinforcement_units)
    
    # print(reinforcement_units)
    return reinforcement_units

def place_reinforcement(selected_unit, area, reinforcement_units):
    '''
    check if conditions are met for selected unit in selected area
    return the selected unit (None if the move was made), and message if move wasn't made
    '''
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
def withdraw(turn, unit, map_areas, out_of_action_units, morale, permanent=False):
    if permanent and unit.withdrawn:
        unit.reinforcement_turn = None

    else:
        for area in map_areas:
            if unit in area.american_units[:]:
                area.remove_unit_from_area(unit)
                unit.withdrawn = True
                if not permanent:
                    unit.reinforcement_turn = turn + 1
                break
        
        if unit in out_of_action_units[:]:
            morale.adjust_morale(-1)
            if permanent:
                unit.withdrawn = True
                out_of_action_units.remove(unit)

    print(permanent)
    print(f'{unit.unit} rein turn is {unit.reinforcement_turn}')

# leader mortality
def leader_mortality(turn, out_of_action_units):
    '''
    runs mortality check on leader and updates unit attributes accordingly
    also removes from out of action units
    '''
    mortality = None

    for unit in out_of_action_units[:]:
        if unit.unit_type == 'leader':
            mortality = random.choice(['kia', 'lightly wounded', 'healthy'])
            if mortality == 'lightly wounded':
                unit.reinforcement_turn = turn + 1
            elif mortality == 'healthy':
                unit.reinforcement_turn = turn

            out_of_action_units.remove(unit)

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

    if selected_unit.withdrawn:
        possible_areas.append(1)
        possible_areas.append(2)
        selected_unit.withdrawn = False

    else:
        if selected_unit.division == '37th Inf':
            possible_areas.append(1)
        elif selected_unit.division == '1st Cav':
            possible_areas.append(2)
        elif selected_unit.division == '11th Air':
            possible_areas.append(30)

        for area in map_areas:
            if area.american_units:
                for unit in area.american_units:
                    if unit.division == selected_unit.division:
                        possible_areas.append(area.identifier)

    selected_unit.setup = possible_areas

# events
def determine_game_event(potential_events, potential_event_weights, turn, game_events, map_areas):
    '''
    determine the event for the game turn
    '''
    new_event = random.choices(potential_events, weights=potential_event_weights)[0]
    print(new_event.type)
    if turn >= 6 and turn <= 9:
        if new_event == potential_events[0]:
            new_event = potential_events[1]
        elif new_event == potential_events[8]:
            new_event = potential_events[7]

    if new_event in (potential_events[2], potential_events[3], potential_events[5]):
        if turn == 1 or turn == 9:
            new_event = potential_events[9]
        if game_events:
            if new_event == game_events[-1]:
                new_event = potential_events[9]

    if new_event == potential_events[6]:
        for area in map_areas:
            if area.control == 'American' and area.terrain in ('urban', 'fort'):
                breakout = random.choices(['breakout', 'no breakout'], [0.33, 0.67])[0]
                if breakout == 'no breakout':
                    new_event = potential_events[9]
                break
        else:
            new_event = potential_events[9]

    return new_event
    

def withdraw_44th_battallion(turn, american_units, map_areas, out_of_action_units, morale, premanent=False):
    '''
    withdraws the 3 units of the 44th tank battalion either permanently or temporarily
    '''
    units_to_withdraw = [unit for unit in american_units if unit.unit.startswith('44_')]

    for unit in units_to_withdraw:
        withdraw(turn, unit, map_areas, out_of_action_units, morale, premanent)          
        update_out_of_action_unit_positions(out_of_action_units)


def update_out_of_action_unit_positions(out_of_action_units):
    '''
    updates the rect values in the American units when they are added or removed from 
    out of action
    '''
    for index, unit in enumerate(out_of_action_units):
        unit.rect.x = LEFT_EDGE_X + ((index % 6) * 60)
        if index <= 5:
            unit.rect.y = OUT_OF_ACTION_Y1 
        elif index >=6 and index <= 11:
            unit.rect.y = OUT_OF_ACTION_Y2
        elif index >= 11 and index <= 17:
            unit.rect.y = OUT_OF_ACTION_Y3
        else:
            unit.rect.y = OUT_OF_ACTION_Y4
    
def pause_division(american_units, division):
    '''
    pause units in appropriate division based on event
    '''
    for unit in american_units:
        if unit.division == division:
            unit.paused = True


# combat phase
def calculate_movement_cost(move_to_area, map_areas):
    '''
    calculates and returns the cost of moving a unit
    also returns whether the unit is required to stop after entering 
    '''
    movement_cost = 0
    if not move_to_area.japanese_unit:
        adjacent_areas = [area for area in map_areas if area.identifier in move_to_area.adjacent_areas]
        for adjacent_area in adjacent_areas:
            if adjacent_area.japanese_unit:
                movement_cost = 2
                break
        else:
            movement_cost = 1

        stop_required = False

    else:
        if move_to_area.japanese_unit.revealed:
            movement_cost = 3
        elif not move_to_area.japanese_unit.revealed:
            movement_cost = 4

        stop_required = True
    print('ran calc move cost')
    return movement_cost, stop_required

def move_unit(unit, move_from_area, move_to_area, movement_cost, stop_required):

    if move_to_area.identifier in move_from_area.adjacent_areas:
        if movement_cost <= unit.movement_factor_remaining:
            message = move_to_area.add_unit_to_area(unit)
            if not message:
                unit.deduct_movement_cost(movement_cost, stop_required)
                move_from_area.remove_unit_from_area(unit)
        else:
            message = 'Not enough movement factor'
    else:
        message = 'Must move to adjacent Area'
    print('ran move unit')
    return message

def bloody_streets_roll(area):
    roll = random.randint(1, 6)
    if area.japanese_unit.strategy == 'elite':
        roll += 1

    return roll

def bloody_streets(bloody_streets_areas, out_of_action_units):
    morale_loss = 0
    results = []
    for area in bloody_streets_areas:
        roll = bloody_streets_roll(area)
        if roll == 4:
            casualty_unit = random.choice(area.american_units) # this is change from actual rules - prefer if lost unit is random
            remove_from_action(casualty_unit, area, out_of_action_units)
            results.append(f'{unit.unit} of the {unit.division} was knocked Out of Action from Area {area.identifier}: {area.area_title}')
        elif roll == 5:
            morale_loss += 1
        elif roll >= 6:
            morale_loss += 1
            for unit in area.american_units:
                unit.spent = True
            results.append(f'All units in Area {area.identifier}: {area.area_title} are spent')
    return morale_loss, results

def remove_from_action(unit, area, out_of_action_units):
    '''
    remove American unit from action to out of action as a result of battle
    '''
    area.remove_unit_from_area(unit)
    unit.out_of_action = True
    out_of_action_units.append(unit)
    update_out_of_action_unit_positions(out_of_action_units)

    return out_of_action_units



    




        
