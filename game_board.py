import pygame

class MapArea:
    def __init__(self, x, y, identifier, terrain, terrain_effect_modifier, area_title, adjacent_areas, control='Japanese', stack_limit = 6):
        self.x = x
        self.y = y
        self.identifier = identifier
        self.terrain = terrain
        self.terrain_effect_modifier = terrain_effect_modifier
        self.area_title = area_title
        self.adjacent_areas = adjacent_areas
        self.control = control
        self.stack_limit = stack_limit
        self.contested = False
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.stack_count = 0
        self.american_units = []
        self.japanese_unit = None # maybe a funtion to randomly pick the unit (this is currently in game.py)

    def __update_american_unit_positions(self):
        '''
        updates the rect values in the american_units list so they are always displayed beginning
        from the top left corner
        '''
        for index, unit in enumerate(self.american_units):
            unit.rect.x = 1020 + ((index % 6) * 60)
            if index <= 5:
                unit.rect.y = 370
            elif index >=6 and index <= 11:
                unit.rect.y = 430
            else:
                unit.rect.y = 490

    def add_unit_to_area(self, unit):
        if self.stack_count and (self.stack_count == self.stack_limit) and unit.type in ('infantry', 'armor'):
            return 'Area at Stacking Limit'
        else:
            self.american_units.append(unit)
            self.__update_american_unit_positions()
            if unit.unit_type in ('infantry', 'armor'):
                self.stack_count += 1
            # print('ran add unit to area')

    def remove_unit_from_area(self, unit):
        self.american_units.remove(unit)
        self.stack_count -= 1
        self.__update_american_unit_positions()
            


def create_map():
    map_areas = []
    map_areas.append(MapArea(177, 66, 1, None, None, 'Caloocan', [2, 9, 10], 'American', None))
    map_areas.append(MapArea(415, 88, 2, None, None, 'Grace Park Airfield', [1, 3, 6, 7, 9], 'American', None))
    map_areas.append(MapArea(797, 77, 3, 'clear', 2, 'Balara', [2, 4, 5, 6]))
    map_areas.append(MapArea(849, 177, 4, 'clear', 2, 'Water Supply Pipeline', [3, 5, 16]))
    map_areas.append(MapArea(676, 156, 5, 'urban', 3, 'Quezon City', [3, 4, 6, 7, 15, 16]))
    map_areas.append(MapArea(589, 96, 6, 'urban', 3, 'San Francisco Del Monte Estate', [2, 3, 5, 7]))
    map_areas.append(MapArea(440, 190, 7, 'clear', 2, 'Santa Mesa Estate', [2, 5, 6, 8, 9, 14, 15]))
    map_areas.append(MapArea(365, 244, 8, 'urban', 3, 'San Lazaro Race Course', [7, 9, 10, 12, 13, 14]))
    map_areas.append(MapArea(244, 135, 9, 'urban', 3, 'Maypajo', [1, 2, 7, 8, 10]))
    map_areas.append(MapArea(140, 204, 10, 'urban', 3, 'Cocomo Island', [1, 8, 9, 11, 12]))
    map_areas.append(MapArea(117, 322, 11, 'urban', 3, 'San Nicolas', [10, 12]))
    map_areas.append(MapArea(269, 316, 12, 'urban', 3, 'Tondo', [8, 10, 11, 13, 35]))
    map_areas.append(MapArea(425, 389, 13, 'urban', 3, 'Quiapo', [8, 12, 14, 34, 35]))
    map_areas.append(MapArea(489, 349, 14, 'urban', 3, 'Quezon Institute', [7, 8, 13, 15, 17, 18, 34]))
    map_areas.append(MapArea(644, 295, 15, 'urban', 3, 'Roario Heights', [5, 7, 14, 16, 17]))
    map_areas.append(MapArea(857, 281, 16, 'clear', 2, 'Camp Murphy', [4, 5, 15, 17, 19, 20]))
    map_areas.append(MapArea(708, 446, 17, 'urban', 3, 'San Juan del Monte', [14, 15, 16, 18, 19]))
    map_areas.append(MapArea(630, 556, 18, 'urban', 3, 'Mandaluyong', [14, 17, 19, 23, 32, 33, 34]))
    map_areas.append(MapArea(770, 594, 19, 'urban', 3, 'US Military Hospitals', [16, 17, 18, 20, 21, 22, 23]))
    map_areas.append(MapArea(885, 516, 20, 'clear', 2, 'Marikina River', [16, 19, 21]))
    map_areas.append(MapArea(934, 676, 21, 'urban', 3, 'Pasig', [19, 20, 22, 26]))
    map_areas.append(MapArea(703, 716, 22, 'fort', 4, 'Fort William McKinley', [19, 21, 23, 24, 25, 26]))
    map_areas.append(MapArea(602, 653, 23, 'urban', 3, 'Nielson Airport', [18, 19, 22, 24, 29, 32]))
    map_areas.append(MapArea(613, 822, 24, 'urban', 3, 'Pasay McKinley Road', [22, 23, 25, 27, 28, 29]))
    map_areas.append(MapArea(773, 836, 25, 'clear', 2, 'Taguig River', [22, 24, 26, 27]))
    map_areas.append(MapArea(891, 828, 26, 'urban', 3, 'Pateros', [21, 22, 25, 27]))
    map_areas.append(MapArea(777, 917, 27, 'clear', 2, 'William McKinley Reservation', [24, 25, 26, 28, 30]))
    map_areas.append(MapArea(562, 911, 28, 'fort', 4, 'Nichols Airfield', [24, 27, 29, 30]))
    map_areas.append(MapArea(516, 845, 29, 'urban', 3, 'Malibay Estate', [23, 24, 28, 30, 31, 32]))
    map_areas.append(MapArea(315, 882, 30, None, None, 'San Rafael', [27, 28, 29, 31], 'American', None))
    map_areas.append(MapArea(310, 714, 31, 'fort', 4, 'Rizal Stadium', [29, 30, 32, 33, 36]))
    map_areas.append(MapArea(466, 664, 32, 'urban', 3, 'Philippine Racing Club', [18, 23, 29, 31, 33]))
    map_areas.append(MapArea(466, 580, 33, 'fort', 4, 'Santa Ana Church', [18, 31, 32, 34, 35, 36]))
    map_areas.append(MapArea(436, 472, 34, 'fort', 4, 'Provisor Island Power Plant', [13, 14, 18, 33, 35]))
    map_areas.append(MapArea(360, 533, 35, 'fort', 4, 'Post Office', [12, 13, 33, 34, 36, 37]))
    map_areas.append(MapArea(266, 608, 36, 'fort', 4, 'University of the Philippines', [31, 33, 35, 37]))
    map_areas.append(MapArea(144, 517, 37, 'fort', 4, 'Intramuros', [35, 36]))
    
    return map_areas
