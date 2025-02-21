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
        self.rect.x = 1400
        self.rect.y = 100
        self.moving = False

    def __load_images(self):
        fresh_image = pygame.image.load(f'./images/{self.unit_fresh_image_filename}')
        spent_image = pygame.image.load(f'./images/{self.unit_spent_image_filename}')
        return fresh_image, spent_image
    
    def draw(self, surface):
        surface.blit(self.fresh_image, self.rect)