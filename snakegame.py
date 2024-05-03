import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Constants
BLOCK_SIZE = 20
FPS = 60  # Increase FPS for smoother movement
MOVE_SPEED = 4  # Increase the speed of movement for smoother motion

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = (0, -1)
        self.color = GREEN
        self.move_counter = 0  # Counter to control snake movement speed

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        self.move_counter += 1
        if self.move_counter >= MOVE_SPEED:
            self.move_counter = 0
        else:
            return True  # Return True to maintain current direction
        
        cur = self.get_head_position()
        x, y = self.direction
        new_x = cur[0] + (x * (BLOCK_SIZE / 2))  # Move by 0.5 tiles horizontally
        new_y = cur[1] + (y * (BLOCK_SIZE / 2))  # Move by 0.5 tiles vertically
        new = (new_x % WIDTH, new_y % HEIGHT)
        
        # Check if the new position collides with the walls
        if new[0] < 0 or new[0] >= WIDTH or new[1] < 0 or new[1] >= HEIGHT:
            return False  # Collision with wall, game over
        elif len(self.positions) > 2 and new in self.positions[2:]:
            return False  # Collision with itself, game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = (0, -1)

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    pygame.quit()
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))
                elif event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.size = BLOCK_SIZE  # Size of the food
        self.hitbox_size = BLOCK_SIZE * 2  # Increase the hitbox size
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
                         random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE)

    def draw(self, surface):
        x, y = self.position
        center = (x + self.size // 2, y + self.size // 2)
        pygame.draw.circle(surface, self.color, center, self.size // 2)
        pygame.draw.circle(surface, WHITE, center, self.size // 2, 1)

    def is_eaten(self, snake_head):
        # Check if the snake's head is within the hitbox of the food
        return math.sqrt((self.position[0] - snake_head[0]) ** 2 + (self.position[1] - snake_head[1]) ** 2) <= self.hitbox_size / 2

def draw_game_over_screen():
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over", True, WHITE)
    exit_text = font.render("Press 'Q' to exit", True, WHITE)
    restart_text = font.render("Press 'R' to restart", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
    WIN.blit(game_over_text, game_over_rect)
    WIN.blit(exit_text, exit_rect)
    WIN.blit(restart_text, restart_rect)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    game_over = False

    while not game_over:
        while True:
            WIN.fill((0, 0, 0))
            snake.handle_keys()
            game_over = not snake.move()  # Check if snake.move() returns False (game over)
            if game_over:
                break
            if food.is_eaten(snake.get_head_position()):
                snake.length += 1
                food.randomize_position()
            snake.draw(WIN)
            food.draw(WIN)
            pygame.display.update()
            clock.tick(FPS)

        draw_game_over_screen()

        # Wait for user input before quitting the game
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == pygame.K_r:
                        snake.reset()
                        game_over = False

if __name__ == "__main__":
    main()
