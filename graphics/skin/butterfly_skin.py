from graphics.spritesheet import Spritesheet


class ButterflySkin:
    FRAME_WIDTH = 42
    FRAME_HEIGHT = 34

    FRAME_POSITIONS = ((3, 6), (51, 6))

    def __init__(self, image, scale=2):
        self.scale = scale

        sheet = Spritesheet(image)

        self.frames = [
            sheet.get_image(
                x,
                y,
                self.FRAME_WIDTH,
                self.FRAME_HEIGHT,
                self.scale
            )
            for x, y in self.FRAME_POSITIONS
        ]
