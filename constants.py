from enum import Enum

SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 1000

ESPRESSO = (75, 56, 42) # table top color
BAY_COLOR = (205, 210, 188)

FRAME_RATE = 60

UNIT_SIZE = (50,50)

TURNS = [(1, 'February 6-8'),
        (2, 'February 9-11'),
        (3, 'February 12-14'),
        (4, 'February 15-17'),
        (5, 'February 18-20'),
        (6, 'February 21-23'),
        (7, 'February 24-26'),
        (8, 'February 27-March 1'),
        (9, 'March 2-4')
        ]

SUPPLY_COSTS = {
    'artillery support': 1,
    'engineer support': 2,
    'recover infantry': 2,
    'recover armor': 3,
    'increase morale': 3
}

# text
LEFT_EDGE_X = 1020
LEFT_EDGE_INDENTED_X = 1030
HEADER_ROW_Y = 80
ROW_1_Y = 110
ROW_2_Y = 130
ROW_3_Y = 150
ROW_4_Y = 170
ROW_5_Y = 190
ROW_6_Y = 210

HEADER_SIZE = 25
LINE_SIZE = 20

# couldn't get these to go into the units class
# unit_type = Enum('Unittype', ['INFANTRY', 'ARMOR', 'LEADER'])
# organization = Enum('Organization', ['37TH_INF', '1ST_CAV', '11TH_AIR'])