import pygame
import sys
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):
        self._game_paused = False

        def get_game_paused(self):
            return self._game_paused

        def set_game_paused(self, game_paused):
            self._game_paused = game_paused

        self.game_paused = property(get_game_paused, set_game_paused)

        # Sprite group setup
        self._visible_sprites = YSortCameraGroup()
        self._obstacle_sprites = pygame.sprite.Group()

        # Attack sprites
        self._current_attack = None
        self._attack_sprites = pygame.sprite.Group()
        self._attackable_sprites = pygame.sprite.Group()

        # Sprite setup
        self._create_map()

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def set_game_paused(self, game_paused):
        self._game_paused = game_paused

    def get_current_attack(self):
        return self._current_attack

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self._visible_sprites])

    def get_add_exp(self, amount):
        return self.player.exp

    def set_add_exp(self, amount):
        self.player.exp += amount

    def _create_map(self):
        layouts = {
            'boundary': import_csv_layout('images/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('images/map/map_Grass.csv'),
            'object': import_csv_layout('images/map/map_Objects.csv'),
            'entities': import_csv_layout('images/map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('images/grass'),
            'objects': import_folder('images/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self._obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y),
                                [self._visible_sprites, self._obstacle_sprites, self._attackable_sprites],
                                'grass',
                                random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self._visible_sprites, self._obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y),
                                    [self._visible_sprites],
                                    self._obstacle_sprites,
                                    self._create_attack,
                                    self._destroy_attack,
                                    self._create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self._visible_sprites, self._attackable_sprites],
                                    self._obstacle_sprites,
                                    self.damage_player,
                                    self._trigger_death_particles,
                                    self.set_add_exp)

    def _create_attack(self):
        self._current_attack = Weapon(self.player, [self._visible_sprites, self._attack_sprites])

    def _create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self._visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self._visible_sprites, self._attack_sprites])

    def _destroy_attack(self):
        if self._current_attack:
            self._current_attack.kill()
        self._current_attack = None

    def _player_attack_logic(self):
        if self._attack_sprites:
            for attack_sprite in self._attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self._attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self._visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def _trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self._visible_sprites)
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.toggle_menu()

        self._visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self._visible_sprites.update()
            self._visible_sprites.enemy_update(self.player)
            self._player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self._half_width = self.display_surface.get_size()[0] // 2
        self._half_height = self.display_surface.get_size()[1] // 2
        self._offset = pygame.math.Vector2()

        # Création du sol
        self.floor_surf = pygame.image.load('images/map1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def get_half_width(self):
        return self._half_width

    def set_half_width(self, half_width):
        self._half_width = half_width

    def get_half_height(self):
        return self._half_height

    def set_half_height(self, half_height):
        self._half_height = half_height

    def set_offset(self, offset):
        self._offset = offset

    def get_offset(self):
        return self._offset

    def custom_draw(self, player):
        offset_x = player.rect.centerx - self._half_width
        offset_y = player.rect.centery - self._half_height

        floor_offset_pos = self.floor_rect.topleft - pygame.math.Vector2(offset_x, offset_y)
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_x, offset_y)
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)