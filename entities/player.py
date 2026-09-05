import pygame

from entities.character import Character

class Player(Character):
    def __init__(self, skin, position, weapon, bounds):
        super().__init__(skin, position)

        self.health = 100
        self.damage_cooldown = 500
        self.last_damage = 0

        self.weapon = weapon
        self.bounds = bounds


    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_damage < self.damage_cooldown:
            return

        self.last_damage = current_time
        self.health -= damage


    def move(self, dx, dy, obstacles):
        self.rect.x += dx

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if dx > 0:
                    self.rect.right = obstacle.left
                elif dx < 0:
                    self.rect.left = obstacle.right

        self.rect.y += dy

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if dy > 0:
                    self.rect.bottom = obstacle.top
                elif dy < 0:
                    self.rect.top = obstacle.bottom


    def update(self, keys, obstacles):
        dx = 0
        dy = 0

        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = "left"
            dx -= self.speed
            moving = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = "right"
            dx += self.speed
            moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = "up"
            dy -= self.speed
            moving = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = "down"
            dy += self.speed
            moving = True

        self.move(dx, dy, obstacles)

        self.animate(moving)
        self.weapon.update(self.center)


    def draw(self, screen):
        super().draw(screen)

        self.weapon.draw(screen)
