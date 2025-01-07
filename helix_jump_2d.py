import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helix Jump 2D")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
BALL_RADIUS = 10

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def jump(self):
        self.vel_y = JUMP_STRENGTH

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

def generate_platforms(num_platforms):
    platforms = []
    for i in range(num_platforms):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = HEIGHT - (i + 1) * 100
        platforms.append(Platform(x, y))
    return platforms

def main():
    clock = pygame.time.Clock()
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    platforms = generate_platforms(5)
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.jump()

        ball.update()

        # Check for collisions with platforms
        for platform in platforms:
            if (ball.y + BALL_RADIUS > platform.y and
                ball.y + BALL_RADIUS < platform.y + PLATFORM_HEIGHT and
                ball.x > platform.x and ball.x < platform.x + PLATFORM_WIDTH):
                ball.y = platform.y - BALL_RADIUS
                ball.vel_y = 0
                score += 1

        # Move platforms up
        for platform in platforms:
            platform.y += 1

        # Remove platforms that are off-screen and add new ones
        platforms = [p for p in platforms if p.y < HEIGHT]
        while len(platforms) < 5:
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = platforms[-1].y - 100
            platforms.append(Platform(x, y))

        # Check if ball is off-screen
        if ball.y > HEIGHT:
            print(f"Game Over! Score: {score}")
            pygame.quit()
            sys.exit()

        # Draw everything
        screen.fill(WHITE)
        ball.draw()
        for platform in platforms:
            platform.draw()

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()