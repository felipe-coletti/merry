import pygame


class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, x, y, width, height, scale=1):
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        image.blit(self.sheet, (0, 0), (x, y, width, height))

        return pygame.transform.scale(
            image,
            (width * scale, height * scale)
        )
