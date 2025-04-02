
import pygame

# Inicializar pygame y el mixer
pygame.init()
pygame.mixer.init()  # <--- Añade esto aquí

# Cargar imagenes y sonidos
fondo = pygame.image.load('imagenes/fondo.png')
fondo = pygame.transform.scale(fondo, (800, 600))
pygame.display.set_icon(fondo)

# Cargar la imagen de "Game Over"
game_over_image = pygame.image.load('imagenes/game_over.png')
game_over_rect = game_over_image.get_rect()
game_over_rect.center = (400, 300)

laser_sonido = pygame.mixer.Sound('sonidos/laser.wav')
explosion_sonido = pygame.mixer.Sound('sonidos/explosion.wav')
golpe_sonido = pygame.mixer.Sound('sonidos/golpe.wav')

# Cargar imagenes de naves y explosiones
explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(f'imagenes/explosion/{i}.png')
    explosion_list.append(explosion)

# Configuración de colores
blanco = (255, 255, 255)
negro = (0, 0, 0)