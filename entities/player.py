import pygame

from entities.character import Character

class Player(Character):
    def __init__(self, skin, position, weapon, bounds):
        super().__init__(skin, position)

        self.weapon = weapon
        self.bounds = bounds


    def update(self, keys):
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = "left"
            self.rect.x -= self.speed
            moving = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = "right"
            self.rect.x += self.speed
            moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = "up"
            self.rect.y -= self.speed
            moving = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = "down"
            self.rect.y += self.speed
            moving = True

        self.rect.clamp_ip(self.bounds)

        self.animate(moving)

        self.weapon.update(self.center)


    def draw(self, screen):
        super().draw(screen)

        self.weapon.draw(screen)
