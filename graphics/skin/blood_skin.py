from graphics.spritesheet import Spritesheet


class BloodSkin:
    FRAME_WIDTH = 32
    FRAME_HEIGHT = 32
    FRAME_COUNT = 8

    def __init__(self, image, scale=2):
        self.scale = scale

        sheet = Spritesheet(image)

        self.frames = [
            sheet.get_image(
                index * self.FRAME_WIDTH,
                0,
                self.FRAME_WIDTH,
                self.FRAME_HEIGHT,
                self.scale
            )
            for index in range(self.FRAME_COUNT)
        ]
