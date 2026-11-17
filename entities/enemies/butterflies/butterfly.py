import pygame

from entities.enemies.enemy import Enemy


class Butterfly(Enemy):
    DAMAGE = 10
    ADRENALINE_REWARD = 10

    def __init__(self, skin, position, speed=120, health=1, animation_fps=9):
        """speed: pixels por segundo."""
        super().__init__()

        self.skin = skin

        self.position = pygame.Vector2(position)
        self.rect = self.skin.frames[0].get_rect(center=self.position)

        self.frame_index = 0
        self.animation_fps = animation_fps

        self.speed = speed
        self.health = health

    def animate(self, dt):
        self.frame_index = (
            self.frame_index + self.animation_fps * dt
        ) % len(self.skin.frames)

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def damages_player(self, player):
        return self.rect.colliderect(player.rect)

    @property
    def dead(self):
        return self.health <= 0

    def update(self, target, dt, level):
        direction = pygame.Vector2(target) - self.position

        if direction.length_squared() > 0:
            self.position += direction.normalize() * self.speed * dt

        self.rect.center = self.position

        self.animate(dt)

    def draw(self, screen, camera):
        frame = self.skin.frames[int(self.frame_index)]

        rect = frame.get_rect(center=self.rect.center)

        screen.blit(frame, camera.apply(rect))
