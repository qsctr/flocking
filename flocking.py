from boid3 import Boid
from os import system
import pygame
from random import randrange
from vector import average

window_width = 800
window_height = 600
background_color = 0, 0, 0
icon_color = 255, 255, 255
icon_size = 256
fps = 30

flock = []
running = True
mouse_pos = None
mouse_on = False

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flocking')
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 100)
icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA).convert_alpha()

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # right click
                global mouse_on
                mouse_on = not mouse_on
                update_console()
            elif empty(event.pos):
                flock.append(Boid(event.pos))
                update_console()
        elif event.type == pygame.MOUSEMOTION:
            global mouse_pos
            mouse_pos = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                global running
                running = not running
                update_console()
            elif event.key == pygame.K_RETURN:
                for i in range(100):
                    pos = randrange(window_width), randrange(window_height)
                    if empty(pos):
                        flock.append(Boid(pos))
                        update_console()
                        break
            elif event.key == pygame.K_BACKSPACE and flock:
                flock.pop()
                update_console()
            elif event.key in keys:
                attr, diff = keys[event.key]
                prev = getattr(Boid, attr)
                if event.mod in [pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT]:
                    setattr(Boid, attr, prev - diff)
                else:
                    setattr(Boid, attr, prev + diff)
                update_console()
    return True

def empty(pos):
    return all(boid.position.coordinates != pos for boid in flock)

keys = {
    pygame.K_1: ('max_speed', 0.5),
    pygame.K_2: ('max_force', 0.01),
    pygame.K_3: ('separation_radius', 20),
    pygame.K_4: ('neighbor_radius', 20),
    pygame.K_5: ('separation_weight', 0.2),
    pygame.K_6: ('alignment_weight', 0.2),
    pygame.K_7: ('cohesion_weight', 0.2),
    pygame.K_8: ('speed_multiplier', 0.2),
    pygame.K_9: ('width', 5),
    pygame.K_0: ('height', 5)
}

def update_console():
    system('cls')
    print('Flocking')
    print()
    print('Left click to add a boid at the mouse pointer')
    print('Right click to toggle follow mouse')
    print('Press enter to add a boid at a random location')
    print('Press backspace to delete the last boid')
    print('Press space to pause/continue')
    print('Press the number to increase the corresponding value')
    print('Hold shift to decrease')
    print()
    for key, (name, _) in keys.items():
        print(f'[{pygame.key.name(key)}] {name} = {getattr(Boid, name):.2f}')
    print()
    print(f'Running: {running}')
    print(f'Follow mouse: {mouse_on}')
    print(f'Boid count: {len(flock)}')

def draw_boid(boid):
    surface = pygame.Surface((boid.width, boid.height), pygame.SRCALPHA).convert_alpha()
    pygame.draw.polygon(surface, boid.color,
                        [(0, 0), (boid.width, boid.height / 2), (0, boid.height)])
    rotated = pygame.transform.rotate(surface, -boid.velocity.angle)
    center = boid.position - (boid.width / 2, boid.height / 2)
    screen.blit(rotated, center.coordinates)

def update_icon():
    if flock:
        avg_angle = average([boid.velocity for boid in flock]).angle
        longer = icon_size
        shorter = icon_size * (Boid.height / Boid.width)
        if Boid.width > boid.height:
            width = longer
            height = shorter
        else:
            width = shorter
            height = longer
        surface = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA).convert_alpha()
        pygame.draw.polygon(surface, (255, 255, 255), [
            (icon_size / 2 - width / 2, icon_size / 2 - height / 2),
            (icon_size / 2 + width / 2, 128),
            (icon_size / 2 - width / 2, icon_size / 2 + height / 2)
        ])
        rotated = pygame.transform.rotate(surface, -avg_angle)
        pygame.transform.scale(rotated, (icon_size, icon_size), icon)
    else:
        icon.fill((0, 0, 0, 0))
    pygame.display.set_icon(icon)

update_console()

while check_events():
    if running:
        screen.fill(background_color)
        flock = [boid.update(flock, mouse_pos if mouse_on else None) for boid in flock]
        for boid in flock:
            boid.position %= window_width, window_height
            draw_boid(boid)
        pygame.display.update()
        update_icon()
    clock.tick(fps)
