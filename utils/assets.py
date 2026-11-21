from functools import lru_cache
from pathlib import Path

import pygame


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def asset_path(*parts):
    return ASSETS_DIR.joinpath(*parts)


@lru_cache(maxsize=None)
def load_image(*parts):
    '''
    Carrega uma imagem de assets/ uma única vez.

    A superfície retornada é compartilhada: não a modifique no lugar,
    use pygame.transform (que devolve uma cópia).
    '''
    return pygame.image.load(asset_path(*parts)).convert_alpha()
