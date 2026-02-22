import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self._y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, self._y_offset)

    def get_sprite_type(self):
        return self.sprite_type

    def set_sprite_type(self, sprite_type):
        self.sprite_type = sprite_type

    def get_y_offset(self):
        return self._y_offset

    def set_y_offset(self, y_offset):
        self._y_offset = y_offset

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image