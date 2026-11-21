from entities.enemies.butterflies.butterfly import Butterfly
from graphics.skin.butterfly_skin import ButterflySkin
from utils.assets import load_image


class CyanButterfly(Butterfly):
    def __init__(self, position, scale=2):
        skin = ButterflySkin(
            load_image("images", "enemies", "butterfly", "cyan_butterfly.png"),
            scale=scale
        )

        super().__init__(skin, position)
