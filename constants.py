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

PHASES = ['Dawn', 'Event', 'Supply', 'Combat', 'End']

SUPPLY_COSTS = {
    'artillery support': 1,
    'engineer support': 2,
    'recover infantry': 2,
    'recover armor': 3,
    'increase morale': 3
}

LEFT_EDGE_X = 1020

# out of action y pixel value
OUT_OF_ACTION_Y1 = 705
OUT_OF_ACTION_Y2 = 765
OUT_OF_ACTION_Y3 = 825
OUT_OF_ACTION_Y4 = 885

# text pixel values
LEFT_EDGE_INDENTED_X = 1030
HEADER_ROW_Y = 120
ROW_1_Y = 150
ROW_2_Y = 170
ROW_3_Y = 190
ROW_4_Y = 210
ROW_5_Y = 230
ROW_6_Y = 250

HEADER_SIZE = 25
LINE_SIZE = 20

# couldn't get these to go into the units class
# unit_type = Enum('Unittype', ['INFANTRY', 'ARMOR', 'LEADER'])
# organization = Enum('Organization', ['37TH_INF', '1ST_CAV', '11TH_AIR'])