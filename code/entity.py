import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self._frame_index = 0
        self._animation_speed = 0.15
        self._direction = pygame.math.Vector2()
        self._obstacle_sprites = pygame.sprite.Group()

    @property
    def frame_index(self):
        return self._frame_index

    @frame_index.setter
    def frame_index(self, value):
        self._frame_index = value

    @property
    def animation_speed(self):
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, value):
        self._animation_speed = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def obstacle_sprites(self):
        return self._obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, value):
        self._obstacle_sprites = value

    def move(self, speed):
        if self._direction.magnitude() != 0:
            self._direction = self._direction.normalize()

        self.hitbox.x += self._direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self._direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self._obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self._direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self._direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self._obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self._direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self._direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0