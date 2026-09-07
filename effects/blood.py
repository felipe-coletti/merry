import pygame

class Blood:
    def __init__(self, skin, position, animation_speed=0.15):
        self.skin = skin
        self.position = pygame.Vector2(position)

        self.frame_index = 0
        self.animation_speed = animation_speed
        self.finished = False

        self.rect = self.skin.frames[0].get_rect(
            center=self.position
        )

    def update(self):
        if self.finished:
            return

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.skin.frames):
            self.frame_index = len(self.skin.frames) - 1
            self.finished = True

    def draw(self, screen, camera):
        frame = self.skin.frames[int(self.frame_index)]

        rect = frame.get_rect(
            center=self.position
        )

        rect = camera.apply(rect)

        screen.blit(frame, rect)