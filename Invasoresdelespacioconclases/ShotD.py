# Shot.py
from EntityD import Entity

class Shot(Entity):
    def __init__(self):
        super().__init__(0, 0)
        self.velocidad_y = 0
        self.is_player_shot = True
        self.rect = None  # Placeholder for the rectangle attribute
    
    def move(self):
        pass
    
    def hit_target(self):
        pass