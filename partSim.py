import pygame
import sys
import time
import math

# Particle class
class Particle:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def update_velocity(self, ax, ay, dt):
        self.vx += ax * dt
        self.vy += ay * dt

    def apply_gravity(self, other, dt, G=6.67430e-11):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        force = G * self.mass * other.mass / (distance**2)

        ax = force * dx / (distance * self.mass)
        ay = force * dy / (distance * self.mass)

        self.update_velocity(ax, ay, dt)

def draw_solar_system(screen, particles, scale):
    width, height = screen.get_size()
    for particle in particles:
        screen_x = int((particle.x / scale) + (width // 2))
        screen_y = int((particle.y / scale) + (height // 2))
        if 0 <= screen_x <= width and 0 <= screen_y <= height:
            pygame.draw.circle(screen, particle.color, (screen_x, screen_y), particle.radius)

# Main function
def main():
    # Pygame setup
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Solar System Simulation')
    clock = pygame.time.Clock()

    # Initialize solar system's particles
    sun = Particle(0, 0, 0, 0, 1.989e30, 10, (255, 255, 0))
    mercury = Particle(57.9e9*1.5, 0, 0, 47.87e3, 3.301e23, 1, (139, 69, 19))
    venus = Particle(108.2e9*1.5, 0, 0, 35.02e3, 4.867e24, 2, (255, 140, 0))
    earth = Particle(147e9*1.75, 0, 0, 29.5e3, 5.972e24, 3, (0, 0, 255))

    particles = [sun, mercury, venus, earth]

    # Simulation parameters
    dt = 60 * 60 * 24  # Time step: 1 day

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((128, 128, 128))

        for i, particle in enumerate(particles):
            for other in particles[:i] + particles[i + 1:]:
                particle.apply_gravity(other, dt)

            particle.update_position(dt)

        draw_solar_system(screen, particles, scale=1e10)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

