import pygame


class Blood:
    def __init__(self, skin, position, animation_fps=9):
        self.skin = skin
        self.position = pygame.Vector2(position)

        self.frame_index = 0
        self.animation_fps = animation_fps
        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        self.frame_index += self.animation_fps * dt

        if self.frame_index >= len(self.skin.frames):
            self.frame_index = len(self.skin.frames) - 1
            self.finished = True

    def draw(self, screen, camera):
        frame = self.skin.frames[int(self.frame_index)]

        rect = frame.get_rect(center=self.position)

        screen.blit(frame, camera.apply(rect))
