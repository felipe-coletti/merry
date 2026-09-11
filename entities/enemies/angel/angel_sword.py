import math
import pygame


class AngelSword:
    DAMAGE = 20

    SCALE = 1.25

    ORBIT_RADIUS = 85
    ORBIT_SPEED = 2

    FLOAT_HEIGHT = 35
    FALL_SPEED = 2

    def __init__(
        self,
        image,
        center,
        angle,
        rotation_direction
    ):
        self.image = pygame.transform.scale(
            image,
            (
                round(image.get_width() * self.SCALE),
                round(image.get_height() * self.SCALE)
            )
        )

        self.center = pygame.Vector2(center)

        self.angle = angle
        self.rotation_direction = rotation_direction

        self.position = pygame.Vector2(center)

        self.height = self.FLOAT_HEIGHT

        self.falling = False
        self.grounded = False

        self.current_image = self.image
        self.mask = pygame.mask.from_surface(self.current_image)

        self.rect = self.current_image.get_rect(
            center=self.position
        )

        self.update_orbit(center)

    def update_orbit(self, center):
        self.center = pygame.Vector2(center)

        self.angle += self.ORBIT_SPEED * self.rotation_direction

        radians = math.radians(self.angle)

        self.position = pygame.Vector2(
            self.center.x + math.cos(radians) * self.ORBIT_RADIUS,
            self.center.y + math.sin(radians) * self.ORBIT_RADIUS
        )

        self.update_visual()

    def update_visual(self):
        rotation = -self.angle - 90

        self.current_image = pygame.transform.rotate(
            self.image,
            rotation
        )

        self.mask = pygame.mask.from_surface(
            self.current_image
        )

        if self.falling or self.grounded:
            visual_position = (
                self.position.x,
                self.position.y - self.height
            )
        else:
            visual_position = self.position

        self.rect = self.current_image.get_rect(
            center=visual_position
        )

    def release(self):
        if self.falling or self.grounded:
            return

        self.falling = True

    def update(self):
        if not self.falling or self.grounded:
            return

        self.height -= self.FALL_SPEED

        if self.height <= 0:
            self.height = 0
            self.falling = False
            self.grounded = True

        self.update_visual()

    def collides_with(self, other_rect, other_mask):
        offset = (
            other_rect.left - self.rect.left,
            other_rect.top - self.rect.top
        )

        return self.mask.overlap(
            other_mask,
            offset
        )

    def damages_player(self, player):
        if not player.moved:
            return False
    
        return self.collides_with(
            player.rect,
            player.mask
        )

    def draw_mask(self, screen, camera):
        mask_surface = self.mask.to_surface(
            setcolor=(255, 0, 0, 150),
            unsetcolor=(0, 0, 0, 0)
        )

        rect = camera.apply(self.rect)
        screen.blit(mask_surface, rect)

    def draw(self, screen, camera):
        rect = camera.apply(self.rect)
        screen.blit(self.current_image, rect)