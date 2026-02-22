import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self._frames = {
            # magie
            'flame': import_folder('images/graphics/particles/flame/frames'),
            'aura': import_folder('images/graphics/particles/aura'),
            'heal': import_folder('images/graphics/particles/heal/frames'),
            
            # attacks 
            'claw': import_folder('images/graphics/particles/claw'),
            'slash': import_folder('images/graphics/particles/slash'),
            'sparkle': import_folder('images/graphics/particles/sparkle'),
            'leaf_attack': import_folder('images/graphics/particles/leaf_attack'),
            'thunder': import_folder('images/graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('images/graphics/particles/smoke_orange'),
            'raccoon': import_folder('images/graphics/particles/raccoon'),
            'spirit': import_folder('images/graphics/particles/nova'),
            'bamboo': import_folder('images/graphics/particles/bamboo'),
            
            # leafs 
            'leaf': (
                import_folder('images/graphics/particles/leaf1'),
                import_folder('images/graphics/particles/leaf2'),
                import_folder('images/graphics/particles/leaf3'),
                import_folder('images/graphics/particles/leaf4'),
                import_folder('images/graphics/particles/leaf5'),
                import_folder('images/graphics/particles/leaf6')
            )
        }

    def get_frames(self):
        return self._frames

    def set_frames(self, frames):
        self._frames = frames

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self._frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self._frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

import pygame
from support import import_folder
from random import choice

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self._frames = animation_frames
        self.sprite_type = 'magic'
        self.frame_index = 0
        self._animation_speed = 0.15
        self.image = self._frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self._animation_speed
        if self.frame_index >= len(self._frames):
            self.kill()
        else:
            self.image = self._frames[int(self.frame_index)]

    def update(self):
        self.animate()

    def get_frames(self):
        return self._frames

    def set_frames(self, frames):
        self._frames = frames

    def get_animation_speed(self):
        return self._animation_speed

    def set_animation_speed(self, animation_speed):
        self._animation_speed = animation_speed

    def set_frame_index(self, frame_index):
        self.frame_index = frame_index