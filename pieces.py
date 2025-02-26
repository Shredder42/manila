import pygame
from constants import *

class AmericanUnit:
    def __init__(self, unit, organization, unit_type, attack, 
                move, setup, unit_fresh_image_filename, unit_spent_image_filename,
                reinforcement = False, leader = False):
        self.unit = unit
        self.organization = organization
        self.unit_type = unit_type
        self.attack = attack
        self.move = move
        self.setup = setup
        self.unit_fresh_image_filename = unit_fresh_image_filename
        self.unit_spent_image_filename = unit_spent_image_filename
        self.reinforcement = reinforcement
        self.leader = leader
        self.fresh_image = self.__load_images()[0]
        self.spent_image = self.__load_images()[1]
        self.fresh = True
        self.rect = self.fresh_image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.out_of_action = False
        self.moving = False

    def __load_images(self):
        '''
        load the images for each unit
        '''
        fresh_image = pygame.image.load(f'./images/{self.unit_fresh_image_filename}')
        fresh_image = pygame.transform.smoothscale(fresh_image, UNIT_SIZE)
        spent_image = pygame.image.load(f'./images/{self.unit_spent_image_filename}')
        spent_image = pygame.transform.smoothscale(spent_image, UNIT_SIZE)
        return fresh_image, spent_image
    
    def draw(self, surface):
        '''
        draw the unit on the board or table
        '''
        if self.fresh:
            surface.blit(self.fresh_image, self.rect)
        else:
            surface.blit(self.spent_image, self.rect)

class JapaneseUnit:
    def __init__(self, terrain, strategy, defense, unit_revealed_filename, unit_unrevealed_filename):
        self.terrain = terrain
        self.strategy = strategy
        self.unit_unrevealed_filename = unit_unrevealed_filename
        self.unit_revealed_filename = unit_revealed_filename
        self.unrevealed_image = self.__load_images()[0]
        self.revealed_image = self.__load_images()[1]
        self.defense = defense
        self.revealed = False
        self.rect = self.unrevealed_image.get_rect()
        self.rect.x = 1020
        self.rect.y = 200 # may want to bump this down a smidge

    def __load_images(self):
        '''
        load the images for each unit
        '''
        unrevealed_image = pygame.image.load(f'./images/{self.unit_unrevealed_filename}')
        unrevealed_image = pygame.transform.smoothscale(unrevealed_image, UNIT_SIZE)
        revealed_image = pygame.image.load(f'./images/{self.unit_revealed_filename}')
        revealed_image = pygame.transform.smoothscale(revealed_image, UNIT_SIZE)
        return unrevealed_image, revealed_image
    
    def draw(self, surface):
        '''
        draw the unit on the board or table
        '''
        if not self.revealed:
            surface.blit(self.unrevealed_image, self.rect)
        else:
            surface.blit(self.revealed_image, self.rect)

class SupportUnit:
    def __init__(self, type, count, attack, cost, filename, x, y):
        self.type = type
        self.count = count
        self.attack = attack
        self.cost = cost
        self.filename = filename
        self.image = self.__load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __load_image(self):
        '''
        load supply image
        '''
        image = pygame.image.load(f'./images/{self.filename}')
        image = pygame.transform.smoothscale(image, UNIT_SIZE)
        return image
    
    def draw(self, surface):
        '''
        draw unit on board or table
        '''
        surface.blit(self.image, self.rect)

