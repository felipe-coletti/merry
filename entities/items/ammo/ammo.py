import pygame

class Ammo:
    AMMO_AMOUNT = 6

    def __init__(self, image_path, position, scale=1):
        image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.scale_by(image, scale)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen, camera):
        rect = camera.apply(self.rect)

        screen.blit(
            self.image,
            rect
        )