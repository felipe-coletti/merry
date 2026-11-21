from effects.blood import Blood
from graphics.skin.blood_skin import BloodSkin
from utils.assets import load_image


class BloodPool(Blood):
    def __init__(self, position):
        skin = BloodSkin(
            load_image("images", "effects", "blood", "blood_pool.png")
        )

        super().__init__(skin, position)
