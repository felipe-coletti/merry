import pygame

class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(
            self,
            frame,
            x,
            y,
            width,
            height,
            scale,
            color
    ):
        image = pygame.Surface((width, height)).convert_alpha()

        image.blit(self.sheet, (0, 0), (x, y, width + 3, height + 3))

        image = pygame.transform.scale(image, (width * scale, height * scale))

        image.set_colorkey(color)

        return image