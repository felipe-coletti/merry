import pygame


class Butterfly:
    ADRENALINE_REWARD = 10
    
    def __init__(self, image_path, position, scale=0.5, speed=1, health=1):
        image = pygame.image.load(image_path).convert_alpha()
        
        self.image = pygame.transform.scale_by(image, scale)

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


    def draw(self, screen):
        screen.blit(self.image, self.rect)