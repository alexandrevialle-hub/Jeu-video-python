import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        self._display_surface = pygame.display.get_surface()
        self._player = player

        self._attribute_nr = len(player.stats)
        self._attribute_names = list(player.stats.keys())
        self._max_values = list(player.max_stats.values())
        self._font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self._height = self._display_surface.get_size()[1] * 0.8
        self._width = self._display_surface.get_size()[0] // 6
        self._create_items()

        self._selection_index = 0
        self._selection_time = None
        self._can_move = True

    def get_selection_index(self):
        return self._selection_index

    def set_selection_index(self, selection_index):
        self._selection_index = selection_index
	
    def get_selection_time(self):
        return self._selection_time

    def set_selection_time(self, selection_time):
        self._selection_time = selection_time

    def get_can_move(self):
        return self._can_move

    def set_can_move(self, can_move):
        self._can_move = can_move

    def input(self):
        keys = pygame.key.get_pressed()

        if self._can_move:
            if keys[pygame.K_RIGHT] and self._selection_index < self._attribute_nr - 1:
                self._selection_index += 1
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self._selection_index >= 1:
                self._selection_index -= 1
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self._can_move = False
                self._selection_time = pygame.time.get_ticks()
                self._item_list[self._selection_index].trigger(self._player)

    def selection_cooldown(self):
        if not self._can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self._selection_time >= 300:
                self._can_move = True

    def _create_items(self):
        self._item_list = []

        for item, index in enumerate(range(self._attribute_nr)):
            full_width = self._display_surface.get_size()[0]
            increment = full_width // self._attribute_nr
            left = (item * increment) + (increment - self._width) // 2

            top = self._display_surface.get_size()[1] * 0.1

            item = Item(left, top, self._width, self._height, index, self._font)
            self._item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self._item_list):
            name = self._attribute_names[index]
            value = self._player.get_value_by_index(index)
            max_value = self._max_values[index]
            cost = self._player.get_cost_by_index(index)
            item.display(self._display_surface, self._selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, l, t, w, h, index, font):
        self._rect = pygame.Rect(l, t, w, h)
        self._index = index
        self._font = font

    def get_rect(self):
        return self._rect

    def set_rect(self, rect):
        self._rect = rect

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_font(self):
        return self._font

    def set_font(self, font):
        self._font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self._font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self._rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surf = self._font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self._rect.midbottom - pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self._rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self._rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # draw elements
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self._index]

        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self._index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self._rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self._rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self._rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self._rect, 4)

        self.display_names(surface, name, cost, self._index == selection_num)
        self.display_bar(surface, value, max_value, self._index == selection_num)