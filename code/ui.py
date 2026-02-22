import pygame
from settings import *
from magic import *

class UI:
    def __init__(self):
        self._display_surface = pygame.display.get_surface()
        self._font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self._health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self._energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self._weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon_image = pygame.image.load(path).convert_alpha()
            self._weapon_graphics.append(weapon_image)

        self._magic_graphics = []
        for magic in magic_data.values():
            if 'graphic' in magic:
                magic_image = pygame.image.load(magic['graphic']).convert_alpha()
                self._magic_graphics.append(magic_image)

    def get_display_surface(self):
        return self._display_surface

    def set_display_surface(self, display_surface):
        self._display_surface = display_surface

    def get_font(self):
        return self._font

    def set_font(self, font):
        self._font = font

    def get_health_bar_rect(self):
        return self._health_bar_rect

    def set_health_bar_rect(self, health_bar_rect):
        self._health_bar_rect = health_bar_rect

	# Fonction récursive
    def display_recursive(self, player, index=0):
        if index == 0:
            self.show_bar(player.health, player.stats['health'], self._health_bar_rect, HEALTH_COLOR)
        elif index == 1:
            self.show_bar(player.energy, player.stats['energy'], self._energy_bar_rect, ENERGY_COLOR)
        elif index == 2:
            self.show_exp(player.exp)
        elif index == 3:
            self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        elif index == 4:
            self.magic_overlay(player.magic_index, not player.can_switch_magic)
        elif index == 5:
            return

        self.display_recursive(player, index + 1)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self._display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self._display_surface, color, current_rect)
        pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self._font.render(str(int(exp)), False, TEXT_COLOR)
        x = self._display_surface.get_size()[0] - 20
        y = self._display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self._display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self._display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self._display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self._display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 680, has_switched)
        weapon_surf = self._weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self._display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(90, 680, has_switched)
        magic_surf = self._magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self._display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self._health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self._energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)