# Player.py
from CharacterD import Character

class Player(Character):
    def __init__(self, lives=3):
        super().__init__(lives, True)
        self.score = 0
        self.vida = 100
        self.velocidad_x = 0
        self.rect = None  # Se inicializará en Game
    
    def move(self):
        pass
    
    def shoot(self):
        pass