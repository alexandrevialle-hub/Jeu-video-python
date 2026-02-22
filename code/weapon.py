import pygame
from player import Player

class Weapon(pygame.sprite.Sprite): # Agrégat de la class Player
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        full_path = f'images/graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # Placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))

    def get_sprite_type(self):
        return self.sprite_type

    def set_sprite_type(self, sprite_type):
        self.sprite_type = sprite_type

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

def create_weapons(player):
	weapon_data = [
		{'name': 'sword', 'stats': {'cooldown': 150, 'damage': 15, 'graphic': 'images/graphics/weapons/sword1.png'}},
        {'name': 'lance', 'stats': {'cooldown': 250, 'damage': 25, 'graphic': 'images/graphics/weapons/lance1.png'}},
        {'name': 'axe', 'stats': {'cooldown': 200, 'damage': 20, 'graphic': 'images/graphics/weapons/axe1.png'}},
        {'name': 'rapier', 'stats': {'cooldown': 80, 'damage': 8, 'graphic': 'images/graphics/weapons/rapier1.png'}},
		{'name': 'sai', 'stats': {'cooldown': 100, 'damage': 10, 'graphic': 'images/graphics/weapons/sai1.png'}},
		{'name': 'sword2', 'stats': {'cooldown': 125, 'damage': 12.5, 'graphic': 'images/graphics/weapons/sword2.png'}},
		{'name': 'lance2', 'stats': {'cooldown': 200, 'damage': 20, 'graphic': 'images/graphics/weapons/lance2.png'}},
        {'name': 'axe2', 'stats': {'cooldown': 200, 'damage': 20, 'graphic': 'images/graphics/weapons/axe2.png'}},
        {'name': 'rapier2', 'stats': {'cooldown': 70, 'damage': 7, 'graphic': 'images/graphics/weapons/rapier2.png'}},
        {'name': 'sai2', 'stats': {'cooldown': 125, 'damage': 12.5, 'graphic': 'images/graphics/weapons/sai2.png'}},
        {'name': 'sword3', 'stats': {'cooldown': 175, 'damage': 17.5, 'graphic': 'images/graphics/weapons/sword3.png'}},
        {'name': 'lance3', 'stats': {'cooldown': 300, 'damage': 30, 'graphic': 'images/graphics/weapons/lance3.png'}},
        {'name': 'axe3', 'stats': {'cooldown': 200, 'damage': 20, 'graphic': 'images/graphics/weapons/axe3.png'}},
        {'name': 'rapier3', 'stats': {'cooldown': 90, 'damage': 9, 'graphic': 'images/graphics/weapons/rapier3.png'}},
        {'name': 'sai3', 'stats': {'cooldown': 150, 'damage': 15, 'graphic': 'images/graphics/weapons/sai3.png'}},
        {'name': 'sword4', 'stats': {'cooldown': 100, 'damage': 10, 'graphic': 'images/graphics/weapons/sword4'}},
        {'name': 'lance4', 'stats': {'cooldown': 275, 'damage': 22.5, 'graphic': 'images/graphics/weapons/lance4.png'}},
        {'name': 'axe4', 'stats': {'cooldown': 200, 'damage': 20, 'graphic': 'images/graphics/weapons/axe4.png'}},
        {'name': 'rapier4', 'stats': {'cooldown': 100, 'damage': 10, 'graphic': 'images/graphics/weapons/rapier4.png'}},
        {'name': 'sai4', 'stats': {'cooldown': 75, 'damage': 7.5, 'graphic': 'images/graphics/weapons/sai4.png'}},
        ]
	
	weapons = []
	for weapon_info in weapon_data:
		weapon_name = weapon_info['name']
		weapon_stats = weapon_info['stats']
		weapon_instance = Weapon(player, weapon_name, weapon_stats)
		weapons.append(weapon_instance)
	return weapons