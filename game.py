import os
import pygame
import random
from constants import *
from pieces import AmericanUnit, JapaneseUnit, SupportUnit, create_units, create_morale, create_control, create_supply, create_events
from game_board import MapArea, create_map
from manage_game import *

# pygame setup
pygame.init()
pygame.font.init()


# To Do


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Manila - The Savage Streets, 1945')
game_board = pygame.image.load('./images/map_only.png')
game_board = pygame.transform.smoothscale_by(game_board, 0.8)

# font_20 = pygame.font.SysFont('times new roman', 20)
# surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # might not actually need this
clock = pygame.time.Clock()

# all testing areas - may get removed later
advance_button = Button(1450, 10, 'arrow.png')
plan_button = Button(1450, 100, 'plan_attack.png')
attack_button = Button(1450, 100, 'attack.png')
retreat_button = Button(1450, 195, 'white_flag.png')
american_units, japanese_units_clear, japanese_units_fort, japanese_units_urban, support_units = create_units()
control = create_control(32, 695)
morale = create_morale()
supply = create_supply()
potential_events, potential_event_weights = create_events()
artillery_support_attack = SupportUnit('artillery support', 0, 1, 1, 'artillery_support_front.png', LEFT_EDGE_X, 585)
engineer_support_attack = SupportUnit('engineer support', 0, 2, 2, 'engineer_support_front.png', LEFT_EDGE_X, 645)
test_unit1 = random.choice(american_units)
test_unit2 = random.choice(japanese_units_clear)




# move all this stuff later?
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

map_areas = create_map()
deploy_japanese_units(map_areas, 'clear', japanese_units_clear)
deploy_japanese_units(map_areas, 'fort', japanese_units_fort)
deploy_japanese_units(map_areas, 'urban', japanese_units_urban)
american_setup_map_areas = [map_areas[0], map_areas[1], map_areas[29]]
deploy_initial_american_units(american_setup_map_areas, american_units)
# these lines for testing - remove when done
# map_areas[0].japanese_unit = test_unit2 
# map_areas[2].contested = True

def text_on_screen(x, y, message, color, size):
    font = pygame.font.SysFont('times new roman', size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text, text_rect)

# def update_out_of_action_unit_positions(out_of_action_units):
#     '''
#     updates the rect values in the American units when they are added or removed from 
#     out of action
#     '''
#     for index, unit in enumerate(out_of_action_units):
#         unit.rect.x = LEFT_EDGE_X + ((index % 6) * 60)
#         if index <= 5:
#             unit.rect.y = OUT_OF_ACTION_Y1 
#         elif index >=6 and index <= 11:
#             unit.rect.y = OUT_OF_ACTION_Y2
#         elif index >= 11 and index <= 17:
#             unit.rect.y = OUT_OF_ACTION_Y3
#         else:
#             unit.rect.y = OUT_OF_ACTION_Y4






