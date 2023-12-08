import pygame
import sys
import random
import math

pygame.init()

width, height = 1000, 700
bg_color = (255, 255, 255)
bird_radius = 3
num_birds = 100
speed_limit = 5
cohesion_factor = 0.01
alignment_factor = 0.1
separation_factor = 10
avoidance_distance = 100


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.color = (207, random.randint(110, 175), random.randint(20, 100))
        self.speed = random.uniform(1, speed_limit)


    def move(self, birds):

        avg_pos = [sum(b.x for b in birds) / len(birds), sum(b.y for b in birds) / len(birds)]
        angle_to_avg = math.atan2(avg_pos[1] - self.y, avg_pos[0] - self.x)
        self.angle += (angle_to_avg - self.angle) * cohesion_factor

        avg_angle_left = sum(b.angle for b in birds if b.angle < 0) / len(birds)
        avg_angle_right = sum(b.angle for b in birds if b.angle >= 0) / len(birds)
        self.angle += (avg_angle_left + avg_angle_right - self.angle) * alignment_factor

        for bird in birds:
            distance = math.sqrt((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2)
            if distance < separation_factor and distance > 0:
                angle_away = math.atan2(self.y - bird.y, self.x - bird.x)
                self.angle += (angle_away - self.angle) * (1 / distance)

        speed_variation = random.uniform(-0.1, 0.1)
        self.speed = max(0.1, min(speed_limit, self.speed + speed_variation))

        self.angle += random.uniform(-0.1, 0.1)
        self.angle = max(-speed_limit, min(speed_limit, self.angle))
        self.x += math.cos(self.angle) * speed_limit
        self.y += math.sin(self.angle) * speed_limit


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Starling Flocking Simulation")

birds = [Bird(random.uniform(height / 2, width / 2), random.uniform(width / 2, height / 2)) for _ in range(num_birds)]


def add_bird(x, y):
    birds.append(Bird(x, y))


def reset_positions(birds):
    for bird in birds:
        bird.x = width / 2
        bird.y = height / 2


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_positions(birds)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                add_bird(*event.pos)

    for bird in birds:
        bird.move(birds)

        bird.x = (bird.x + width) % width
        bird.y = (bird.y + height) % height

    screen.fill(bg_color)
    for bird in birds:
        pygame.draw.circle(screen, bird.color, (int(bird.x), int(bird.y)), bird_radius)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
