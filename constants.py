from enum import Enum

SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 1000

ESPRESSO = (75, 56, 42) # table top color
BAY_COLOR = (205, 210, 188)

FRAME_RATE = 60

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

# couldn't get these to go into the units class
# unit_type = Enum('Unittype', ['INFANTRY', 'ARMOR', 'LEADER'])
# organization = Enum('Organization', ['37TH_INF', '1ST_CAV', '11TH_AIR'])