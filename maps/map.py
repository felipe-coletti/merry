from maps.level_01 import Level01

class Map:
    LEVELS = [
        Level01
    ]
        
     
    @classmethod
    def get_level(cls, index):
        return cls.LEVELS[index]()

