import math

import pygame

from entities.enemies.angel.angel_beam import AngelBeam
from graphics.spritesheet import Spritesheet
from utils.assets import load_image


class AngelForm2:
    EYE_SCALE = 4
    ORB_SCALE = 2

    # angel_eye.png: grade 5x5 de olhos de 24x24, com passo de 27px.
    # O centro (2, 2) olha para frente; o 3x3 interno é o olhar moderado
    # e o anel externo, o olhar extremo (só nas 8 direções principais).
    EYE_GRID_ORIGIN = 3
    EYE_GRID_STEP = 27
    EYE_SIZE = 24

    # angel_beam.png: 5 quadros de 48x48 de uma esfera crescendo. Os 4
    # primeiros animam a carga; o último fica na boca do raio ao disparar.
    ORB_SIZE = 48
    ORB_FRAMES = 5

    # Alvo mais longe que isso faz o olho girar até o extremo.
    FAR_GAZE_DISTANCE = 200

    # Distância do centro do olho até onde nasce o raio (a pupila).
    PUPIL_OFFSET = 24

    IDLE_TIME = 1000
    CHARGE_TIME = 1000
    FIRE_TIME = 500

    def __init__(self, angel):
        self.angel = angel

        self.position = pygame.Vector2(angel.position)

        self.eye_frames = self._load_eye_frames()
        self.orb_frames = self._load_orb_frames()

        self.gaze = (0, 0)

        self.rect = self.image.get_rect(center=self.position)

        self.aim_direction = pygame.Vector2(0, 1)

        self.state = "idle"
        self.state_start = pygame.time.get_ticks()

        self.beam = None

    def _load_eye_frames(self):
        sheet = Spritesheet(
            load_image("images", "enemies", "angel", "angel_2", "angel_eye.png")
        )

        frames = {}

        for row in range(5):
            for column in range(5):
                gaze = (column - 2, row - 2)

                # O anel externo só tem as 8 direções principais.
                if 2 in map(abs, gaze) and 1 in map(abs, gaze):
                    continue

                frames[gaze] = sheet.get_image(
                    self.EYE_GRID_ORIGIN + column * self.EYE_GRID_STEP,
                    self.EYE_GRID_ORIGIN + row * self.EYE_GRID_STEP,
                    self.EYE_SIZE,
                    self.EYE_SIZE,
                    self.EYE_SCALE
                )

        return frames

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
        return self.position + self.aim_direction * self.PUPIL_OFFSET

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
        distance = offset.length()

        if distance < self.rect.width / 2:
            self.gaze = (0, 0)
            return

        # Arredonda o ângulo para uma das 8 direções.
        octant = round(math.atan2(offset.y, offset.x) / (math.pi / 4))
        angle = octant * math.pi / 4

        reach = 2 if distance >= self.FAR_GAZE_DISTANCE else 1

        self.gaze = (
            round(math.cos(angle)) * reach,
            round(math.sin(angle)) * reach
        )

    def update(self, target, dt):
        offset = pygame.Vector2(target) - self.position

        self._update_gaze(offset)

        if offset.length_squared() == 0:
            return

        self.aim_direction = offset.normalize()

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.state_start

        if self.state == "idle":
            if elapsed >= self.IDLE_TIME:
                self._change_state("charging", current_time)

        elif self.state == "charging":
            if elapsed >= self.CHARGE_TIME:
                self._change_state("firing", current_time)

                self.beam = AngelBeam(self.pupil_position, self.aim_direction)

        elif self.state == "firing":
            self.beam.update(self.pupil_position, self.aim_direction)

            if elapsed >= self.FIRE_TIME:
                self._change_state("idle", current_time)

                self.beam = None

    def _orb_frame(self):
        if self.state == "firing":
            return self.orb_frames[-1]

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
