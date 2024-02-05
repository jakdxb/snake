import pygame
import sys
import random

pygame.init()

cell_size = 20
grid_width = 800 // cell_size
grid_height = 600 // cell_size

screen_width = grid_width * cell_size
screen_height = grid_height * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
brown = (150, 75, 0)
red = (255, 0, 0)
green = (162, 196, 145)
gray = (169, 169, 169)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

difficulty = None
easy = {'obstacle_count': 5, 'snake_speed': 10}
normal = {'obstacle_count': 10, 'snake_speed': 15}
hard = {'obstacle_count': 15, 'snake_speed': 20}

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, green, segment)
        pygame.draw.rect(screen, gray, segment, 1)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, brown, obstacle)

def draw_apple(apple):
    pygame.draw.ellipse(screen, red, apple)

def draw_menu():
    screen.fill(green)
    # Napis "SNAKE GAME"
    snake_game_text = big_font.render("SNAKE GAME", True, black)
    snake_game_rect = snake_game_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(snake_game_text, snake_game_rect)

    text = font.render("Press X for Easy, E for Normal, H for Hard", True, black)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    press_p_text = font.render("Press P to pause during the game", True, black)
    press_p_rect = press_p_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
    screen.blit(press_p_text, press_p_rect)

    pygame.display.flip()

def draw_game_over(score):
    screen.fill(white)
    game_over_text = font.render("GAME OVER", True, black)
    score_text = font.render(f"SCORE: {score}", True, black)

    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.delay(3000)
    draw_menu()

def game_loop():
    global difficulty
    snake = [pygame.Rect(2 * cell_size, 2 * cell_size, cell_size, cell_size)]
    direction = "RIGHT"
    change_to = direction
    game_over = False
    paused = False
    score = 0

    obstacles = [pygame.Rect(random.randint(0, grid_width - 1) * cell_size,
                             random.randint(0, grid_height - 1) * cell_size, cell_size, cell_size) for _ in range(difficulty['obstacle_count'])]

    apple = pygame.Rect(random.randint(0, grid_width - 1) * cell_size,
                        random.randint(0, grid_height - 1) * cell_size, cell_size, cell_size)

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            pygame.time.delay(100)
            screen.fill(black)
            pause_text = big_font.render("PAUSED", True, white)
            press_p_text = font.render("Press P to continue", True, white)
            pause_rect = pause_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
            press_p_rect = press_p_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
            screen.blit(pause_text, pause_rect)
            screen.blit(press_p_text, press_p_rect)
            pygame.display.flip()
            continue

        direction = change_to

        if direction == "UP":
            new_head = pygame.Rect(snake[0].x, snake[0].y - cell_size, cell_size, cell_size)
        elif direction == "DOWN":
            new_head = pygame.Rect(snake[0].x, snake[0].y + cell_size, cell_size, cell_size)
        elif direction == "LEFT":
            new_head = pygame.Rect(snake[0].x - cell_size, snake[0].y, cell_size, cell_size)
        elif direction == "RIGHT":
            new_head = pygame.Rect(snake[0].x + cell_size, snake[0].y, cell_size, cell_size)

        if new_head.collidelist(obstacles) != -1 or new_head.collidelist(snake[1:]) != -1:
            game_over = True

        new_head.x = (new_head.x + screen_width) % screen_width
        new_head.y = (new_head.y + screen_height) % screen_height

        if new_head.colliderect(apple):
            apple = pygame.Rect(random.randint(0, grid_width - 1) * cell_size,
                                random.randint(0, grid_height - 1) * cell_size, cell_size, cell_size)
            snake.append(pygame.Rect(-cell_size, -cell_size, cell_size, cell_size))
            score += 1


        snake.insert(0, new_head)
        if len(snake) > score + 1:
            snake.pop()

        screen.fill(black)
        draw_snake(snake)
        draw_obstacles(obstacles)
        draw_apple(apple)
        score_text = font.render(f"SCORE: {score}", True, white)
        screen.blit(score_text, (screen_width - 150, 10))
        pygame.display.flip()

        clock.tick(difficulty['snake_speed'])

    draw_game_over(score)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                difficulty = easy
                game_loop()

            elif event.key == pygame.K_e:
                difficulty = normal
                game_loop()

            elif event.key == pygame.K_h:
                difficulty = hard
                game_loop()

    draw_menu()
    pygame.display.update()
