# Simple flugzeugspiel mit Hindernissen und Schießen
# Importiere die benötigten Module:  pip install pygame
# Steuerung: Pfeiltasten für Bewegung, <--  -->  [Leertaste]  zum Schießen

import pygame
import random

# Initialisierung von pygame
pygame.init()

# Bildschirmgröße und Spielfeldparameter
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PLANE_WIDTH = 50
PLANE_HEIGHT = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
BULLET_WIDTH = 5
BULLET_HEIGHT = 10

# Farben
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Flugzeug-Klasse
class Plane:
    def __init__(self):
        self.image = pygame.Surface((PLANE_WIDTH, PLANE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PLANE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLANE_WIDTH

# Hindernis-Klasse
class Obstacle:
    def __init__(self, x):
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, 0))

    def move(self):
        self.rect.y += 5

# Kugel-Klasse
class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y -= 10

# Hauptspiel-Schleife
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flugzeugspiel mit Schießen")
clock = pygame.time.Clock()
plane = Plane()
obstacles = []
bullets = []
score = 0

# Hindernisse generieren
def create_obstacle():
    x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
    obstacles.append(Obstacle(x))

# Spiel-Loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(plane.image, plane.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Steuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        plane.move(-5)
    if keys[pygame.K_RIGHT]:
        plane.move(5)
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Begrenzung auf max. 5 Kugeln gleichzeitig
            bullet_x = plane.rect.centerx
            bullet_y = plane.rect.top
            bullets.append(Bullet(bullet_x, bullet_y))

    # Kugeln bewegen und anzeigen
    for bullet in bullets[:]:
        bullet.move()
        screen.blit(bullet.image, bullet.rect)

        # Entferne Kugeln außerhalb des Bildschirms
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    # Hindernisse bewegen, anzeigen und prüfen
    for obstacle in obstacles[:]:
        obstacle.move()
        screen.blit(obstacle.image, obstacle.rect)

        # Kollision mit Flugzeug
        if obstacle.rect.colliderect(plane.rect):
            print(f"Spiel beendet! Dein Score: {score}")
            running = False

        # Kollision mit Kugel
        for bullet in bullets[:]:
            if obstacle.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                obstacles.remove(obstacle)
                score += 1
                break  # Nur ein Treffer pro Hindernis

        if obstacle.rect.y > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            score += 1

    # Zufällig Hindernisse generieren
    if random.randint(1, 20) == 1:
        create_obstacle()

    # Score anzeigen
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
 