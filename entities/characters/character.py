import pygame


class Character:
    def __init__(self, skin, position, speed=300, animation_fps=6):
        '''
        speed: pixels por segundo.
        animation_fps: quadros de animação por segundo ao caminhar.
        '''
        self.skin = skin
        self.direction = "down"
        self.frame_index = 0

        self.rect = self.image.get_rect(topleft=position)

        # Posição em ponto flutuante: o Rect só guarda inteiros, e
        # movimentos pequenos por frame se perderiam no arredondamento.
        self.float_position = pygame.Vector2(self.rect.topleft)

        self.animation_fps = animation_fps

        self.speed = speed

    def animate(self, moving, dt):
        if not moving:
            self.frame_index = 0
            return

        frame_count = len(self.skin.frames[self.direction])

        self.frame_index = (
            self.frame_index + self.animation_fps * dt
        ) % frame_count

    @property
    def image(self):
        return self.skin.frames[self.direction][int(self.frame_index)]

    @property
    def mask(self):
        return self.skin.masks[self.direction][int(self.frame_index)]

    @property
    def position(self):
        return self.rect.topleft

    @property
    def center(self):
        return self.rect.center

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
