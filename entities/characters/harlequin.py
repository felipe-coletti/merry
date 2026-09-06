import os

from graphics.character_skin import CharacterSkin
from entities.characters.player import Player
from entities.weapons.magnum import Magnum

class Harlequin(Player):
     def __init__(self, position, weapon=None):
        skin = CharacterSkin(
            os.path.join(
                "assets",
                "images",
                "characters",
                "harlequin",
                "harlequin.png"
            )
        )

        if weapon is None:
            weapon = Magnum()
         
        super().__init__(
            skin,
            position,
            weapon
        )