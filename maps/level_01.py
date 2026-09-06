import pygame

from maps.level import Level

from entities.enemies.butteflies.cyan_butterfly import CyanButterfly
from entities.items.ammo.magnum_ammo import MagnumAmmo

class Level01(Level):
    def __init__(self):
        super().__init__(
            size=(1600, 1200),

            player_spawn=(400, 300),

            floor_areas=[
                pygame.Rect(100, 100, 600, 400),
                pygame.Rect(500, 300, 500, 200),
                pygame.Rect(900, 150, 500, 500),
            ],

            obstacles=[
                pygame.Rect(300, 200, 100, 40),
                pygame.Rect(500, 350, 40, 120),
            ],

            enemies=[
                (CyanButterfly, (600, 300)),
                (CyanButterfly, (200, 400)),
            ],

            ammo=[
                (MagnumAmmo, (100, 100)),
                (MagnumAmmo, (1000, 400)),
            ]
        )