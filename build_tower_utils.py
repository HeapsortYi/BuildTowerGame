import pygame
import sys


def load_resource():
    SOUNDS = {}
    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['perfect'] = pygame.mixer.Sound('assets/audio/perfect' + soundExt)
    SOUNDS['good'] = pygame.mixer.Sound('assets/audio/good' + soundExt)
    SOUNDS['normal'] = pygame.mixer.Sound('assets/audio/normal' + soundExt)

    IMAGES_BKG = pygame.image.load('assets/sprites/background.png').convert()

    return SOUNDS, IMAGES_BKG