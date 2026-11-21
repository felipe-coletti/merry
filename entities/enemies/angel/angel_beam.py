import math

import pygame


class AngelBeam:
    '''
    Raio feito da esfera de carga esticada até o alcance atual.

    A esfera é cortada ao meio: uma metade fica na origem, a outra na
    ponta, e a coluna central é repetida entre elas. Assim o raio vira
    uma cápsula com a borda da mesma espessura e pixels sem distorção.
    '''

    DAMAGE_PER_SECOND = 25

    # A ponta do raio acompanha a distância do jogador, mas no máximo
    # nesta velocidade: recuar rápido o bastante tira o jogador do alcance.
    EXTEND_SPEED = 150  # pixels por segundo

    # Largura da faixa branca da esfera (sem o brilho amarelo), usada
    # na colisão.
    HIT_WIDTH = 42

    def __init__(self, image, position, direction, length):
        """
        image: último quadro da esfera de carga (largura = altura).
        length: começa na distância do jogador no momento do disparo.
        """
        width, height = image.get_size()
        half = width // 2

        self.left_cap = image.subsurface((0, 0, half, height))
        self.right_cap = image.subsurface((half, 0, width - half, height))
        self.middle = image.subsurface((half, 0, 1, height))

        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()
        self.length = length

    def update(self, position, direction, target_length, dt):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()

        max_step = self.EXTEND_SPEED * dt
        difference = target_length - self.length

        self.length = max(
            0,
            self.length + max(-max_step, min(difference, max_step))
        )

    def get_end_position(self):
        return self.position + self.direction * self.length

    def hits(self, rect):
        # Aumenta o alvo em vez de engrossar a linha: equivale a testar
        # a faixa branca inteira do raio, não só o seu eixo. Inclui as
        # pontas arredondadas de forma aproximada.
        target = rect.inflate(self.HIT_WIDTH, self.HIT_WIDTH)

        return bool(
            target.clipline(
                tuple(self.position),
                tuple(self.get_end_position())
            )
        )

    def _build_image(self):
        length = round(self.length)
        cap_width = self.left_cap.get_width()
        height = self.left_cap.get_height()

        image = pygame.Surface(
            (cap_width * 2 + length, height),
            pygame.SRCALPHA
        )

        image.blit(self.left_cap, (0, 0))

        if length > 0:
            image.blit(
                pygame.transform.scale(self.middle, (length, height)),
                (cap_width, 0)
            )

        image.blit(self.right_cap, (cap_width + length, 0))

        angle = -math.degrees(math.atan2(self.direction.y, self.direction.x))

        return pygame.transform.rotate(image, angle)

    def draw(self, screen, camera):
        image = self._build_image()

        center = (self.position + self.get_end_position()) / 2

        rect = image.get_rect(center=center)

        screen.blit(image, camera.apply(rect))
