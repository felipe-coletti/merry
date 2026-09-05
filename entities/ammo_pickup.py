import pygame

class AmmoPickup:
    AMMO_AMOUNT = 6

    def __init__(self, image_path, position, scale=0.5):
        image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.scale_by( image, scale )
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)