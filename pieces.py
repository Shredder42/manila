import pygame

class AmericanUnit:
    def __init__(self, unit, organization, type, attack, 
                move, setup, unit_fresh_image_filename, unit_spent_image_filename,
                leader = False, reinforcement = False):
        self.unit = unit
        self.organization = organization
        self.type = type
        self.attack = attack
        self.move = move
        self.setup = setup
        self.unit_fresh_image_filename = unit_fresh_image_filename
        self.unit_spent_image_filename = unit_spent_image_filename
        self.leader = leader
        self.reinforcment = reinforcement
        self.fresh_image = self.__load_images()[0]
        self.spent_image = self.__load_images()[1]
        self.fresh = True
        self.rect = self.fresh_image.get_rect()
        self.rect.x = 1400 # x,y coordinates will be updated later
        self.rect.y = 100
        self.moving = False

    def __load_images(self):
        fresh_image = pygame.image.load(f'./images/{self.unit_fresh_image_filename}')
        fresh_image = pygame.transform.smoothscale(fresh_image, (50,50))
        spent_image = pygame.image.load(f'./images/{self.unit_spent_image_filename}')
        spent_image = pygame.transform.smoothscale(spent_image, (50,50))
        return fresh_image, spent_image
    
    def draw(self, surface):
        if self.fresh:
            surface.blit(self.fresh_image, self.rect)
        else:
            surface.blit(self.spent_image, self.rect)

class JapaneseUnit:
    def __init__(self, terrain, strategy, defense, unit_unrevealed_filename, unit_revealed_filename):
        self.terrain = terrain
        self.strategy = strategy
        self.unit_unrevealed_filename = unit_unrevealed_filename
        self.unit_revealed_filename = unit_revealed_filename
        self.unrevealed_image = self.__load_images()[0]
        self.revealed_image = self.__load_images()[1]
        self.defense = defense
        self.revealed = False
        self.rect = self.unrevealed_image.get_rect()
        self.rect.x = 1400 # x,y coordinates will be updated later
        self.rect.y = 200

    def __load_images(self):
        unrevealed_image = pygame.image.load(f'./images/{self.unit_unrevealed_filename}')
        unrevealed_image = pygame.transform.smoothscale(unrevealed_image, (50,50))
        revealed_image = pygame.image.load(f'./images/{self.unit_revealed_filename}')
        revealed_image = pygame.transform.smoothscale(revealed_image, (50,50))
        return unrevealed_image, revealed_image
    
    def draw(self, surface):
        if not self.revealed:
            surface.blit(self.unrevealed_image, self.rect)
        else:
            surface.blit(self.revealed_image, self.rect)