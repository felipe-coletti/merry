import pygame


class AngelBeam:
    DAMAGE_PER_SECOND = 25

    # A ponta do raio acompanha a distância do jogador, mas no máximo
    # nesta velocidade: recuar rápido o bastante tira o jogador do alcance.
    EXTEND_SPEED = 150  # pixels por segundo

    # Mesmas cores do sprite angel_beam.png: núcleo branco e brilho amarelo.
    CORE_COLOR = (255, 255, 255)
    GLOW_COLOR = (253, 255, 105)

    CORE_WIDTH = 24
    GLOW_WIDTH = 36

    def __init__(self, position, direction, length):
        """length: começa na distância do jogador no momento do disparo."""
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()
        self.length = length

    def update(self, position, direction, target_length, dt):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()

        max_step = self.EXTEND_SPEED * dt
        difference = target_length - self.length

        self.length += max(-max_step, min(difference, max_step))

    def get_end_position(self):
        return self.position + self.direction * self.length

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
        pygame.draw.circle(screen, self.GLOW_COLOR, end, self.GLOW_WIDTH / 2)

        pygame.draw.line(screen, self.CORE_COLOR, start, end, self.CORE_WIDTH)
        pygame.draw.circle(screen, self.CORE_COLOR, end, self.CORE_WIDTH / 2)
