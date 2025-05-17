from abc import ABC

from code.Const import ENTITY_SPEED
from code.entity import Entity


class PlayerShot(Entity, ABC):


    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx += ENTITY_SPEED[self.name]