def main():
    running = True
    selected_unit = None
    selected_area = None
    move_from_area = None
    turn_index = 1 # this will increment at end of every turn (one below actual turn number)
    phase_index = 0 # this will increment at end of every phase and turn over at the end - update manually for now
    # areas_controlled = 3 # this will need to be updated by a function whenever an area flips to American control
    reinforcement_units = []
    out_of_action_units = []
    game_events = []
    mandatory_attacks = set()
    planning_attack = False
    attacking_units = []
    attack_value = 0
    attacking = False
    barrage = False
    barrage_retreating = False
    # attack_result = None
    lead_attack_unit = None
    retreating_units = []
    morale_message_4 = None

    
    while running:
        screen.fill(ESPRESSO)
        screen.blit(game_board, (0,0))
        pygame.draw.rect(screen, BAY_COLOR, (30, 695, 230, 290))
        text_on_screen(LEFT_EDGE_X, 20, f'Turn {TURNS[turn_index][0]}: {TURNS[turn_index][1]}, 1945', 'white', COUNTER_SIZE)
        text_on_screen(LEFT_EDGE_X, 50, f'Phase: {PHASES[phase_index]}', 'white', COUNTER_SIZE)
        text_on_screen(LEFT_EDGE_X, 90, f'Event:', 'white', COUNTER_SIZE)
        # if PHASES[phase_index] != 'Combat':
        if not planning_attack and not attacking and not barrage:
            text_on_screen(LEFT_EDGE_X, 670, 'Out of Action Units:', 'white', COUNTER_SIZE)
            for unit in out_of_action_units:
                unit.draw(screen)
        advance_button.draw(screen)
        control.draw(screen)
        for support_unit in support_units:
            support_unit.draw(screen)
        morale.draw(screen)
        supply.draw(screen)
        text_on_screen(90, 710, str(control.count), 'black', COUNTER_SIZE)
        text_on_screen(90, 770, str(morale.count), 'black', COUNTER_SIZE)
        text_on_screen(90, 830, str(support_units[0].count), 'black', COUNTER_SIZE)
        text_on_screen(90, 890, str(support_units[1].count), 'black', COUNTER_SIZE)
        text_on_screen(90, 950, str(supply.count), 'black', COUNTER_SIZE)
        for unit in reinforcement_units:
            unit.draw(screen)
        if game_events and PHASES[phase_index] != 'Dawn':
            game_events[-1].draw(screen)
        if PHASES[phase_index] == 'Combat' and selected_area: # and selected_area.contested:
            if not planning_attack:
                if not attacking:
                    if selected_area.contested:
                        plan_button.draw(screen)
                else:
                    if not barrage_retreating:
                        text_on_screen(LEFT_EDGE_X, 550, f'Attack Value: {attack_value}', 'white', HEADER_SIZE)
                        text_on_screen(LEFT_EDGE_X, 640, f'Defense Value: {selected_area.defense_value}', 'white', HEADER_SIZE)
                        if not barrage:
                            text_on_screen(LEFT_EDGE_X, 580, f'Die Roll: {attack_battle_value}', 'white', HEADER_SIZE)
                            text_on_screen(LEFT_EDGE_X, 610, f'Total Attack Value: {total_attack_value}', 'white', HEADER_SIZE)                   
                            text_on_screen(LEFT_EDGE_X, 670, f'Die Roll: {defense_battle_value}', 'white', HEADER_SIZE)
                            text_on_screen(LEFT_EDGE_X, 700, f'Total Defense Value: {total_defense_value}', 'white', HEADER_SIZE)
                            text_on_screen(LEFT_EDGE_X, 730, f'Attack Result: {attack_result.capitalize()}', 'white', HEADER_SIZE)
                    if barrage:
                        attack_button.draw(screen)                       
                        retreat_button.draw(screen)

            else:
                attack_button.draw(screen)
                text_on_screen(LEFT_EDGE_X, 550, 'Request Support', 'white', HEADER_SIZE)
                artillery_support_attack.draw(screen)
                text_on_screen(1078, 600, str(artillery_support_attack.count), 'white', COUNTER_SIZE)
                engineer_support_attack.draw(screen)
                text_on_screen(1078, 660, str(engineer_support_attack.count), 'white', COUNTER_SIZE)
                text_on_screen(LEFT_EDGE_X, 710, f'Attack Value: {attack_value}', 'white', HEADER_SIZE)
                text_on_screen(LEFT_EDGE_X, 740, f'Defense Value: {selected_area.defense_value}', 'white', HEADER_SIZE)
        
        pos = pygame.mouse.get_pos()


        if advance_button.rect.collidepoint(pos):
            if not planning_attack and not attacking:
                if mandatory_attacks:
                    text_on_screen(LEFT_EDGE_X, BOTTOM_ROW_Y, 'Mandatory Attacks remaining', 'white', LINE_SIZE)
                else:
                    text_on_screen(1435, advance_button.rect.y + 60, 'Next Phase', 'white', LINE_SIZE)
        # testing - remove
        # test_unit1.draw(screen)
        # test_unit2.draw(screen)
        


        for area in map_areas:
            if area.japanese_unit and area.american_units:
                area.contested = True
            else:
                area.contested = False

            if (area.rect.collidepoint(pos) and not selected_area) or (PHASES[phase_index] == 'Combat' and selected_area == area):
                # make everything below it's own function probably
                # informational text
                text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, area.area_title, 'white', HEADER_SIZE)
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'{area.control} controlled', 'white', LINE_SIZE)
                if area.terrain:
                    text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, f'{area.terrain.capitalize()} terrain: +{area.terrain_effect_modifier} TEM', 'white', LINE_SIZE)
                if area.contested:
                    if area.mandatory_attack:
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, 'Area Contested! - MANDATORY ATTACK', 'red', LINE_SIZE)
                    else:
                        text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, 'Area Contested!', 'red', LINE_SIZE)                    

            
                # display japanese_unit
                if area.japanese_unit:
                    if not area.japanese_unit.revealed:
                        text_on_screen(LEFT_EDGE_X, 245, 'Japanese Unit', 'white', LINE_SIZE)
                    else:
                        if area.japanese_unit.strategy_available:
                            text_on_screen(LEFT_EDGE_X, 245, f'Japanese Unit: {area.japanese_unit.strategy.capitalize()} - {area.japanese_unit.defense_factor}', 'white', LINE_SIZE)
                        else:
                            text_on_screen(LEFT_EDGE_X, 245, f'Japanese Unit: {area.japanese_unit.defense_factor}', 'white', LINE_SIZE)
                    area.japanese_unit.draw(screen)
                # display american_units
                if area.american_units:
                    text_on_screen(LEFT_EDGE_X, 345, 'American Units', 'white', LINE_SIZE)
                    for unit in area.american_units:
                        if unit.attacking:
                            highlight_unit(unit, screen)
                        unit.draw(screen)

        if control.rect.collidepoint(pos):
            control_message_1 = 'Automatic Victory if every Area is American controlled'
            control_message_2 = 'Operational Victory if Americans control:'
            text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, f'Areas controlled by American Forces', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, control_message_1, 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, control_message_2, 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, '- At least 34 Areas', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_4_Y, '- Intramuros (Area 37)', 'white', LINE_SIZE)

        for support_unit in support_units:
            if support_unit.rect.collidepoint(pos):
                text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, support_unit.type.title(), 'white', HEADER_SIZE)
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, f'+{support_unit.attack_value} to Attack Value', 'white', LINE_SIZE)
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
            if morale_message_4:
                text_on_screen(LEFT_EDGE_INDENTED_X, ROW_4_Y, morale_message_4, 'red', LINE_SIZE)

        # removes message after moving cursor off morale rect
        if not morale.rect.collidepoint(pos):
            morale_message_4 = None

        if supply.rect.collidepoint(pos):
            text_on_screen(LEFT_EDGE_X, HEADER_ROW_Y, 'Total Supply available', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_1_Y, 'Supply Costs:', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_2_Y, f'- Artillery Support: {SUPPLY_COSTS["artillery support"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_3_Y, f'- Engineer Support: {SUPPLY_COSTS["engineer support"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_4_Y, f'- Recover Infantry Unit: {SUPPLY_COSTS["infantry"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_5_Y, f'- Recover Armor Unit: {SUPPLY_COSTS["armor"]}', 'white', LINE_SIZE)
            text_on_screen(LEFT_EDGE_INDENTED_X, ROW_6_Y, f'- Increase Morale: {SUPPLY_COSTS["increase morale"]}', 'white', LINE_SIZE)


        # reinforcement part of Dawn
        # reinforcement_units = identify_reinforcement_units(TURNS[turn_index][0], american_units)
        # print(reinforcement_units)

        # turn 2 reinforcements
        if TURNS[turn_index][0] == 2 and PHASES[phase_index] == 'Dawn':
            text_on_screen(LEFT_EDGE_X, 550, 'Reinforcements Available', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_X, 580, 'Select Units to add to American controlled Areas 27, 28, or 30', 'white', LINE_SIZE)
            # for unit in reinforcement_units:
            #     unit.draw(screen)

        # turn 6 reinforcements
        if TURNS[turn_index][0] == 6 and PHASES[phase_index] == 'Dawn':
            text_on_screen(LEFT_EDGE_X, 550, 'Reinforcements Arrived', 'white', HEADER_SIZE)
            text_on_screen(LEFT_EDGE_X, 580, 'Click to deploy one Armor Unit to each Area 1 and 2', 'white', LINE_SIZE)

        
        if PHASES[phase_index] == 'Combat':
            if selected_unit:
                selected_unit.draw(screen)

            if selected_area and selected_area.contested:
                if plan_button.rect.collidepoint(pos): 
                    if not planning_attack: 
                        if not attacking:        
                            text_on_screen(plan_button.rect.x - 5, plan_button.rect.y + 75, 'Plan Attack', 'white', LINE_SIZE)
                        if attacking and barrage:
                            text_on_screen(plan_button.rect.x + 5, plan_button.rect.y + 75, 'Push On!', 'white', LINE_SIZE)
                    else:
                        if lead_attack_unit:
                            if not attacking:
                                text_on_screen(plan_button.rect.x + 5, plan_button.rect.y + 75, 'Attack!', 'white', LINE_SIZE)
                        else:
                            text_on_screen(LEFT_EDGE_X, SCREEN_HEIGHT - 30, 'Designate lead attack unit', 'white', LINE_SIZE)
                if barrage:
                    if retreat_button.rect.collidepoint(pos)                    :
                        text_on_screen(retreat_button.rect.x + 5, retreat_button.rect.y + 75, 'Retreat', 'white', LINE_SIZE)

            # mandatory withdrawal
            # units_to_withdraw = [unit for unit in american_units if unit.unit.startswith('44_')]
            # for unit in units_to_withdraw:
            #     withdrawal(6, unit, map_areas, out_of_action_units, morale, True)          
            #     update_out_of_action_unit_positions(out_of_action_units)

        # for unit in map_areas[1].american_units:
        #     print(unit.unit)
        # # print(map_areas[1].identifier)
        # if american_units[0] in map_areas[1].american_units:
        #     remove_from_action(american_units[0], map_areas[1], out_of_action_units)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pos)


                # advancing the game
                if not mandatory_attacks and not planning_attack and not attacking:
                    if advance_button.rect.collidepoint(pos):
                        phase_index, turn_index = advance_game(phase_index, turn_index)
                        selected_area = None
                        selected_unit = None
                        planning_attack = False

                        # DAWN PHASE
                        if PHASES[phase_index] == 'Dawn':
                            game_event = None
                            # mandatory withdrawal
                            if TURNS[turn_index][0] == 6:
                                withdraw_44th_battallion(TURNS[turn_index][0], american_units, map_areas, out_of_action_units, morale, premanent=True)
                            # leader_mortality
                            mortality = leader_mortality(TURNS[turn_index][0], out_of_action_units)
                            update_out_of_action_unit_positions(out_of_action_units)
                            print(mortality)
                            # reinforcement check
                            reinforcement_units = identify_reinforcement_units(TURNS[turn_index][0], american_units, reinforcement_units)


                        # EVENT PHASE
                        if PHASES[phase_index] == 'Event':
                            game_events.append(determine_game_event(potential_events, potential_event_weights, TURNS[turn_index][0], game_events, map_areas))

                            if game_events[-1].type == 'Kembu Group Breakthrough':
                                withdraw_44th_battallion(TURNS[turn_index][0], american_units, map_areas, out_of_action_units, morale, premanent=False)
                            elif game_events[-1].type == 'Pause 1st Cavalry':
                                pause_division(american_units, '1st Cav')
                            elif game_events[-1].type == 'Pause 37th Division':
                                pause_division(american_units, '37th Inf')
                            elif game_events[-1].type == 'Pause 11th Airborne':
                                pause_division(american_units, '11th Air')
                            elif game_events[-1].type == 'Shimbu Group Breakthrough':
                                withdraw_44th_battallion(TURNS[turn_index][0], american_units, map_areas, out_of_action_units, morale, premanent=False)

                        # SUPPLY PHASE
                        if PHASES[phase_index] == 'Supply':
                            supply.add_supply(get_supply(TURNS[turn_index], game_events[-1].type))

                        # COMBAT PHASE
                        if PHASES[phase_index] == 'Combat':
                            bloody_streets_areas = [area for area in map_areas if area.contested]
                            if bloody_streets_areas:
                                morale_loss, bloody_streets_results = bloody_streets(bloody_streets_areas, out_of_action_units)
                                morale.adjust_morale(-morale_loss)
                                print(f'Morale dropped by {morale_loss} points')
                                if bloody_streets_results:
                                    for result in bloody_streets_results:
                                        print(result)


                # COMBAT
                # may want to rework this entire section to be more efficient
                    # only select area once (and only if contains fresh american units)
                # select area and lock it so can interact with the units in it (will also need to be in the event for iwabuchi)
                # modify this after moving cuz will be easier to move units around then
                # get unit selected for moving to stay on the screen
                if PHASES[phase_index] == 'Combat':
                    if not planning_attack and not attacking:
                    # movement
                        for area in map_areas:
                            if area.rect.collidepoint(pos):
                                if not selected_unit:
                                    if area == selected_area:
                                        selected_area = None
                                    elif selected_area == None and area.american_units:
                                        for unit in area.american_units: # only select if area has a fresh unit
                                            if not unit.spent:
                                                selected_area = area
                                                move_from_area = area
                                                break
                                if selected_unit:
                                    movement_cost, stop_required = calculate_movement_cost(area, map_areas)
                                    message = move_unit(selected_unit, move_from_area, area, movement_cost, stop_required)
                                    if message:
                                        selected_unit.rect.x = previous_rect_x
                                        selected_unit.rect.y = previous_rect_y
                                    # if area.japanese_unit and area.american_units:
                                    #     area.contested = True
                                    if area.mandatory_attack and area.contested:
                                        mandatory_attacks.add(area)
                                    move_from_area = None
                                    selected_unit = None
                                    print(message)
                                    print(mandatory_attacks)


                        # show selected unit (probs where the reinforcement_units normally show)
                        if selected_area:
                            for unit in selected_area.american_units:
                                if unit.rect.collidepoint(pos):
                                    selected_unit = unit
                                    previous_rect_x = unit.rect.x
                                    previous_rect_y = unit.rect.y
                                    update_rects_for_location_change([unit])
                                    print(f'remaining movement factor: {selected_unit.movement_factor_remaining}')
                                    selected_area = None


                    # attacking
                    if retreating_units:
                        for unit in retreating_units:
                            if unit.rect.collidepoint(pos):
                                retreating_units = retreat(unit, selected_area, retreating_units)
                                # if retreat_stacked:





                    if attacking and not barrage and not retreating_units: 
                        # if selected_area.japanese_unit.strategy_available:
                        #     if selected_area.japanese_unit.strategy == 'sniper':
                        #         out_of_action_units, attacking_units = sniper(attacking_units, selected_area, out_of_action_units)
                        #     if selected_area.japanese_unit.strategy == 'ambush':
                        #         out_of_action_units, attacking_units = ambush(attacking_units, selected_area, out_of_action_units)
                        if attack_result:
                            out_of_action_units = apply_battle_outcome(attack_result, attacking_units, selected_area, out_of_action_units, morale, control)
                        if selected_area.japanese_unit: # clear everything after attack
                            selected_area.japanese_unit.strategy_available = False
                        # for unit in attacking_units:
                        #     unit.attacking = False
                        #     unit.attack_lead = False
                            # unit.spent = True
                        attacking_units = []
                        lead_attack_unit = None
                        attack_value = 0
                        artillery_support_attack.count = 0
                        engineer_support_attack.count = 0
                        attack_result = None
                        selected_area.mandatory_attack = False
                        if selected_area in mandatory_attacks:
                            mandatory_attacks.remove(selected_area)
                        selected_area = None
                        attacking = False
                        barrage_retreating = False


                    if attacking and barrage:
                        if attack_button.rect.collidepoint(pos):
                            attacking_units, out_of_action_units, lead_attack_unit = barrage_press_on(attacking_units, lead_attack_unit, selected_area, out_of_action_units)
                            selected_area.japanese_unit.strategy_available = False
                            barrage = False
                            attack_value = calculate_attack_value(lead_attack_unit, attacking_units, artillery_support_attack, engineer_support_attack, morale, game_events[-1], selected_area)
                            attack_battle_value, defense_battle_value, total_attack_value, total_defense_value = attack(attack_value, selected_area, attacking_units)
                            attack_result = determine_attack_result(total_attack_value, total_defense_value, selected_area)
                            out_of_action_units = apply_battle_outcome(attack_result, attacking_units, selected_area, out_of_action_units, morale, control)
                        if retreat_button.rect.collidepoint(pos):
                            attacking_units, lead_attack_unit = barrage_retreat(attacking_units, lead_attack_unit)
                            support_units[0].count += artillery_support_attack.count
                            support_units[1].count += engineer_support_attack.count
                            # function for retreating 
                            selected_area.japanese_unit.strategy_available = False
                            barrage = False
                            barrage_retreating = True
                           


                        # attack_battle_value, defense_battle_value, total_attack_value, total_defense_value = attack(attack_value, selected_area, attacking_units)
                        # attack_result = determine_attack_result(total_attack_value, total_defense_value, selected_area)


                    if selected_area and selected_area.contested:
                        if not planning_attack:
                            if not attacking:
                                if plan_button.rect.collidepoint(pos):
                                    planning_attack = True
                                # attacking_units = []

                        else:
                            for unit in selected_area.american_units:
                                if unit.rect.collidepoint(pos):
                                    if not unit.paused and not unit.spent: # deal with paused and spent units (spent units also can't move)
                                        if not unit.attacking: # puts unit in attack
                                            attacking_units.append(unit)
                                            unit.attacking = True
                                        elif unit.attacking:
                                            if not unit.attack_lead: # makes unit lead attack unit
                                                if lead_attack_unit:
                                                    lead_attack_unit.attack_lead = False
                                                unit.attack_lead = True
                                                lead_attack_unit = unit
                                            else: # removes unit from attacking (and no longer lead)
                                                attacking_units.remove(unit)
                                                unit.attacking = False
                                                unit.attack_lead = False
                                                lead_attack_unit = None
                                        attack_value = calculate_attack_value(lead_attack_unit, attacking_units, artillery_support_attack, engineer_support_attack, morale, game_events[-1], selected_area)

                                    else:
                                        print('Unit is paused and may not attack')


                            if artillery_support_attack.count + engineer_support_attack.count < len(attacking_units): # support limit 9.5.4
                                if artillery_support_attack.rect.collidepoint(pos):
                                    if (TURNS[turn_index][0] < 4 and artillery_support_attack.count == 0) or TURNS[turn_index][0] >= 4:
                                        request_support(artillery_support_attack, support_units)
                                    else: # historical artillery support restrictions optional rule
                                        print('More than 1 Artillery Support not allowed')
                                if engineer_support_attack.rect.collidepoint(pos):
                                    request_support(engineer_support_attack, support_units)
                                    attack_value = calculate_attack_value(lead_attack_unit, attacking_units, artillery_support_attack, engineer_support_attack, morale, game_events[-1], selected_area)
                            # selected_area.japanese_unit.revealed = True
                            selected_area.calculate_defense_value(morale) # have this run whenever the japanese unit gets revealed like the line above
                            # print(area.identifier)
                            # print(area.japanese_unit.revealed)
                            # defense_value = calculate_defense_value(selected_area, morale)
                            if attack_button.rect.collidepoint(pos):
                                if attacking_units and lead_attack_unit:
                                    selected_area.japanese_unit.revealed = True
                                    selected_area.calculate_defense_value(morale)
                                    planning_attack = False
                                    attacking = True
                                    if selected_area.japanese_unit.strategy_available and selected_area.japanese_unit.strategy == 'barrage':
                                        barrage = True
                                    if not barrage:
                                        attack_battle_value, defense_battle_value, total_attack_value, total_defense_value = attack(attack_value, selected_area, attacking_units)
                                        attack_result = determine_attack_result(total_attack_value, total_defense_value, selected_area)
                                        print(attack_result)
                                        # print(selected_area.japanese_unit.strategy_available)
                                        print(selected_area.japanese_unit.strategy)
                                        if selected_area.japanese_unit.strategy_available:
                                            if selected_area.japanese_unit.strategy == 'sniper':
                                                out_of_action_units, attacking_units = sniper(attacking_units, selected_area, out_of_action_units)
                                            if selected_area.japanese_unit.strategy == 'ambush':
                                                out_of_action_units, attacking_units = ambush(attacking_units, selected_area, out_of_action_units)
                                        if attack_result == 'repulse' and selected_area.mandatory_attack:
                                            retreating_units = [unit for unit in attacking_units if not unit.attack_lead]
                                            # for unit in retreating_units:
                                            #     print(unit.unit)
                                        # print(retreating_units)
                                                # print(out_of_action_units)
                                        # out_of_action_units = apply_battle_outcome(attack_result, attacking_units, selected_area, out_of_action_units, morale, control, False)
                        


                            




                # turn_index = 5

                # if TURNS[turn_index][0] == 5 and PHASES[phase_index] == 'Dawn' and out_of_action_units:
                    # mortality = leader_mortality(TURNS[turn_index][0], out_of_action_units)
                    # print(mortality)

                # this is a test of out_of_action_units - remove later and update code
                # if map_areas[0].rect.collidepoint(pos):
                #     out_of_action_units = remove_from_action(map_areas[0].american_units[-1], map_areas[0], out_of_action_units)
                if american_units[0] in map_areas[1].american_units and map_areas[2].rect.collidepoint(pos):
                    remove_from_action(american_units[0], map_areas[1], out_of_action_units)
                    remove_from_action(american_units[21], map_areas[1], out_of_action_units)
                    remove_from_action(american_units[22], map_areas[1], out_of_action_units)
                    remove_from_action(american_units[29], map_areas[1], out_of_action_units)
                    # reinforcement_units = identify_reinforcement_units(TURNS[turn_index][0], american_units, reinforcement_units)

                # reinforcements UPDATE HOW REINFORCEMENT UNITS GET ADDED (TURN QUALIFIER - SHOULD ONLY WORK IN CORRECT PHASE FOR BOTH )
                if PHASES[phase_index] in ('Dawn', 'Supply'):
                    # print(selected_unit.unit)
                    for unit in reinforcement_units:
                        update_return_areas(unit, map_areas)
                        if unit.rect.collidepoint(pos):
                            selected_unit = unit
                            # print(f'selected unit: {selected_unit.unit}')

                    if selected_unit:
                        for area in map_areas:
                            if area.rect.collidepoint(pos):
                                selected_unit, message = place_reinforcement(selected_unit, area, reinforcement_units)
                # print(selected_unit)

                # if TURNS[turn_index][0] == 6 and PHASES[phase_index] == 'Dawn':
                #     place_turn_6_reinforcements(american_units, map_areas[:2])
                #     for unit in reinforcement_units:
                #         print(unit.unit)

                # supply
                if PHASES[phase_index] == 'Supply':

                    # may want to put these into one or two functions
                    # artillery support
                    if support_units[0].rect.collidepoint(pos):
                        message = supply.spend_supply(support_units[0].type)
                        if not message:
                            support_units[0].add_support_unit()
                    # engineer support
                    if support_units[1].rect.collidepoint(pos):
                        message = supply.spend_supply(support_units[1].type)
                        if not message:
                            support_units[1].add_support_unit()
                    # increase morale
                    if morale.rect.collidepoint(pos):
                        if morale.count < 19:
                            message = supply.spend_supply('increase morale')
                            if not message:
                                morale.adjust_morale(1)
                        else:
                            morale_message_4 = 'Morale already at max'
                    # return unit to map - MAYBE WANT TO CLEAN THIS UP
                    for unit in out_of_action_units:
                        if unit.rect.collidepoint(pos):
                            if unit.unit_type in ('infantry', 'armor'):
                                message = supply.spend_supply(unit.unit_type)
                                if not message:
                                    unit.reinforcement_turn = TURNS[turn_index]
                                    reinforcement_units = identify_reinforcement_units(TURNS[turn_index], [unit], reinforcement_units)
                                    out_of_action_units.remove(unit)
                                    update_out_of_action_unit_positions(out_of_action_units)
                                
                    # finish placing the reinforcement
                    # print(selected_unit.unit)
                    print(f'first rein units {reinforcement_units}')
                    if reinforcement_units and not selected_unit:
                        for unit in reinforcement_units:
                            if unit.rect.collidepoint(pos):
                                selected_unit = unit
                                # print(f'selected unit: {selected_unit.unit}')
                                # print(f'second rein units {reinforcement_units}')

                    if selected_unit:
                        for area in map_areas:
                            if area.rect.collidepoint(pos):
                                # print(f'third rein unit {reinforcement_units}')
                                selected_unit, message = place_reinforcement(selected_unit, area, reinforcement_units)
                    # print(f'selected unit {selected_unit}')                                              







        pygame.display.flip() # flip the display to put changes on screen

        clock.tick(FRAME_RATE) # 60 fps

if __name__ == '__main__':
    main()




