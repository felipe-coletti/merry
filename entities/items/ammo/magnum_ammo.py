from entities.items.ammo.ammo import Ammo
from utils.assets import load_image


class MagnumAmmo(Ammo):
    def __init__(self, position, scale=0.5):
        super().__init__(
            image=load_image("images", "items", "ammo", "magnum_ammo.png"),
            position=position,
            scale=scale
        )
