import pygame
from graphics import spritesheet

class Butterfly:
    ADRENALINE_REWARD = 10

    def __init__(self, path, position, scale=0.5, speed=2, health=1):
        image = pygame.image.load(path).convert_alpha()
        sheet = spritesheet.Spritesheet(image)

        butterfly_0 = sheet.get_image(
            0,
            3,
            7,
            42,
            34,
            scale,
            (0, 0, 0)
        )
        
        self.image = butterfly_0

        self.position = pygame.Vector2(position)
        self.speed = speed
        self.health = health

        self.rect = self.image.get_rect(
            center=self.position
        )


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


    def draw(self, screen, camera):
        screen.blit(
            self.image,
            camera.apply(self.rect)
        )