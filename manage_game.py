import pygame
from constants import *
import random

# game setup and control
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

def deploy_japanese_units(map_areas, terrain, area_units):
    '''
    adds Japanese units to the map, randomly selecting Area for each terrain
    '''
    for area in map_areas:
        if area.terrain == terrain:
            unit = random.choice(area_units)       
            area.japanese_unit = unit
            area_units.remove(unit)

def deploy_initial_american_units(map_areas, american_units):
    '''
    adds starting Amercian units to the map in designated Areas
    '''
    for area in map_areas:
        for unit in american_units:
            if unit.setup == area.identifier and not unit.reinforcement:
                area.add_unit_to_area(unit)

def advance_game(phase_index, turn_index):
    '''
    advances phase of game by increaing phase index when advance game button is clicked
    when phase index gets to 5 it resets to 0 and advances turn index
    '''
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

def roll_dice(dice_to_roll, drop_lowest=False):
    '''
    rolls the specified number of dice
    option to drop the lowest die
    '''

    die_results = []

    for i in range(dice_to_roll):
        die_results.append(random.randint(1, 6))

    if drop_lowest: 
        sorted_die_results = sorted(die_results)
        die_results = sorted_die_results[1:]
        
    return sum(die_results)

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
    '''
    handles the withdrawal of units from the board, both permanent and temporary
    '''
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
    '''
    determines the amount of supply that gets added in the supply phase
    certain events limit dice rolled
    in the first turn the minimum amount received is 12
    '''
    if event in ('Kembu Group Offensive', 'Shimbu Group Offensive'):
        supply = roll_dice(2)
    else:
        supply = roll_dice(4)
    if turn == 1:
        supply = max(supply, 12)
    return supply

