import pygame

from entities.characters.character import Character

class Player(Character):
    def __init__(self, skin, position, weapon):
        super().__init__(skin, position)

        self.health = 100
        self.max_health = 100
        self.damage_cooldown = 500
        self.last_damage = 0

        self.adrenaline = 0
        self.max_adrenaline = 100
        self.adrenaline_decay = 1
        self.adrenaline_cooldown = 500
        self.last_adrenaline = 0

        self.adrenaline_speed_bonus = 5

        self.weapon = weapon


    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_damage < self.damage_cooldown:
            return

        self.last_damage = current_time

        if self.health > damage:
            self.health -= damage
        else:
            self.health = 0


    def add_adrenaline(self, amount):
        self.adrenaline = min(
            self.adrenaline + amount,
            self.max_adrenaline
        )


    def update_adrenaline(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_adrenaline < self.adrenaline_cooldown:
            return

        self.last_adrenaline = current_time

        if self.adrenaline > 0:
            self.adrenaline -= self.adrenaline_decay


    def current_speed(self):
        return self.speed + (
            self.adrenaline // (self.max_adrenaline // self.adrenaline_speed_bonus)
        )


    def move(self, dx, dy, map):
        new_rect = self.rect.copy()
        new_rect.x += dx

        if map.can_move(new_rect):
            self.rect.x = new_rect.x

        new_rect = self.rect.copy()
        new_rect.y += dy

        if map.can_move(new_rect):
            self.rect.y = new_rect.y


    def update(self, keys, map, camera):
        dx = 0
        dy = 0

        speed = self.current_speed()

        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = "left"
            dx -= speed
            moving = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = "right"
            dx += speed
            moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = "up"
            dy -= speed
            moving = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = "down"
            dy += speed
            moving = True

        self.move(dx, dy, map)

        self.animate(moving)
        self.weapon.update(self.center, camera.position)


    def draw(self, screen, camera):
        super().draw(screen, camera)

        self.weapon.draw(screen, camera)
