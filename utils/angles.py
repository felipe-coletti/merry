def angle_difference(current, target):
    """Menor diferença (em graus, de -180 a 180) de `current` até `target`."""
    return (target - current + 180) % 360 - 180


def approach_angle(current, target, max_step):
    """Gira `current` em direção a `target` no máximo `max_step` graus.

    Retorna (novo_ângulo, chegou).
    """
    difference = angle_difference(current, target)

    if abs(difference) <= max_step:
        return target, True

    return current + max_step * (1 if difference > 0 else -1), False
