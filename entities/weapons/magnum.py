import os

from entities.weapons.weapon import Weapon

class Magnum(Weapon):
    def __init__(self):
        magnum_image_path = os.path.join(
            "assets",
            "images",
            "weapons",
            "magnum",
            "magnum.png"
        )

        magnum_projectile_image_path = os.path.join(
            "assets",
            "images",
            "weapons",
            "magnum",
            "magnum_bullet.png"
        )

        magnum_muzzle_flash_image_path = os.path.join(
            "assets",
            "images",
            "weapons",
            "magnum",
            "magnum_muzzle_flash.png"
        )

        super().__init__(
            image_path=magnum_image_path,
            projectile_image_path=magnum_projectile_image_path,
            muzzle_flash_image_path=magnum_muzzle_flash_image_path,
            distance=30,
            projectile_speed=30,
            projectile_scale=0.5,
            muzzle_offset=(37, -7),
            fire_cooldown=550,
            recoil_amount=8,
            recoil_recovery=2
        )