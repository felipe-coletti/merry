import os

from graphics.skin.blood_skin import BloodSkin
from effects.blood import Blood

class BloodPool(Blood):
    def __init__(self, position):
        skin = BloodSkin(
            os.path.join(
                "assets",
                "images",
                "effects",
                "blood",
                "blood_pool.png"
            )
        )

        super().__init__(
            skin,
            position
        )