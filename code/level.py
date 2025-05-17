#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
from idlelib.calltip import get_entity
from random import choice

import pygame
import os
import pygame
import self
from pygame import Surface, Rect
from pygame.font import Font

from code import EntityMediator
from code.Const import COLOR_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME
from code.enemy import Enemy
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.player import Player


def should_remove(ent):
    pass


class Level:
    def __init__(self, window, name, game_mode):
        self.timeout = 20000  # 20 segundos
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Player1'))
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2'))
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def _should_remove(self, ent):
        # Remove tiros que saíram da tela
        if 'Shot' in ent.name:
            # Tiro de jogador sobe, então remove se saiu por cima
            if 'Player' in ent.name and ent.rect.bottom < 0:
                return True
            # Tiro de inimigo desce, então remove se saiu por baixo
            if 'Enemy' in ent.name and ent.rect.top > WIN_HEIGHT:
                return True

        # Remove inimigos mortos ou fora da tela
        if isinstance(ent, Enemy):
            if ent.health <= 0 or ent.rect.top > WIN_HEIGHT:
                return True

        return False


    def run(self):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            # Limpa entidades que saíram da tela ou morreram
            self.entity_list = [ent for ent in self.entity_list if not self._should_remove(ent)]

            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            # Atualiza e desenha entidades
            for ent in self.entity_list:
                ent.move()
                self.window.blit(ent.surf, ent.rect)

                # Se for Player ou Enemy, tenta atirar
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # Desenha texto informativo
            self.level_text(text_size=14, text=f'{self.name} - Timeout: {self.timeout / 1000:1f}s',
                            text_color=COLOR_WHITE, text_pos=(10, 5))
            self.level_text(text_size=14, text=f'fps: {clock.get_fps():.0f}', text_color=COLOR_WHITE,
                            text_pos=(10, WIN_HEIGHT - 35))
            self.level_text(text_size=14, text=f'entidades: {len(self.entity_list)}', text_color=COLOR_WHITE,
                            text_pos=(10, WIN_HEIGHT - 20))

            # Colisões e verificação de vida
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            # Atualiza a tela apenas uma vez por frame
            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name='Lucida Sans Typewriter', size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
