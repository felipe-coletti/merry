import os

from entities.enemies.butteflies.butterfly import Butterfly

class CyanButterfly(Butterfly):
    def __init__(self, position, scale=1):
        butterfly_image = os.path.join(
            "assets",
            "images",
            "enemies",
            "butterfly",
            "butterfly.png"
        )

        super().__init__(butterfly_image, position, scale=scale)