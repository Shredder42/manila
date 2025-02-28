import pygame
from constants import *

def reinforcements(turn, american_units, map_areas):
    reinforcement_units = [unit for unit in american_units if unit.reinforcement]
    
    # return reinforcement_units
    # reinforce_areas = []
    # if turn == 2:
    #     pass
    if turn == 6:
        for unit in reinforcement_units:
            if unit.reinforcement_turn == turn:
                for area in map_areas:     
                    if unit.setup == area.identifier:
                        area.american_units.append(unit)
                        area.update_american_unit_positions()

# def reinforce_turn_6()


# print(reinforcements(2, american_units, map_areas))