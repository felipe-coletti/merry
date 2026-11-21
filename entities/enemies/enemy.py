class Enemy:
    #Interface comum a todos os inimigos usada pelo Game.

    DAMAGE = 0
    ADRENALINE_REWARD = 0

    def __init__(self):
        self.released_objects = []

    @property
    def projectile_blockers(self):
        # Objetos que param projéteis antes de atingirem o inimigo.
        return []

    @property
    def dead(self):
        raise NotImplementedError

    def take_damage(self, damage):
        raise NotImplementedError

    def damages_player(self, player):
        return False

    def attack(self, player, dt):
        if self.damages_player(player):
            player.take_damage(self.DAMAGE)

    def pop_released_objects(self):
        released = self.released_objects
        self.released_objects = []

        return released

    def update(self, target, dt, level):
        pass

    def draw(self, screen, camera):
        pass
