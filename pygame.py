import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("comicsansms", 24)

# Clock
clock = pygame.time.Clock()
FPS = 15

# Snake and Food
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, DARK_GREEN, [segment[0], segment[1], CELL_SIZE, CELL_SIZE])
        pygame.draw.rect(screen, GREEN, [segment[0]+2, segment[1]+2, CELL_SIZE-4, CELL_SIZE-4])

def draw_food(x, y):
    pygame.draw.rect(screen, RED, [x, y, CELL_SIZE, CELL_SIZE])

def message(text, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def game_loop():
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    food_x = random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE)
    food_y = random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE)

    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press R to Restart or Q to Quit", WHITE, -20)
            message(f"Score: {score}", WHITE, 20)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -CELL_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = CELL_SIZE
                    x_change = 0

        x += x_change
        y += y_change

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        screen.fill(BLACK)
        draw_food(food_x, food_y)

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])
        pygame.display.update()

        # Snake eats food
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE)
            food_y = random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE)
            snake_length += 1
            score += 1

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
