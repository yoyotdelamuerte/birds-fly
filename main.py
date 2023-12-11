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
avoidance_distance = 75
max_link_distance = 30
show_links_flag = False
show_concentration_flag = False
frame = 60
grid_size = 20

screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.color = (207, random.randint(110, 175), random.randint(20, 100))
        self.speed = random.uniform(1, speed_limit)
        self.last_reset_time = 0
        self.links = []

    def add_link(self, other_bird):
        self.links.append(other_bird)

    def clear_links(self):
        self.links = []

    def move(self, birds):

        avg_pos = [sum(b.x for b in birds) / len(birds), sum(b.y for b in birds) / len(birds)]
        angle_to_avg = math.atan2(avg_pos[1] - self.y, avg_pos[0] - self.x)
        self.angle += (angle_to_avg - self.angle) * cohesion_factor

        avg_angle_left = sum(b.angle for b in birds if b.angle < 0) / len(birds)
        avg_angle_right = sum(b.angle for b in birds if b.angle >= 0) / len(birds)
        self.angle += (avg_angle_left + avg_angle_right - self.angle) * alignment_factor

        for bird in birds:
            distance = math.sqrt((self.x - bird.x) ** 2 + (self.y - bird.y) ** 2)
            if separation_factor > distance > 0:
                angle_away = math.atan2(self.y - bird.y, self.x - bird.x)
                self.angle += (angle_away - self.angle) * (1 / distance)

        speed_variation = random.uniform(-0.1, 0.1)
        self.speed = max(0.1, min(speed_limit, self.speed + speed_variation))

        self.angle += random.uniform(-0.1, 0.1)
        self.angle = max(-speed_limit, min(speed_limit, self.angle))
        self.x += math.cos(self.angle) * speed_limit
        self.y += math.sin(self.angle) * speed_limit


def calculate_distance(bird1, bird2):
    return math.sqrt((bird1.x - bird2.x) ** 2 + (bird1.y - bird2.y) ** 2)


def show_links(birds, max_distance):
    for bird in birds:
        for other_bird in birds:
            if bird != other_bird:
                distance = calculate_distance(bird, other_bird)
                if distance < max_distance:
                    color_intensity = int((max_distance - distance) / max_distance * 255)
                    link_color = (255, color_intensity, color_intensity)
                    pygame.draw.line(screen, link_color, (int(bird.x), int(bird.y)),
                                     (int(other_bird.x), int(other_bird.y)), 1)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Starling Flocking Simulation")

birds = [Bird(random.uniform(height / 2, width / 2), random.uniform(width / 2, height / 2)) for _ in range(num_birds)]


def add_bird(x, y):
    birds.append(Bird(x, y))


def reset_positions(birds):
    for bird in birds:
        bird.x = width / 2
        bird.y = height / 2


def change_colors(birds):
    for bird in birds:
        bird.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def show_link(birds):
    for bird in birds:
        pass



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  ## reset birds positions
                reset_positions(birds)

            if event.key == pygame.K_KP0:  ##change birds colors
                change_colors(birds)

            if event.key == pygame.K_KP1:  ##show links between birds
                show_links_flag = not show_links_flag

            if event.key == pygame.K_KP2:  ##show concentration area birds
                show_concentration_flag = not show_concentration_flag

        elapsed_time = pygame.time.get_ticks()

    if event.type == pygame.MOUSEBUTTONDOWN:  ##add birds on click
        if event.button == 1:
            add_bird(*event.pos)

    for bird in birds:
        bird.move(birds)

        bird.x = (bird.x + width) % width
        bird.y = (bird.y + height) % height

    screen.fill(bg_color)
    if show_links_flag:
        show_links(birds, max_link_distance)

    if show_concentration_flag:
        draw_grid()
    for bird in birds:
        pygame.draw.circle(screen, bird.color, (int(bird.x), int(bird.y)), bird_radius)

    pygame.display.flip()
    pygame.time.Clock().tick(frame)