def update_return_areas(selected_unit, map_areas):
    '''
    updates the setup areas in the american unit to where they can return to the game as reinforcements from withdrawn or out of action
    includes some base areas and if returning from out of action then they can return where there is a unit in the same division
    '''
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
                if area.control == 'American':
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
    # put this back in after testing
    if new_event == potential_events[6]:
        for area in map_areas:
            if area.control == 'American' and area.terrain in ('urban', 'fort'):
    #             # breakout = random.choices(['breakout', 'no breakout'], [0.33, 0.67])[0]
    #             # if breakout == 'no breakout':
    #             #     new_event = potential_events[9]
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
    pause units in appropriate division based on the event
    '''
    for unit in american_units:
        if unit.division == division:
            unit.paused = True

def select_iwabuchi_breakout_area(map_areas):
    '''
    gathers potential areas for the Iwabuchi breakout and selects one
    '''
    breakout_areas = []
    for area in map_areas:
        if area.control == 'American' and area.terrain in ('urban', 'fort'):
            for adjacent_area in map_areas:
                if adjacent_area.identifier in area.adjacent_areas:
                    if adjacent_area.control == 'Japanese':
                        breakout_areas.append(area)
                        break
    return random.choice(breakout_areas)

def iwabuchi_deploy_unit(breakout_area, area_units, control):
    '''
    places a new japanese unit in area where the iwabuchi breakout occurs
    '''
    new_japanese_unit = random.choice(area_units)
    breakout_area.japanese_unit = new_japanese_unit
    breakout_area.control = 'Japanese'
    control.count -= 1
    area_units.remove(new_japanese_unit)


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
    '''
    moves unit to new area or returns a message why it can't be moved
    '''
    if move_to_area.identifier in move_from_area.adjacent_areas:
        if movement_cost <= unit.movement_factor_remaining:
            if move_from_area.contested and move_to_area.japanese_unit:
                return 'Must move to vacant Area when leaving Contested Area'
            message = move_to_area.add_unit_to_area(unit)
            if not message:
                unit.deduct_movement_cost(movement_cost, stop_required)
                move_from_area.remove_unit_from_area(unit)
                unit.previous_area = move_from_area

                if move_to_area.japanese_unit:
                    move_to_area.contested = True
                if not move_to_area.american_units or not move_from_area.japanese_unit:
                    move_from_area.contested = False
        else:
            message = 'Not enough movement factor'
    else:
        message = 'Must move to adjacent Area'
    print('ran move unit')
    return message

def bloody_streets_roll(area):
    '''
    rolls die to determine the bloody streets effect
    '''

    roll = roll_dice(1)
    if area.japanese_unit.strategy == 'elite':
        roll += 1

    return roll

def bloody_streets(bloody_streets_areas, out_of_action_units):
    '''
    applies the result of the bloody streets roll
    4 is randomly put a unit in out of action
    5 reduces morale by 1
    6+ reduces morale and swtiches all units in area to spent
    '''
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
    unit.attacking = False
    return out_of_action_units

def highlight_unit(unit, surface):
    '''
    higlights selected unit by drawing box underneath
    '''
    highlight_rect = pygame.Rect(0, 0, 54, 54)
    highlight_rect.center = unit.rect.center
    if unit.attack_lead:
        color = 'red'
    else:
        color = 'green'
    pygame.draw.rect(surface, color, highlight_rect)


def request_support(support_unit_attack, support_units):
    '''
    adds a support unit to the attack
    '''
    if support_unit_attack.type == 'artillery support':
        support_unit_index = 0
    else:
        support_unit_index = 1
    if support_units[support_unit_index].count > 0:
        support_unit_attack.add_support_unit()
        support_units[support_unit_index].use_support_unit()

def calculate_attack_value(lead_attack_unit, attacking_units, artillery_support_attack, engineer_support_attack, morale, event, area):
    '''
    calculates the attack value
    '''
    attack_value = 0

    infantry_unit = False
    armor_unit = False
    leader_units = []
    fighting_units = []
    for unit in attacking_units[:]:
        if unit.unit_type == 'infantry':
            infantry_unit = True
        if unit.unit_type == 'armor':
            armor_unit = True
        if unit.unit_type == 'leader':
            leader_units.append(unit)
        else:
            fighting_units.append(unit)

    # value if lead attack unit selected
    if lead_attack_unit:
        attack_value += lead_attack_unit.attack_factor

        attack_value += len(fighting_units) - 1
            
    # value if lead attack unit not selected
    else:
        attack_value += len(fighting_units)

    if leader_units:
        for leader in leader_units:
            for unit in fighting_units:
                if leader.division == unit.division:
                    attack_value += 1
                    break 
            else:
                continue

    # artillery support
    attack_value += artillery_support_attack.count * artillery_support_attack.attack_value
    # engineer support
    attack_value += engineer_support_attack.count * engineer_support_attack.attack_value
    # combined arms
    if area.terrain == 'clear':
        if infantry_unit and armor_unit and (artillery_support_attack.count > 0 or engineer_support_attack.count > 0):
            attack_value += 1
    else: # rubble optional rule
        if infantry_unit and armor_unit and engineer_support_attack.count > 0:
            attack_value += 1
    # morale
    if not morale.shaken:
        attack_value += 1
    # event
    if area.mandatory_attack and event.type == 'Civilians and Refugees':
        attack_value -= 1

    return attack_value

def attack(attack_value, area):
    '''
    performs the actual attack  by rolling the dice for each side and returning the result of the rolls and the total values
    '''
    attack_battle_value = roll_dice(2)
    if area.japanese_unit.strategy_available and area.japanese_unit.strategy == 'elite':
        defense_battle_value = roll_dice(3, drop_lowest=True)
    else:
        defense_battle_value = roll_dice(2)

    total_attack_value = attack_value + attack_battle_value
    total_defense_value = area.defense_value + defense_battle_value

    return attack_battle_value, defense_battle_value, total_attack_value, total_defense_value

def determine_attack_result(total_attack_value, total_defense_value, area):
    '''
    determines the outcome of the attack base on the values and the terrain and japanese units
    '''
    if total_attack_value < total_defense_value:
        outcome = 'repulse'
    elif total_attack_value == total_defense_value:
        outcome = 'stalemate'
    else:
        outcome = 'success'

    if outcome == 'success' and total_attack_value - total_defense_value > total_defense_value and not area.terrain == 'fort':
        outcome = 'overrun' 

    if outcome == 'success' and area.japanese_unit.strategy_available and area.japanese_unit.strategy == 'fanatic':
        outcome = 'stalemate'
    
    return outcome

def sniper(attacking_units, area, out_of_action_units):
    '''
    applies the outcome of a sniper defense
    removes a leader from action
    if no leader is present, runs ambush instead
    '''
    leaders = [unit for unit in attacking_units if unit.unit_type == 'leader']
    # print(leaders)
    if leaders:
        sniper_victim = random.choice(leaders)
        # print(sniper_victim.unit)
        sniper_victim.spent = True
        attacking_units.remove(sniper_victim)
        out_of_action_units = remove_from_action(sniper_victim, area, out_of_action_units)
    else:
        out_of_action_units, attacking_units = ambush(attacking_units, area, out_of_action_units)

    return out_of_action_units, attacking_units

def ambush(attacking_units, area, out_of_action_units):
    '''
    applies the outcome of an ambush defense
    the lead unit is removed from action
    '''
    print('ran ambush')
    for unit in attacking_units[:]:
        if unit.attack_lead:
            unit.spent = True
            attacking_units.remove(unit)
            return remove_from_action(unit, area, out_of_action_units), attacking_units
        
def barrage_press_on(attacking_units, lead_attack_unit, area, out_of_action_units):
    '''
    applies barrage if chosen to continue
    removes one unit from action (not the lead unit) prior to the attack
    '''
    fighting_units = [unit for unit in attacking_units if unit.unit_type in ('infantry', 'armor') and not unit.attack_lead]

    if fighting_units:
        hit_unit = random.choice(fighting_units)

        attacking_units.remove(hit_unit)
        hit_unit.attacking = False
        hit_unit.spent = True
        # if hit_unit.attack_lead:
        #     hit_unit.attack_lead = False
        #     lead_attack_unit = None

    out_of_action_units = remove_from_action(hit_unit, area, out_of_action_units)
    
    return attacking_units, out_of_action_units, lead_attack_unit

def barrage_retreat(attacking_units, lead_attack_unit):
    '''
    applies the barrage if chosen to retreat
    units become spend and are allowed to retreat
    '''
    for unit in attacking_units:
        unit.spent = True
        unit.attacking = False
        if unit.attack_lead:
            unit.attack_lead = False

    lead_attack_unit = None
    attacking_units = []

    return attacking_units, lead_attack_unit


def apply_attack_outcome(attack_result, attacking_units, area, out_of_action_units, morale, control):
    '''
    applies the outcome of the attack
    overrun removes the japanese unit and units are not spent
    success removes the japanese unit and units are spent
    stalemate units are spent
    repulse the lead unit is removed from action and morale drops by 1
    '''
    for unit in attacking_units:
        unit.attacking = False
        if attack_result in ('repulse', 'stalemate', 'success'):
            unit.spent = True
        if attack_result == 'overrun':
            unit.movement_factor_remaining = unit.movement_factor
        if unit.attack_lead:
            unit.attack_lead = False
            if attack_result == 'repulse':
                out_of_action_units = remove_from_action(unit, area, out_of_action_units)

    if attack_result in ('success', 'overrun'):
        area.japanese_unit = None
        area.control = 'American'
        area.contested = False
        control.count += 1
        if area.identifier in (22, 31, 34, 37): # captured area morale bonus (9.5.8)
            morale.adjust_morale(1)

    if attack_result == 'repulse':
        morale.adjust_morale(-1)




    return out_of_action_units

def retreat(unit, area, retreating_units):
    '''
    adds unit the last area it was in during a retreat or returns a message that the area is fully stacked
    '''
    message = unit.previous_area.add_unit_to_area(unit)
    if not message:
        area.remove_unit_from_area(unit)
        retreating_units.remove(unit)
        return retreating_units

def retreat_stacked(unit, area, selected_area, retreating_units):
    '''
    if the previous area was stacked allows selection of an adjacent area to previous to retreat to
    '''
    message = area.add_unit_to_area(unit)
    if not message:
        selected_area.remove_unit_from_area(unit)
        retreating_units.remove(unit)
        unit.retreating = False
    return retreating_units

# end phase
def check_for_automatic_victory(map_areas):
    '''
    checks for an automatic victory - every area american controlled
    '''
    for area in map_areas:
        if area.control == 'Japanese':
            return False
    else:
        return True
    
def check_for_operational_victory(map_areas):
    '''
    checks for operational viction - 34+ areas and Intramuros american controlled
    '''
    count = 0
    for area in map_areas:
        if area.control == 'American':
            count += 1
    if count >= 34 and map_areas[36].control == 'American':
        return True
    else:
        return False
    



    


        










    




        
