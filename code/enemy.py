import pygame
from settings import *
from entity import Entity
import csv
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.__monster_name = monster_name
        self.status = 'idle'

        # Graphics setup
        self.animations = {'idle': [], 'move': [], 'attack': []}

        main_path = f'images/graphics/monsters/{self.__monster_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

        self.image = self.animations[self.status][self.frame_index]

        # Mouvement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        monster_info = None
        for monster in monster_data:
            if monster['name'] == self.__monster_name:
                monster_info = monster
        if monster_info is not None:
            self.health = monster_info['health']
            self.exp = monster_info['exp']
            self.speed = monster_info['speed']
            self.attack_damage = monster_info['damage']
            self.resistance = monster_info['resistance']
            self.attack_radius = monster_info['attack_radius']
            self.notice_radius = monster_info['notice_radius']
            self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        self.death_sound = pygame.mixer.Sound('song/death.wav')
        self.hit_sound = pygame.mixer.Sound('song/hit.wav')
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)

    def get_monster_name(self):
        return self.__monster_name

    def get_animations(self):
        return self.animations

    def set_attack_cooldown(self, cooldown):
        self.attack_cooldown = cooldown

    def set_resistance(self, resistance):
        self.resistance = resistance

    def set_attack_radius(self, attack_radius):
        self.attack_radius = attack_radius

    def import_graphics(self, name):
        main_path = f'images/graphics/monsters/{self.__monster_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.__monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

monster_data = [
    {'name': 'squid', 'health': 100, 'exp': 100, 'damage': 15, 'attack_type': 'slash', 'attack_sound': 'song/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    {'name': 'gojo', 'health': 300, 'exp': 350, 'damage': 40, 'attack_type': 'claw', 'attack_sound': 'song/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    {'name': 'spirit', 'health': 100, 'exp': 110, 'damage': 12, 'attack_type': 'thunder', 'attack_sound': 'song/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'bamboo', 'health': 70, 'exp': 120, 'damage': 10, 'attack_type': 'leaf_attack', 'attack_sound': 'song/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    {'name': 'squid2', 'health': 120, 'exp': 100, 'damage': 15, 'attack_type': 'slash', 'attack_sound': 'song/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    {'name': 'blue_spirit', 'health': 100, 'exp': 100, 'damage': 12, 'attack_type': 'claw', 'attack_sound': 'song/attack/claw.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'green_spirit', 'health': 100, 'exp': 110, 'damage': 12, 'attack_type': 'thunder', 'attack_sound': 'song/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'bamboo2', 'health': 70, 'exp': 120, 'damage': 10, 'attack_type': 'leaf_attack', 'attack_sound': 'song/attack/slash.wav', 'speed': 4, 'resistance': 2, 'attack_radius': 50, 'notice_radius': 300},
    {'name': 'squid3', 'health': 90, 'exp': 100, 'damage': 18, 'attack_type': 'slash', 'attack_sound': 'song/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    {'name': 'gojo3', 'health': 300, 'exp': 350, 'damage': 40, 'attack_type': 'claw', 'attack_sound': 'song/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    {'name': 'rose_spirit', 'health': 100, 'exp': 110, 'damage': 12, 'attack_type': 'thunder', 'attack_sound': 'song/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'bamboo3', 'health': 100, 'exp': 120, 'damage': 14, 'attack_type': 'leaf_attack', 'attack_sound': 'song/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    {'name': 'squid4', 'health': 75, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound': 'song/attack/slash.wav', 'speed': 3.5, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    {'name': 'raccoon', 'health': 300, 'exp': 350, 'damage': 40, 'attack_type': 'claw', 'attack_sound': 'song/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    {'name': 'violet_spirit', 'health': 100, 'exp': 110, 'damage': 12, 'attack_type': 'thunder', 'attack_sound': 'song/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'bamboo4', 'health': 60, 'exp': 120, 'damage': 11, 'attack_type': 'leaf_attack', 'attack_sound': 'song/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    {'name': 'squid5', 'health': 110, 'exp': 100, 'damage': 12, 'attack_type': 'slash', 'attack_sound': 'song/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    {'name': 'raccoon2', 'health': 400, 'exp': 350, 'damage': 35, 'attack_type': 'claw', 'attack_sound': 'song/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    {'name': 'yellow_spirit', 'health': 100, 'exp': 110, 'damage': 12, 'attack_type': 'thunder', 'attack_sound': 'song/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    {'name': 'bamboo5', 'health': 75, 'exp': 120, 'damage': 12, 'attack_type': 'leaf_attack', 'attack_sound': 'song/attack/slash.wav', 'speed': 3.5, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
]