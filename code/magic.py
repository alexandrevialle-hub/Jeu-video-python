import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self._animation_player = animation_player
        self._sounds = {
            'heal': pygame.mixer.Sound('song/heal.wav'),
            'flame': pygame.mixer.Sound('song/Fire.wav')
        }

    def get_animation_player(self):
        return self._animation_player

    def set_animation_player(self, animation_player):
        self._animation_player = animation_player

    def get_sounds(self):
        return self._sounds

    def set_sounds(self, sounds):
        self._sounds = sounds

    def set_animation_speed(self, speed):
        self._animation_speed = speed

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self._sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self._animation_player.create_particles('aura', player.rect.center, groups)
            self._animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self._sounds['flame'].play()

            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self._animation_player.create_particles('flame', (x, y), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self._animation_player.create_particles('flame', (x, y), groups)

magic_data = {  # Vous pouvez rajouter un chiffre entre 2 et 10 après fire et/ou heal avant le .png de la ligne 65 et 66 dans le lien de l'image pour modifier l'image
	'flame': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal.png'},
    'flame2': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire2.png'},
	'heal2' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal2.png'},
    'flame3': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire3.png'},
	'heal3' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal3.png'},
    'flame4': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire4.png'},
	'heal4' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal4.png'},
    'flame5': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire5.png'},
	'heal5' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal5.png'},
    'flame6': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire6.png'},
	'heal6' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal6.png'},
    'flame7': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire7.png'},
	'heal7' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal7.png'},
    'flame8': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire8.png'},
	'heal8' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal8.png'},
    'flame9': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire9.png'},
	'heal9' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal9.png'},
    'flame10': {'strength': 20,'cost': 20,'graphic':'images/graphics/particles/flame/fire10.png'},
	'heal10' : {'strength': 20,'cost': 10,'graphic':'images/graphics/particles/heal/heal10.png'}}