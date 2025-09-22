import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debris Simulation")
clock = pygame.time.Clock()


class RigidDebris:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.size = random.randint(8, 15)
        self.color = (255, 100, 100)  # Red for rigid

    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Gravity
        self.vy += 0.1

        # Bounce off walls
        if self.x <= self.size or self.x >= WIDTH - self.size:
            self.vx *= -0.8
            self.x = max(self.size, min(WIDTH - self.size, self.x))

        if self.y <= self.size or self.y >= HEIGHT - self.size:
            self.vy *= -0.8
            self.y = max(self.size, min(HEIGHT - self.size, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class SemiRigidDebris:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.size = random.randint(10, 18)
        self.deform = 1.0  # Deformation factor
        self.color = (100, 255, 100)  # Green for semi-rigid

    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Gravity
        self.vy += 0.08

        # Bounce with deformation
        if self.x <= self.size or self.x >= WIDTH - self.size:
            self.vx *= -0.6
            self.deform = 0.7  # Compress on impact
            self.x = max(self.size, min(WIDTH - self.size, self.x))

        if self.y <= self.size or self.y >= HEIGHT - self.size:
            self.vy *= -0.6
            self.deform = 0.7  # Compress on impact
            self.y = max(self.size, min(HEIGHT - self.size, self.y))

        # Recover deformation
        self.deform = min(1.0, self.deform + 0.02)

    def draw(self, surface):
        # Draw deformed ellipse
        deformed_size = int(self.size * self.deform)
        pygame.draw.ellipse(surface, self.color,
                            (self.x - deformed_size, self.y - self.size // 2,
                             deformed_size * 2, self.size))


# Create debris
debris_list = []
for _ in range(15):
    debris_list.append(RigidDebris(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2)))
    debris_list.append(SemiRigidDebris(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2)))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Add debris at mouse position
            x, y = pygame.mouse.get_pos()
            debris_list.append(RigidDebris(x, y))
            debris_list.append(SemiRigidDebris(x + 20, y))

    # Clear screen
    screen.fill((20, 20, 40))

    # Update and draw debris
    for debris in debris_list:
        debris.update()
        debris.draw(screen)

    # Draw instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Click to add debris", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()