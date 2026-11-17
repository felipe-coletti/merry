from entities.characters.player import Player
from entities.weapons.magnum import Magnum
from graphics.skin.character_skin import CharacterSkin
from utils.assets import load_image


class Merry(Player):
    def __init__(self, position, weapon=None):
        skin = CharacterSkin(
            load_image("images", "characters", "merry", "merry.png")
        )

        if weapon is None:
            weapon = Magnum()

        super().__init__(skin, position, weapon)
