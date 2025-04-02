# Character.py
from EntityD import Entity

class Character(Entity):
    def __init__(self, lives, is_alive):
        super().__init__(0, 0)  # x, y se inicializarán en las clases hijas
        self.lives = lives
        self.is_alive = is_alive
    
    def move(self):
        pass
    
    def shoot(self):
        pass
    
    def collide(self):
        pass