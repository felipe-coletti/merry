import pygame


class AngelBeam:
    DAMAGE_PER_SECOND = 25

    LENGTH = 2000

    # Mesmas cores do sprite angel_beam.png: núcleo branco e brilho amarelo.
    CORE_COLOR = (255, 255, 255)
    GLOW_COLOR = (253, 255, 105)

    CORE_WIDTH = 24
    GLOW_WIDTH = 36

    def __init__(self, position, direction):
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

    def update(self, position, direction):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()

    def get_end_position(self):
        return self.position + self.direction * self.LENGTH

    def hits(self, rect):
        # Aumenta o alvo em vez de engrossar a linha: equivale a testar
        # a faixa branca inteira do raio, não só o seu eixo.
        target = rect.inflate(self.CORE_WIDTH, self.CORE_WIDTH)

        return bool(
            target.clipline(
                tuple(self.position),
                tuple(self.get_end_position())
            )
        )

    def draw(self, screen, camera):
        offset = -camera.position

        start = self.position + offset
        end = self.get_end_position() + offset

        pygame.draw.line(screen, self.GLOW_COLOR, start, end, self.GLOW_WIDTH)
        pygame.draw.line(screen, self.CORE_COLOR, start, end, self.CORE_WIDTH)
