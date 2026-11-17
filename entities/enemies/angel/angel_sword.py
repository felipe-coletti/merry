import math

import pygame


class AngelSword:
    DAMAGE = 20

    SCALE = 1.25

    ORBIT_RADIUS = 85
    ORBIT_SPEED = 120  # graus por segundo

    FLOAT_HEIGHT = 35
    FALL_SPEED = 120  # pixels por segundo

    def __init__(self, image, center, angle, rotation_direction):
        self.image = pygame.transform.scale_by(image, self.SCALE)

        self.center = pygame.Vector2(center)

        self.angle = angle
        self.rotation_direction = rotation_direction

        self.position = pygame.Vector2(center)

        self.height = self.FLOAT_HEIGHT

        self.falling = False
        self.grounded = False

        self.update_orbit(center, 0)

    @property
    def released(self):
        return self.falling or self.grounded

    def update_orbit(self, center, dt):
        self.center = pygame.Vector2(center)

        self.angle += self.ORBIT_SPEED * self.rotation_direction * dt

        radians = math.radians(self.angle)

        self.position = pygame.Vector2(
            self.center.x + math.cos(radians) * self.ORBIT_RADIUS,
            self.center.y + math.sin(radians) * self.ORBIT_RADIUS
        )

        self.update_visual()

    def update_visual(self):
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
