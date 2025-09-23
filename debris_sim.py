import pygame
import random
import math


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
        self.color = (255, 100, 100)  

    def update(self):
        
        self.x += self.vx
        self.y += self.vy

        
        self.vy += 0.1

        
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
        self.deform = 1.0  
        self.color = (100, 255, 100)  

    def update(self):
        
        self.x += self.vx
        self.y += self.vy

        
        self.vy += 0.08

        
        if self.x <= self.size or self.x >= WIDTH - self.size:
            self.vx *= -0.6
            self.deform = 0.7  
            self.x = max(self.size, min(WIDTH - self.size, self.x))

        if self.y <= self.size or self.y >= HEIGHT - self.size:
            self.vy *= -0.6
            self.deform = 0.7  
            self.y = max(self.size, min(HEIGHT - self.size, self.y))

        
        self.deform = min(1.0, self.deform + 0.02)

    def draw(self, surface):
        
        deformed_size = int(self.size * self.deform)
        pygame.draw.ellipse(surface, self.color,
                            (self.x - deformed_size, self.y - self.size // 2,
                             deformed_size * 2, self.size))



debris_list = []
for _ in range(15):
    debris_list.append(RigidDebris(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2)))
    debris_list.append(SemiRigidDebris(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT // 2)))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            x, y = pygame.mouse.get_pos()
            debris_list.append(RigidDebris(x, y))
            debris_list.append(SemiRigidDebris(x + 20, y))

    
    screen.fill((20, 20, 40))

    
    for debris in debris_list:
        debris.update()
        debris.draw(screen)

    
    font = pygame.font.Font(None, 36)
    text = font.render("Click to add debris", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
