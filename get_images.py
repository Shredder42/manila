import os
import pygame
def get_images(punch_out, x, y, dimension, side, row, row_length):
    '''
    load punchout image and crop out game pieces from back of the countersheet
    '''
    punchout = pygame.image.load(f'./images/{punch_out}')
    for i in range(row_length):
        piece = punchout.subsurface(x, y, dimension, dimension)
        if row in (2, 4):
            piece = pygame.transform.flip(piece, True, True)
        pygame.image.save(piece, f'./images/{side}_{row}_image_{i+1}.png')
        if (i + 1) % 4 == 0:
            if (i + 1) % 8 == 0:
                x += 20 + dimension
            else:
                x+= 11 + dimension
        else:
            x += dimension



def main():
    # get the images from the countersheet
    x, y = 19, 37
    dimension = 44  # pixel dimensions of playing piece
    for i in range(11):
        get_images('m45_countersback.png', x, y, dimension, 'back', i + 1, 16)
        get_images('m45_countersfront.png', x, y, dimension, 'front', i + 1, 16)
        if (i + 1) % 2 == 0:
            y += dimension + 10
        else:
            y += dimension

if __name__ == '__main__':
    main()


# manually deleted out extras
# renamed outside of python
# (19,37)
# (63,37)
# (19,82)
# (63,82)
# width = 44
# height = 45
# try it at 44x44