import pygame


class Ammo:
    AMMO_AMOUNT = 6

    def __init__(self, image, position, scale=1):
        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
