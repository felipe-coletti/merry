import math

import pygame

from entities.enemies.angel.angel_beam import AngelBeam
from entities.enemies.angel.movement import keep_distance
from graphics.spritesheet import Spritesheet
from utils.assets import load_image


class AngelForm2:
    EYE_SCALE = 4

    # Na escala 1 o último quadro da esfera (48px) tem a mesma largura da
    # íris do olho (12px x EYE_SCALE): a esfera cobre a íris e o raio,
    # que é a esfera esticada, sai com a largura dela.
    ORB_SCALE = 1

    # angel_eye.png: grade 5x5 de olhos de 24x24, com passo de 27px.
    # O centro (2, 2) olha para frente; o 3x3 interno é o olhar moderado
    # e o anel externo, o olhar extremo (só nas 8 direções principais).
    EYE_GRID_ORIGIN = 3
    EYE_GRID_STEP = 27
    EYE_SIZE = 24

    # angel_beam.png: 5 quadros de 48x48 de uma esfera crescendo. Os 4
    # primeiros animam a carga; o último vira o raio ao disparar.
    ORB_SIZE = 48
    ORB_FRAMES = 5

    # Alvo mais longe que isso faz o olho girar até o extremo.
    FAR_GAZE_DISTANCE = 200

    # Mantém distância para usar o raio com segurança.
    MOVE_SPEED = 80
    PREFERRED_DISTANCE = 380
    DISTANCE_TOLERANCE = 60

    IDLE_TIME = 1000
    CHARGE_TIME = 1000  # mira travada enquanto carrega
    FIRE_TIME = 1500

    # Durante o disparo o raio persegue o jogador, mas mais devagar do
    # que ele consegue correr de perto: dá para fugir, não é acerto certo.
    BEAM_TURN_SPEED = 25  # graus por segundo

    def __init__(self, angel):
        self.angel = angel

        self.eye_frames, self.iris_offsets = self._load_eye_frames()
        self.orb_frames = self._load_orb_frames()

        self.gaze = (0, 0)

        self.rect = self.image.get_rect(center=self.position)

        self.aim_direction = pygame.Vector2(0, 1)

        self.state = "idle"
        self.state_start = 0

        self.beam = None

    def enter(self):
        self.rect.center = self.position
        self._change_state("idle", pygame.time.get_ticks())

    @property
    def position(self):
        return self.angel.position

    def _load_eye_frames(self):
        sheet = Spritesheet(
            load_image("images", "enemies", "angel", "angel_2", "angel_eye.png")
        )

        frames = {}
        iris_offsets = {}

        for row in range(5):
            for column in range(5):
                gaze = (column - 2, row - 2)

                # O anel externo só tem as 8 direções principais.
                if 2 in map(abs, gaze) and 1 in map(abs, gaze):
                    continue

                frame = sheet.get_image(
                    self.EYE_GRID_ORIGIN + column * self.EYE_GRID_STEP,
                    self.EYE_GRID_ORIGIN + row * self.EYE_GRID_STEP,
                    self.EYE_SIZE,
                    self.EYE_SIZE,
                    self.EYE_SCALE
                )

                frames[gaze] = frame
                iris_offsets[gaze] = self._find_iris_offset(frame)

        return frames, iris_offsets

    @staticmethod
    def _find_iris_offset(frame):
        """Deslocamento do centro da íris em relação ao centro do quadro.

        A íris é a área azul do olho; medir no sprite faz o raio sair do
        lugar certo em cada direção de olhar, mesmo se a arte mudar.
        """
        width, height = frame.get_size()

        xs = []
        ys = []

        for x in range(width):
            for y in range(height):
                red, _, blue, alpha = frame.get_at((x, y))

                if alpha and blue > red + 40:
                    xs.append(x)
                    ys.append(y)

        if not xs:
            return pygame.Vector2()

        return pygame.Vector2(
            (min(xs) + max(xs) + 1) / 2 - width / 2,
            (min(ys) + max(ys) + 1) / 2 - height / 2
        )

    def _load_orb_frames(self):
        sheet = Spritesheet(
            load_image("images", "enemies", "angel", "angel_2", "angel_beam.png")
        )

        return [
            sheet.get_image(
                index * self.ORB_SIZE,
                0,
                self.ORB_SIZE,
                self.ORB_SIZE,
                self.ORB_SCALE
            )
            for index in range(self.ORB_FRAMES)
        ]

    @property
    def image(self):
        return self.eye_frames[self.gaze]

    @property
    def pupil_position(self):
        return self.position + self.iris_offsets[self.gaze]

    def _distance_from_pupil(self, target):
        return self.pupil_position.distance_to(target)

    @property
    def projectile_blockers(self):
        return []

    def take_damage(self, damage):
        # Por enquanto qualquer dano representa um tiro no olho.
        self.angel.next_form()

    def release_objects(self):
        return []

    def attack(self, player, dt):
        if self.beam and self.beam.hits(player.rect):
            player.take_damage_over_time(
                self.beam.DAMAGE_PER_SECOND,
                dt
            )

    def _change_state(self, state, current_time):
        self.state = state
        self.state_start = current_time

    def _update_gaze(self, offset):
        if self.state != "idle":
            # Carregando ou disparando: olha para onde está mirando.
            offset = self.aim_direction
            reach = 2
        else:
            distance = offset.length()

            if distance < self.rect.width / 2:
                self.gaze = (0, 0)
                return

            reach = 2 if distance >= self.FAR_GAZE_DISTANCE else 1

        # Arredonda o ângulo para uma das 8 direções.
        octant = round(math.atan2(offset.y, offset.x) / (math.pi / 4))
        angle = octant * math.pi / 4

        self.gaze = (
            round(math.cos(angle)) * reach,
            round(math.sin(angle)) * reach
        )

    def _turn_aim_towards(self, offset, max_degrees):
        difference = self.aim_direction.angle_to(offset)
        difference = (difference + 180) % 360 - 180

        step = max(-max_degrees, min(difference, max_degrees))

        self.aim_direction = self.aim_direction.rotate(step)

    def update(self, target, dt, level):
        position = keep_distance(
            self.position,
            target,
            self.PREFERRED_DISTANCE,
            self.DISTANCE_TOLERANCE,
            self.MOVE_SPEED,
            dt
        )

        self.angel.move_to(position, level)

        self.rect.center = self.position

        offset = pygame.Vector2(target) - self.position

        # Antes da máquina de estados: o raio nasce na íris do quadro
        # que será desenhado neste frame.
        self._update_gaze(offset)

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.state_start

        if self.state == "idle":
            if offset.length_squared() > 0:
                self.aim_direction = offset.normalize()

            if elapsed >= self.IDLE_TIME:
                # A partir daqui a mira fica travada até disparar.
                self._change_state("charging", current_time)

        elif self.state == "charging":
            if elapsed >= self.CHARGE_TIME:
                self._change_state("firing", current_time)

                self.beam = AngelBeam(
                    self.orb_frames[-1],
                    self.pupil_position,
                    self.aim_direction,
                    self._distance_from_pupil(target)
                )

        elif self.state == "firing":
            if offset.length_squared() > 0:
                self._turn_aim_towards(offset, self.BEAM_TURN_SPEED * dt)

            self.beam.update(
                self.pupil_position,
                self.aim_direction,
                self._distance_from_pupil(target),
                dt
            )

            if elapsed >= self.FIRE_TIME:
                self._change_state("idle", current_time)

                self.beam = None

    def _orb_frame(self):
        # Durante o disparo a esfera já faz parte do raio.
        if self.state == "charging":
            progress = (
                pygame.time.get_ticks() - self.state_start
            ) / self.CHARGE_TIME

            charge_frames = self.ORB_FRAMES - 1
            index = min(int(progress * charge_frames), charge_frames - 1)

            return self.orb_frames[index]

        return None

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

        if self.beam:
            self.beam.draw(screen, camera)

        orb = self._orb_frame()

        if orb:
            orb_rect = orb.get_rect(center=self.pupil_position)

            screen.blit(orb, camera.apply(orb_rect))
