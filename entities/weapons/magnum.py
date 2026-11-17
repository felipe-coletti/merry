from entities.weapons.weapon import Weapon


class Magnum(Weapon):
    def __init__(self):
        super().__init__(
            image=self.load("magnum", "magnum.png"),
            projectile_image=self.load("magnum", "magnum_bullet.png"),
            muzzle_flash_image=self.load("magnum", "magnum_muzzle_flash.png"),
            distance=30,
            projectile_speed=1800,
            projectile_damage=25,
            projectile_scale=0.5,
            muzzle_offset=(37, -7),
            fire_cooldown=550,
            recoil_amount=8,
            recoil_recovery=120
        )
