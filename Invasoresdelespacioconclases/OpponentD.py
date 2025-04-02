# Opponent.py
from CharacterD import Character

class Opponent(Character):
    def __init__(self, is_star=False):
        super().__init__(1, True)  # lives=1, is_alive=True
        self.is_star = is_star
        self.velocidad_y = 0
        self.rect = None  # Se inicializará en Game
    
    def move(self):
        pass
    
    def shoot(self):
        pass