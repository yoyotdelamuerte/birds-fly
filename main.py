import pygame
import sys
import random
import math

pygame.init()

width, height = 800, 600
bg_color = (255, 255, 255)
bird_radius = 5
num_birds = 50
speed_limit = 5
cohesion_factor = 0.01
alignment_factor = 0.1
separation_factor = 10


class Bird:
    def __init__(self, x, y):
        """
        Initialize a bird with random initial position and angle.

        Parameters:
        - x: Initial x-coordinate of the bird.
        - y: Initial y-coordinate of the bird.
        """
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.color = (207, random.randint(110, 175), random.randint(20, 100))
        self.speed = random.uniform(1, speed_limit)

    def move(self, birds):
        """
        Move the bird based on the rules of cohesion, alignment, and separation.

        Parameters:
        - birds: List of all birds in the simulation.
        """
        # Cohesion
        avg_pos = [sum(b.x for b in birds) / len(birds), sum(b.y for b in birds) / len(birds)]
        angle_to_avg = math.atan2(avg_pos[1] - self.y, avg_pos[0] - self.x)
        self.angle += (angle_to_avg - self.angle) * cohesion_factor

        # Alignment
        avg_angle = sum(b.angle for b in birds) / len(birds)
        self.angle += (avg_angle - self.angle) * alignment_factor

        # Separation
        for bird in birds:
            distance = math.sqrt((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2)
            if distance < separation_factor and distance > 0:
                angle_away = math.atan2(self.y - bird.y, self.x - bird.x)
                self.angle += (angle_away - self.angle) * (1 / distance)

        speed_variation = random.uniform(-0.1, 0.1)
        self.speed = max(0.1, min(speed_limit, self.speed + speed_variation))
        self.angle += random.uniform(-0.1, 0.1)
        # Speed limit
        self.angle = max(-speed_limit, min(speed_limit, self.angle))
        # Update position
        self.x += math.cos(self.angle) * speed_limit
        self.y += math.sin(self.angle) * speed_limit


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Starling Flocking Simulation")

birds = [Bird(random.uniform(height / 2, width / 2), random.uniform(width / 2, height / 2)) for _ in range(num_birds)]


def reset_positions(birds):
    for bird in birds:
        bird.x = random.uniform(0, width)
        bird.y = random.uniform(0, height)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_positions(birds)

    for bird in birds:
        bird.move(birds)

        # Wrap around the screen
        bird.x = (bird.x + width) % width
        bird.y = (bird.y + height) % height

    screen.fill(bg_color)
    for bird in birds:
        pygame.draw.circle(screen, bird.color, (int(bird.x), int(bird.y)), bird_radius)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