class Morale:
    def __init__(self):
        self.strong_filepath = './images/morale_strong.png'
        self.shaken_filepath = './images/morale_shaken.png'
        self.strong_image = self.__load_images()[0]
        self.shaken_image = self.__load_images()[1]
        self.rect = self.strong_image.get_rect()
        self.rect.x = 32
        self.rect.y = 755
        self.count = 19
        self.shaken = False

    def __load_images(self):
        '''
        load the images for morale marker
        '''
        strong_image = pygame.image.load(self.strong_filepath)
        strong_image = pygame.transform.smoothscale(strong_image, UNIT_SIZE)
        shaken_image = pygame.image.load(self.shaken_filepath)
        shaken_image = pygame.transform.smoothscale(shaken_image, UNIT_SIZE)
        return strong_image, shaken_image
    
    
    def draw(self, surface):
        '''
        draw morale image to the screen
        '''
        if not self.shaken:
            surface.blit(self.strong_image, self.rect)
        else:
            surface.blit(self.shaken_image, self.rect)

    def adjust_morale(self, amount):
        '''
        adjusts morale and strong/shaken status
        '''
        self.count += amount

        if self.count <= 9:
            self.shaken = True
        else:
            self.shaken = False

class ControlMarker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.filepath = './images/control_front.png'
        self.image = self.__load_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __load_image(self):
        image = pygame.image.load(self.filepath)
        image = pygame.transform.smoothscale(image, UNIT_SIZE)
        return image
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Supply:
    def __init__(self):
        self.filepath = './images/supply_1.png'
        self.image = self.__load_image()
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 935
        self.count = 0

    def __load_image(self):
        image = pygame.image.load(self.filepath)
        image = pygame.transform.smoothscale(image, UNIT_SIZE)
        return image
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def add_supply(self, amount_received):
        '''
        adds the amount of supply received to that available suppy
        '''
        self.count += amount_received

    def spend_supply(self, item_purchased):
        '''
        subtacts amount of supply available when supply is spent
        '''
        if self.count >= SUPPLY_COSTS[item_purchased]:
            self.count -= SUPPLY_COSTS[item_purchased]
        # figure out message and how this will work
        # else:
        #     text_on_screen()

