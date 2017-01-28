from boid3 import Boid
import pygame

window_width = 1000
window_height = 600
boid_width = 40
boid_height = 20
boid_color = 255, 255, 255
background_color = 0, 0, 0
fps = 60

flock = []
running = True

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif (event.type == pygame.MOUSEBUTTONDOWN and
              all(boid.position.coordinates != event.pos for boid in flock)):
            flock.append(Boid(event.pos))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            global running
            running = not running
    return True

def draw_boid(boid):
    surface = pygame.Surface((boid_width, boid_height), pygame.SRCALPHA).convert_alpha()
    pygame.draw.polygon(surface, boid_color,
                        [(0, 0), (boid_width, boid_height / 2), (0, boid_height)])
    rotated = pygame.transform.rotate(surface, -boid.angle)
    center = boid.position - (boid_width / 2, boid_height / 2)
    screen.blit(rotated, center.coordinates)

pygame.init()
icon = pygame.Surface((32, 32))
icon.set_alpha(0)
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flocking')
clock = pygame.time.Clock()

while check_events():
    screen.fill(background_color)
    if running:
        flock = [boid.update(flock) for boid in flock]
    for boid in flock:
        boid.position %= window_width, window_height
        draw_boid(boid)
    pygame.display.update()
    clock.tick(fps)