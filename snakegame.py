import pygame
import sys
import random

#initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Other constants
max_cells = (WIDTH // CELL_SIZE) * (HEIGHT // CELL_SIZE)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Snake
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (CELL_SIZE, 0)
next_dir = snake_dir

# Food
def generateFood():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = generateFood()

# Draw objects
def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

# Snake functions
def move_snake():
    global food
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake.insert(0, head)

    if head == food:
        food = generateFood()
    else:
        snake.pop()

def check_collision():
    head = snake[0]
    if head in snake[1:] or head[0] < 0 or head[0] >= WIDTH or head [1] < 0 or head [1] >= HEIGHT:
        return True
    return False

# Game states
game_state = 'running'

font = pygame.font.SysFont(None, 48)

def show_message(text_lines, color=(255, 255, 255)):
    total_height = len(text_lines) * 40  # 40 is line spacing
    start_y = HEIGHT // 2 - total_height // 2

    for i, line in enumerate(text_lines):
        msg = font.render(line, True, color)
        rect = msg.get_rect(center=(WIDTH // 2, start_y + i * 40))
        screen.blit(msg, rect)

def reset_game():
    global snake, snake_dir, next_dir, food, game_state
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_dir = (CELL_SIZE, 0)
    next_dir = snake_dir
    food = generateFood()
    game_state = 'running'

# Game loop
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and game_state in 'running':
            if event.key in (pygame.K_UP, pygame.K_w) and snake_dir != (0, CELL_SIZE):
                next_dir = (0, -CELL_SIZE)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and snake_dir != (0, -CELL_SIZE):
                next_dir = (0, CELL_SIZE)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and snake_dir != (CELL_SIZE, 0):
                next_dir = (-CELL_SIZE, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake_dir != (-CELL_SIZE, 0):
                next_dir = (CELL_SIZE, 0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            ai_mode = not ai_mode
        elif event.type == pygame.KEYDOWN and game_state in ('game_over', 'win'):
            if event.key == pygame.K_r:
                reset_game()
    
    if game_state == 'running':
        snake_dir = next_dir
        move_snake()
        if check_collision():
            game_state = 'game_over'
        if len(snake) == max_cells:
            game_state = 'win'
        draw_snake()
        draw_food()
    elif game_state == 'game_over':
        show_message(["Game Over, loser!", "Press R to restart"], RED)
    elif game_state == 'win':
        show_message(["Wow, you managed to fill the screen!", "GG.", "Press R to restart",], GREEN)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()