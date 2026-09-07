import pygame

class Butterfly:
    ADRENALINE_REWARD = 10

    def __init__(self, skin, position, speed=2, health=1):
        self.skin = skin

        frame = self.skin.frames[0]

        self.position = pygame.Vector2(position)
        self.rect = frame.get_rect(center=self.position)
        
        self.frame_index = 0
        self.animation_speed = 0.15

        self.speed = speed
        self.health = health


    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.skin.frames):
            self.frame_index = 0


    def take_damage(self, damage):
        if self.health > damage:
            self.health -= damage
        else:
            self.health = 0


    def update(self, target):
        direction = pygame.Vector2(target) - self.position

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.position += direction * self.speed

        self.rect.center = self.position

        self.animate()


    def draw(self, screen, camera):
        frame = self.skin.frames[int(self.frame_index)]

        rect = frame.get_rect(
            center=self.rect.center
        )

        rect = camera.apply(rect)

        screen.blit(frame, rect)