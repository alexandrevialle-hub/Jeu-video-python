import pygame
import sys
import csv
from settings import *
from support import import_folder
from entity import Entity
from magic import *

pygame.mixer.init()
player_death_sound = pygame.mixer.Sound('song/player_death.wav')

def get_kashimo_stats(image_path):
        with open('code/player.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['image_path'] == image_path:
                    return {
                        'health': int(row['health']),
                        'energy': int(row['energy']),
                        'attack': int(row['attack']),
                        'magic': int(row['magic']),
                        'speed': int(row['speed'])
                    }

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('images/graphics/player/kashimo.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        self.weapon_order = ['sword', 'lance', 'axe', 'rapier', 'sai']
        self.weapon_index = 0
        self.weapon = self.weapon_order[self.weapon_index]
        self.max_weapon_index = 4
        self.max_magic_index = 1

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # mouvement
        self.attacking = False
        self._attack_cooldown = 400
        self._attack_time = None
        self._obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magie
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats  Il suffit de rajouter après kashimo un numéro entre 2 et 20 si on veut changer les stats du joueur
        kashimo_stats = get_kashimo_stats('images/graphics/player/kashimo.png')
        self.stats = kashimo_stats
        self.max_stats = {'health': 1000, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 60}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 100
        self.speed = self.stats['speed']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.weapon_attack_sound = pygame.mixer.Sound('song/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)
	
    def get_attack_cooldown(self):
        return self._attack_cooldown

    def set_attack_cooldown(self, attack_cooldown):
        self._attack_cooldown = attack_cooldown
	
    def get_attack_time(self):
        return self._attack_time

    def set_attack_time(self, attack_time):
        self._attack_time = attack_time
	
    def get_obstacle_sprites(self):
        return self._obstacle_sprites

    def set_obstacle_sprites(self, obstacle_sprites):
        self._obstacle_sprites = obstacle_sprites
    
    def __add__(self, strength):
        self.player.health += strength

    def __sub__(self, cost):
        self.player.energy -= cost
	
	# Agrège la class Weapon
    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def remove_weapon(self, weapon):
        self.weapons.remove(weapon)

    def import_player_assets(self):
        character_path = 'images/graphics/player/'
        self._frames = {'up': [], 'down': [], 'left': [], 'right': [],
                        'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                        'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self._frames.keys():
            full_path = character_path + animation
            self._frames[animation] = import_folder(full_path)
    
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self._direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self._direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            def circular_increment(index, max_value):
                return (index + 1) % max_value
			
            def circular_decrement(index, max_value):
                return (index - 1) % max_value
			
            # Algorithme de tri
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(self.weapon_order)
                self.weapon = self.weapon_order[self.weapon_index]
			
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index = (self.magic_index + 1) % (self.max_magic_index + 1)
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        if self._direction.x == 0 and self._direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self._direction.x = 0
            self._direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self._attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self._frames[self.status]

        self._frame_index += self._animation_speed
        if self._frame_index >= len(animation):
            self._frame_index = 0

        self.image = animation[int(self._frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
        if self.health <= 0:
            player_death_sound.play()
            pygame.time.delay(2000)
            sys.exit()