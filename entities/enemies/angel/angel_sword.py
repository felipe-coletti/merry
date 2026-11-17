import math

import pygame

from utils.angles import approach_angle


class AngelSword:
    DAMAGE = 20

    SCALE = 1.25

    ORBIT_RADIUS = 85
    ORBIT_SPEED = 120  # graus por segundo

    # Ataque ativo (estocada).
    AIM_SPEED = 240  # graus por segundo ao girar para mirar no jogador
    LOCK_TIME = 400  # ms parada apontando antes de estocar
    STAB_DISTANCE = 110  # quanto a espada avança além da órbita
    STAB_SPEED = 900  # pixels por segundo
    RETRACT_SPEED = 300  # pixels por segundo
    RETURN_SPEED = 360  # graus por segundo ao voltar para a sua vaga

    FLOAT_HEIGHT = 35
    FALL_SPEED = 120  # pixels por segundo

    ATTACK_STATES = ("aiming", "locked", "stabbing", "retracting", "returning")

    def __init__(self, image, center, angle, rotation_direction):
        self.image = pygame.transform.scale_by(image, self.SCALE)

        self.center = pygame.Vector2(center)

        # slot_angle é onde a espada deveria estar na órbita; ele continua
        # girando durante o ataque para a espada saber para onde voltar.
        self.slot_angle = angle
        self.angle = angle
        self.radius = self.ORBIT_RADIUS
        self.rotation_direction = rotation_direction

        self.state = "orbiting"
        self.state_start = 0

        self.position = pygame.Vector2(center)

        self.height = self.FLOAT_HEIGHT

        self.falling = False
        self.grounded = False

        self.update_orbit(center, center, 0)

    @property
    def released(self):
        return self.falling or self.grounded

    @property
    def attacking(self):
        return self.state in self.ATTACK_STATES

    @property
    def length(self):
        return self.image.get_height()

    def start_attack(self):
        if self.state == "orbiting":
            self._change_state("aiming")

    def _change_state(self, state):
        self.state = state
        self.state_start = pygame.time.get_ticks()

    def _update_attack(self, target, dt):
        if self.state == "aiming":
            offset = pygame.Vector2(target) - self.center

            if offset.length_squared() > 0:
                target_angle = math.degrees(math.atan2(offset.y, offset.x))

                self.angle, aimed = approach_angle(
                    self.angle,
                    target_angle,
                    self.AIM_SPEED * dt
                )

                if aimed:
                    self._change_state("locked")

        elif self.state == "locked":
            if pygame.time.get_ticks() - self.state_start >= self.LOCK_TIME:
                self._change_state("stabbing")

        elif self.state == "stabbing":
            self.radius += self.STAB_SPEED * dt

            if self.radius >= self.ORBIT_RADIUS + self.STAB_DISTANCE:
                self.radius = self.ORBIT_RADIUS + self.STAB_DISTANCE
                self._change_state("retracting")

        elif self.state == "retracting":
            self.radius -= self.RETRACT_SPEED * dt

            if self.radius <= self.ORBIT_RADIUS:
                self.radius = self.ORBIT_RADIUS
                self._change_state("returning")

        elif self.state == "returning":
            self.angle, arrived = approach_angle(
                self.angle,
                self.slot_angle,
                self.RETURN_SPEED * dt
            )

            if arrived:
                self._change_state("orbiting")

    def update_orbit(self, center, target, dt):
        self.center = pygame.Vector2(center)

        self.slot_angle += self.ORBIT_SPEED * self.rotation_direction * dt

        if self.state == "orbiting":
            self.angle = self.slot_angle
        else:
            self._update_attack(target, dt)

        radians = math.radians(self.angle)

        self.position = pygame.Vector2(
            self.center.x + math.cos(radians) * self.radius,
            self.center.y + math.sin(radians) * self.radius
        )

        self.update_visual()

    def update_visual(self):
        # O sprite aponta para cima; esta rotação deixa a ponta virada
        # para fora da órbita.
        self.current_image = pygame.transform.rotate(
            self.image,
            -self.angle - 90
        )

        self.mask = pygame.mask.from_surface(self.current_image)

        if self.released:
            visual_position = (
                self.position.x,
                self.position.y - self.height
            )
        else:
            visual_position = self.position

        self.rect = self.current_image.get_rect(center=visual_position)

    def release(self):
        if self.released:
            return

        self.state = "released"
        self.falling = True

    def update(self, dt):
        if not self.falling:
            return

        self.height -= self.FALL_SPEED * dt

        if self.height <= 0:
            self.height = 0
            self.falling = False
            self.grounded = True

        # A imagem não gira durante a queda: só a posição muda.
        self.rect.center = (
            self.position.x,
            self.position.y - self.height
        )

    def collides_with(self, other_rect, other_mask):
        offset = (
            other_rect.left - self.rect.left,
            other_rect.top - self.rect.top
        )

        return self.mask.overlap(other_mask, offset) is not None

    def touches_player(self, player):
        return self.collides_with(player.rect, player.mask)

    def damages_player(self, player):
        # Espadas soltas só ferem quem se move sobre elas.
        if not player.moved:
            return False

        return self.touches_player(player)

    def draw(self, screen, camera):
        screen.blit(self.current_image, camera.apply(self.rect))
