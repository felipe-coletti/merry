import pygame


def keep_distance(position, target, distance, tolerance, speed, dt):
    '''
    Nova posição que aproxima ou afasta `position` de `target`.

    Fica parado enquanto a distância estiver dentro de
    `distance ± tolerance`; fora disso, anda até `speed` pixels por
    segundo, sem passar da distância desejada.
    '''
    position = pygame.Vector2(position)
    offset = pygame.Vector2(target) - position

    current = offset.length()

    if current == 0:
        return position

    if current > distance + tolerance:
        step = min(speed * dt, current - distance)
    elif current < distance - tolerance:
        step = -min(speed * dt, distance - current)
    else:
        return position

    return position + offset.normalize() * step
