import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 600, 400
FPS = 10

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Inicjalizacja ekranu gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Funkcja rysująca węża na ekranie
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, WHITE, segment)

# Funkcja rysująca przeszkody na ekranie
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

# Funkcja rysująca jedzenie na ekranie
def draw_food(food):
    pygame.draw.rect(screen, WHITE, food)

# Funkcja sprawdzająca kolizję z przeszkodami
def check_obstacle_collision(snake, obstacles):
    for obstacle in obstacles:
        if snake[0].colliderect(obstacle):
            return True
    return False

# Funkcja sprawdzająca kolizję z samym sobą
def check_self_collision(snake):
    for i in range(1, len(snake)):
        if snake[0].colliderect(snake[i]):
            return True
    return False

# Funkcja generująca nowe położenie dla jedzenia
def generate_food_position(snake, obstacles):
    while True:
        food_position = (
            random.randrange(0, WIDTH, 20),
            random.randrange(0, HEIGHT, 20)
        )
        # Sprawdź, czy jedzenie nie koliduje z wężem, przeszkodami lub samym sobą
        if food_position not in [segment.topleft for segment in snake] and \
                food_position not in [obstacle.topleft for obstacle in obstacles]:
            return food_position

# Funkcja generująca przeszkody
def generate_obstacles(snake, food):
    obstacles = []
    for _ in range(3):
        obstacle_position = (
            random.randrange(0, WIDTH, 20),
            random.randrange(0, HEIGHT, 20)
        )
        # Sprawdź, czy przeszkoda nie koliduje z wężem, jedzeniem lub innymi przeszkodami
        if obstacle_position not in [segment.topleft for segment in snake] and \
                obstacle_position != food.topleft and \
                obstacle_position not in [obs.topleft for obs in obstacles]:
            obstacles.append(pygame.Rect(obstacle_position, (20, 20)))
    return obstacles

# Początkowe położenie węża
initial_length = 1
snake = [pygame.Rect(100 - i * 20, 100, 20, 20) for i in range(initial_length)]

# Początkowe położenie jedzenia
food = pygame.Rect(200, 200, 20, 20)

# Początkowe położenie przeszkód
obstacles = generate_obstacles(snake, food)

# Kierunek ruchu węża (początkowo w prawo)
direction = "RIGHT"

# Wynik gry
score = 0

# Czcionka do wyświetlania wyniku
font = pygame.font.Font(None, 36)

# Pętla gry
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Kontrola ruchu węża
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        elif keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        elif keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        elif keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

    # Przesunięcie głowy węża zgodnie z kierunkiem
    if direction == "UP":
        snake[0].y = (snake[0].y - 20) % HEIGHT
    elif direction == "DOWN":
        snake[0].y = (snake[0].y + 20) % HEIGHT
    elif direction == "LEFT":
        snake[0].x = (snake[0].x - 20) % WIDTH
    elif direction == "RIGHT":
        snake[0].x = (snake[0].x + 20) % WIDTH

    # Sprawdzenie kolizji z przeszkodami
    if check_obstacle_collision(snake, obstacles) or check_self_collision(snake):
        # Ekran "Game Over"
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 18))
        pygame.display.flip()
        pygame.time.wait(2000)  # Poczekaj 2 sekundy
        # Zresetuj grę
        snake = [pygame.Rect(100 - i * 20, 100, 20, 20) for i in range(initial_length)]
        food.topleft = generate_food_position(snake, obstacles)
        obstacles = generate_obstacles(snake, food)
        direction = "RIGHT"
        score = 0

    # Sprawdzenie kolizji z jedzeniem
    if snake[0].colliderect(food):
        # Dodanie nowego segmentu węża
        snake.append(pygame.Rect(0, 0, 20, 20))
        # Wygenerowanie nowego położenia dla jedzenia
        food.topleft = generate_food_position(snake, obstacles)
        # Zwiększenie wyniku
        score += 1

    # Przesunięcie reszty ciała węża
    for i in range(len(snake) - 1, 0, -1):
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y

    # Rysowanie na ekranie
    screen.fill(BLACK)
    draw_snake(snake)
    draw_obstacles(obstacles)
    draw_food(food)

    # Wyświetlenie wyniku
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

    # Ustawienie liczby klatek na sekundę
    clock.tick(FPS)
