import pygame
import random
from GraphicsD import *
from PlayerD import Player
from OpponentD import Opponent
from BossD import Boss
from ShotD import Shot

class Game:
    def __init__(self, score=0, player=None, opponent=None, is_running=True):
        self.score = score
        self.player = player if player else Player()
        self.opponents = []
        self.boss = None
        self.is_running = is_running
        self.shots = []
        self.enemy_shots = []
        self.explosions = []
        self.game_over = False
        self.victory = False
        
        # Inicializar rectángulo del jugador
        self.player.rect = pygame.Rect(0, 0, 50, 50)
        self.player.rect.centerx = 400
        self.player.rect.centery = 550
        
        # Crear oponentes iniciales
        for _ in range(10):
            opp = Opponent()
            opp.rect = pygame.Rect(0, 0, 50, 50)
            opp.rect.x = random.randrange(1, 750)
            opp.rect.y = 10
            opp.velocidad_y = random.randrange(1, 3)
            self.opponents.append(opp)
    
    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Juego Space Invaders')
        clock = pygame.time.Clock()
        
        while self.is_running:
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shot = Shot()
                        shot.x = self.player.rect.centerx
                        shot.y = self.player.rect.top
                        shot.velocidad_y = -18
                        shot.is_player_shot = True
                        self.shots.append(shot)
                        laser_sonido.play()
                    elif event.key == pygame.K_ESCAPE:
                        self.is_running = False
            
            # Actualización del juego
            self.update()
            
            # Dibujado
            screen.blit(fondo, (0, 0))
            
            # Dibujar elementos del juego
            pygame.draw.rect(screen, (255, 255, 255), self.player.rect)
            
            for opp in self.opponents:
                pygame.draw.rect(screen, (255, 0, 0), opp.rect)
            
            if self.boss:
                pygame.draw.rect(screen, (255, 0, 255), self.boss.rect)
            
            for shot in self.shots:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(shot.x, shot.y, 10, 20))
            
            for shot in self.enemy_shots:
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(shot.x, shot.y, 10, 20))
            
            # Dibujar UI
            self.UI(screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        # Mostrar mensaje final
        if self.game_over:
            screen.blit(game_over_image, game_over_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
        
        pygame.quit()
    
    def update(self):
        if self.game_over:
            self.end_game()
            return
            
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        self.player.velocidad_x = 0
        if keys[pygame.K_LEFT]:
            self.player.velocidad_x = -5
        elif keys[pygame.K_RIGHT]:
            self.player.velocidad_x = 5
        
        self.player.rect.x += self.player.velocidad_x
        if self.player.rect.right > 800:
            self.player.rect.right = 800
        elif self.player.rect.left < 0:
            self.player.rect.left = 0
        
        # Movimiento de oponentes
        for opp in self.opponents:
            opp.rect.x += random.randint(-1, 1)
            opp.rect.y += opp.velocidad_y
            
            if opp.rect.x >= 800:
                opp.rect.x = 0
                opp.rect.y += 50
            
            # Disparo de oponentes
            if random.random() < 0.01:
                shot = Shot()
                shot.x = opp.rect.centerx
                shot.y = opp.rect.bottom
                shot.velocidad_y = 4
                shot.is_player_shot = False
                self.enemy_shots.append(shot)
                laser_sonido.play()
        
        # Movimiento del jefe
        if self.boss:
            self.boss.rect.x += self.boss.velocidad_x
            self.boss.rect.y += self.boss.velocidad_y
            
            if self.boss.rect.x <= 0 or self.boss.rect.x >= 800 - self.boss.rect.width:
                self.boss.velocidad_x *= -1
            if self.boss.rect.y <= 0 or self.boss.rect.y >= 300:
                self.boss.velocidad_y *= -1
            
            # Disparo del jefe
            if random.random() < 0.05:
                shot = Shot()
                shot.x = self.boss.rect.centerx
                shot.y = self.boss.rect.bottom
                shot.velocidad_y = 6
                shot.is_player_shot = False
                self.enemy_shots.append(shot)
                laser_sonido.play()
        
        # Movimiento de disparos
        for shot in self.shots[:]:
            shot.y += shot.velocidad_y
            if shot.y < 0:
                self.shots.remove(shot)
        
        for shot in self.enemy_shots[:]:
            shot.y += shot.velocidad_y
            if shot.y > 600:
                self.enemy_shots.remove(shot)
        
        # Colisiones
        self.check_collisions()
        
        # Verificar fin del juego
        if self.player.vida <= 0:
            self.game_over = True
        
        # Aparecer jefe si no hay oponentes
        if not self.opponents and not self.boss:
            self.boss = Boss()
            self.boss.rect = pygame.Rect(0, 0, 300, 300)
            self.boss.rect.centerx = 50
            self.boss.rect.centery = 200
            self.boss.velocidad_x = 2
            self.boss.velocidad_y = 1
    
    def check_collisions(self):
        # Disparos del jugador con oponentes
        for shot in self.shots[:]:
            shot_rect = pygame.Rect(shot.x, shot.y, 10, 20)
            for opp in self.opponents[:]:
                if shot_rect.colliderect(opp.rect):
                    self.score += 10
                    self.shots.remove(shot)
                    self.opponents.remove(opp)
                    explosion_sonido.play()
                    
                    if len(self.opponents) < 10 and not self.boss:
                        new_opp = Opponent()
                        new_opp.rect = pygame.Rect(0, 0, 50, 50)
                        new_opp.rect.x = random.randrange(1, 750)
                        new_opp.rect.y = 10
                        new_opp.velocidad_y = random.randrange(1, 3)
                        self.opponents.append(new_opp)
                    break
        
        # Disparos del jugador con jefe
        if self.boss:
            for shot in self.shots[:]:
                shot_rect = pygame.Rect(shot.x, shot.y, 10, 20)
                if shot_rect.colliderect(self.boss.rect):
                    self.boss.vida -= 10
                    self.shots.remove(shot)
                    explosion_sonido.play()
                    
                    if self.boss.vida <= 0:
                        self.score += 100
                        self.boss = None
                        self.victory = True
                        self.game_over = True
                    break
        
        # Disparos enemigos con jugador
        for shot in self.enemy_shots[:]:
            shot_rect = pygame.Rect(shot.x, shot.y, 10, 20)
            if shot_rect.colliderect(self.player.rect):
                self.player.vida -= 33
                self.enemy_shots.remove(shot)
                golpe_sonido.play()
                
                if self.player.vida <= 0:
                    self.game_over = True
        
        # Oponentes con jugador
        for opp in self.opponents:
            if opp.rect.colliderect(self.player.rect):
                self.player.vida = 0
                self.game_over = True
    
    def end_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
    
    def UI(self, screen):
        # Dibujar puntuación
        font = pygame.font.SysFont('Small Fonts', 30, bold=True)
        text = font.render(f'SCORE: {self.score}', True, blanco, negro)
        screen.blit(text, (800 - 150, 2))
        
        # Dibujar barra de vida
        longitud = 100
        alto = 20
        fill = int((self.player.vida / 100) * longitud)
        border = pygame.Rect(800 - 285, 0, longitud, alto)
        fill_rect = pygame.Rect(800 - 285, 0, fill, alto)
        pygame.draw.rect(screen, (255, 0, 55), fill_rect)
        pygame.draw.rect(screen, blanco, border, 4)
    
    def remove_oponent(self):
        pass