def create_units():
    '''
    create units for both sides and return in a list
    '''
    # create American units
    american_units = []
    american_units.append(AmericanUnit('1_5', '1st Cav', 'infantry', 5, 6, 2, '1_5_fresh.png', '1_5_spent.png'))
    american_units.append(AmericanUnit('1_12', '1st Cav', 'infantry', 5, 6, 2, '1_12_fresh.png', '1_12_spent.png'))
    american_units.append(AmericanUnit('1_129', '37th Inf', 'infantry', 4, 6, 1, '1_129_fresh.png', '1_129_spent.png'))
    american_units.append(AmericanUnit('1_145', '37th Inf', 'infantry', 4, 6, 1, '1_145_fresh.png', '1_145_spent.png'))
    american_units.append(AmericanUnit('1_148', '37th Inf', 'infantry', 4, 6, 1, '1_148_fresh.png', '1_148_spent.png'))
    american_units.append(AmericanUnit('1_187', '11th Air', 'infantry', 4, 4, [27, 28, 30], '1_187_fresh.png', '1_187_spent.png', True))
    american_units.append(AmericanUnit('1_188', '11th Air', 'infantry', 4, 4, [27, 28, 30], '1_188_fresh.png', '1_188_spent.png', True))
    american_units.append(AmericanUnit('1_511', '11th Air', 'infantry', 4, 4, 30, '1_511_fresh.png', '1_511_spent.png'))
    american_units.append(AmericanUnit('2_7', '1st Cav', 'infantry', 5, 6, 2, '2_7_fresh.png', '2_7_spent.png'))
    american_units.append(AmericanUnit('2_8', '1st Cav', 'infantry', 5, 6, 2, '2_8_fresh.png', '2_8_spent.png'))
    american_units.append(AmericanUnit('2_129', '37th Inf', 'infantry', 4, 6, 1, '2_129_fresh.png', '2_129_spent.png'))
    american_units.append(AmericanUnit('2_145', '37th Inf', 'infantry', 4, 6, 1, '2_145_fresh.png', '2_145_spent.png'))
    american_units.append(AmericanUnit('2_148', '37th Inf', 'infantry', 4, 6, 1, '2_148_fresh.png', '2_148_spent.png'))
    american_units.append(AmericanUnit('2_187', '11th Air', 'infantry', 4, 4, [27, 28, 30], '2_187_fresh.png', '2_187_spent.png', True))
    american_units.append(AmericanUnit('2_188', '11th Air', 'infantry', 4, 4, [27, 28, 30], '2_188_fresh.png', '2_188_spent.png', True))
    american_units.append(AmericanUnit('2_511', '11th Air', 'infantry', 4, 4, 30, '2_511_fresh.png', '2_511_spent.png'))
    american_units.append(AmericanUnit('3_129', '37th Inf', 'infantry', 4, 6, 1, '3_129_fresh.png', '3_129_spent.png'))
    american_units.append(AmericanUnit('3_145', '37th Inf', 'infantry', 4, 6, 1, '3_145_fresh.png', '3_145_spent.png'))
    american_units.append(AmericanUnit('3_148', '37th Inf', 'infantry', 4, 6, 1, '3_148_fresh.png', '3_148_spent.png'))
    american_units.append(AmericanUnit('3_511', '11th Air', 'infantry', 4, 4, 30, '3_511_fresh.png', '3_511_spent.png'))
    american_units.append(AmericanUnit('44_a', '1st Cav', 'armor', 7, 6, 2, '44_a_fresh.png', '44_a_spent.png'))
    american_units.append(AmericanUnit('44_b', '1st Cav', 'armor', 7, 6, 2, '44_b_fresh.png', '44_b_spent.png'))
    american_units.append(AmericanUnit('44_d', '1st Cav', 'armor', 5, 7, 2, '44_d_fresh.png', '44_d_spent.png'))
    american_units.append(AmericanUnit('302rcn', '1st Cav', 'armor', 3, 8, 2, '302rcn_fresh.png', '302rcn_spent.png'))
    american_units.append(AmericanUnit('637_a', '37th Inf', 'armor', 6, 6, 1, '637_a_fresh.png', '637_a_spent.png'))
    american_units.append(AmericanUnit('637_b', '37th Inf', 'armor', 6, 6, 1, '637_b_fresh.png', '637_b_spent.png'))
    american_units.append(AmericanUnit('637_c', '37th Inf', 'armor', 6, 6, 1, '637_c_fresh.png', '637_c_spent.png'))
    american_units.append(AmericanUnit('754_a', '37th Inf', 'armor', 7, 6, 1, '754_a_fresh.png', '754_a_spent.png', True))
    american_units.append(AmericanUnit('754_b', '1st Cav', 'armor', 7, 6, 2, '754_b_fresh.png', '754_b_spent.png', True))
    american_units.append(AmericanUnit('chase', '1st Cav', 'leader', None, 6, 2, 'chase_fresh.png', 'chase_spent.png', False, True))
    american_units.append(AmericanUnit('fredrick', '37th Inf', 'leader', None, 6, 1, 'fredrick_fresh.png', 'fredrick_spent.png', False, True))
    american_units.append(AmericanUnit('haugen', '11th Air', 'leader', None, 6, 30, 'haugen_fresh.png', 'haugen_spent.png', False, True))
    american_units.append(AmericanUnit('hildenbrand', '11th Air', 'leader', None, 6, [27, 28, 30], 'hildebrand_fresh.png', 'hildebrand_spent.png', True, True))
    american_units.append(AmericanUnit('hoffman', '1st Cav', 'leader', None, 6, 2, 'hoffman_fresh.png', 'hoffman_spent.png', False, True))
    american_units.append(AmericanUnit('soule', '11th Air', 'leader', None, 6, [27, 28, 30], 'soule_fresh.png', 'soule_spent.png', True, True))
    american_units.append(AmericanUnit('whitcomb', '37th Inf', 'leader', None, 6, 1, 'whitcomb_fresh.png', 'whitcomb_spent.png', False, True))
    american_units.append(AmericanUnit('white', '37th Inf', 'leader', None, 6, 1, 'white_fresh.png', 'white_spent.png', False, True))
    
    # create Japanese units
    japanese_units_clear = []
    japanese_units_fort = []
    japanese_units_urban = []

    japanese_units_clear.append(JapaneseUnit('clear', 'ambush', 3, 'clear_ambush_3.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'ambush', 4, 'clear_ambush_4.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'ambush', 5, 'clear_ambush_5.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'ambush', 6, 'clear_ambush_6.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'barrage', 3, 'clear_barrage_3.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'barrage', 4, 'clear_barrage_4.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'barrage', 5, 'clear_barrage_5.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'barrage', 6, 'clear_barrage_6.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'fanatic', 3, 'clear_fanatic_3.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'fanatic', 4, 'clear_fanatic_4.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'fanatic', 5, 'clear_fanatic_5.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'fanatic', 6, 'clear_fanatic_6.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'sniper', 3, 'clear_sniper_3.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'sniper', 4, 'clear_sniper_4.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'sniper', 5, 'clear_sniper_5.png', 'clear_front.png'))
    japanese_units_clear.append(JapaneseUnit('clear', 'sniper', 6, 'clear_sniper_6.png', 'clear_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'ambush', 7, 'fort_ambush_7.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'ambush', 8, 'fort_ambush_8.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'ambush', 9, 'fort_ambush_9.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'ambush', 10, 'fort_ambush_10.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'barrage', 7, 'fort_barrage_7.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'barrage', 8, 'fort_barrage_8.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'barrage', 9, 'fort_barrage_9.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'barrage', 10, 'fort_barrage_10.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'elite', 7, 'fort_elite_7.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'elite', 8, 'fort_elite_8.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'elite', 9, 'fort_elite_9.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'elite', 10, 'fort_elite_10.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'fanatic', 7, 'fort_fanatic_7.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'fanatic', 8, 'fort_fanatic_8.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'fanatic', 9, 'fort_fanatic_9.png', 'fort_front.png'))
    japanese_units_fort.append(JapaneseUnit('fort', 'fanatic', 10, 'fort_fanatic_10.png', 'fort_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 5, 'urban_ambush_5.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 6, 'urban_ambush_6.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 7, 'urban_ambush_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 7, 'urban_ambush_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 8, 'urban_ambush_8.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'ambush', 9, 'urban_ambush_9.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 5, 'urban_barrage_5.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 6, 'urban_barrage_6.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 7, 'urban_barrage_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 7, 'urban_barrage_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 8, 'urban_barrage_8.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'barrage', 9, 'urban_barrage_9.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 5, 'urban_elite_5.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 6, 'urban_elite_6.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 7, 'urban_elite_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 7, 'urban_elite_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 8, 'urban_elite_8.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 9, 'urban_elite_9.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'elite', 10, 'urban_elite_10.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 5, 'urban_fanatic_5.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 6, 'urban_fanatic_6.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 7, 'urban_fanatic_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 7, 'urban_fanatic_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 8, 'urban_fanatic_8.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 9, 'urban_fanatic_9.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'fanatic', 10, 'urban_fanatic_10.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 5, 'urban_sniper_5.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 6, 'urban_sniper_6.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 7, 'urban_sniper_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 7, 'urban_sniper_7.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 8, 'urban_sniper_8.png', 'urban_front.png'))
    japanese_units_urban.append(JapaneseUnit('urban', 'sniper', 9, 'urban_sniper_9.png', 'urban_front.png'))

    support_units = []
    support_units.append(SupportUnit('artillery support', 0, 1, 1, 'artillery_support_front.png', 32, 815))
    support_units.append(SupportUnit('engineer support', 0, 2, 2, 'engineer_support_front.png', 32, 875))

    return american_units, japanese_units_clear, japanese_units_fort, japanese_units_urban, support_units

def create_morale():
    return Morale()

def create_control_marker(x, y):
    return ControlMarker(x, y)

def create_supply():
    return Supply()