import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße und Titel
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Grundlage")

bg_path = "img/bg.png"
bg = pygame.image.load(bg_path)
pygame.transform.scale(bg, (WIDTH, HEIGHT))

blue_path = "img/sprites/bubble_blue.png"
blue = pygame.image.load(blue_path).convert_alpha()
blue = pygame.transform.scale(blue, (60, 60))

snake_path = "img/sprites/snake.png"
snake = pygame.image.load(snake_path).convert_alpha()
snake = pygame.transform.scale(snake, (100, 200))

# Farben (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Framerate
clock = pygame.time.Clock()
FPS = 60

location = 0

# Haupt-Loop
running = True
while running:
    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                location -= 40
            if event.key == pygame.K_RIGHT:
                location += 40

    # Spiellogik (hier kannst du Logik hinzufügen)


    # Bildschirm aktualisieren
    screen.fill(WHITE)  # Hintergrundfarbe
    screen.blit(bg, (0, 0))
    screen.blit(blue, (100, 50))

    snake_pos = (400 + location, 400)
    screen.blit(snake, snake_pos)
    screen.blit(blue, (snake_pos[0]+20, 540))

    #pygame.display.update()
    pygame.display.flip()

    # Framerate begrenzen
    clock.tick(FPS)

# Pygame beenden
pygame.quit()
sys.exit()
