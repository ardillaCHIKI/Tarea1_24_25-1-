# Boss.py
from OpponentD import Opponent

class Boss(Opponent):
    def __init__(self):
        super().__init__()
        self.vida = 100
        self.velocidad_x = 0
    
    def move(self):
        pass
    
    def shoot(self):
        pass
    
    def special_attack(self):
        pass