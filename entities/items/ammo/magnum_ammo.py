import os

from entities.items.ammo.ammo import Ammo

class MagnumAmmo(Ammo):
    def __init__(self, position, scale=0.5):
        magnum_ammo_image_path = os.path.join(
            "assets",
            "images",
            "items",
            "ammo",
            "magnum_ammo.png"
        )

        super().__init__(
            image_path=magnum_ammo_image_path,
            position=position,
            scale=scale
        )