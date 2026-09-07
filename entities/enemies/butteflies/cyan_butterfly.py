import os

from entities.enemies.butteflies.butterfly import Butterfly
from graphics.butterfly_skin import ButterflySkin

class CyanButterfly(Butterfly):
    def __init__(self, position, scale=2):
        butterfly_skin = ButterflySkin(
            os.path.join(
                "assets",
                "images",
                "enemies",
                "butterfly",
                "cyan_butterfly.png"
            ),
            scale=scale
        )

        super().__init__(
            butterfly_skin,
            position,
            scale
        )