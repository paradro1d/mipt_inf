import pygame
import numpy as np
import yaml

# Для изменения формы и параметров фигур используйте файл figures.yml
# Считывание figures.yml:
figures = yaml.load(open('figures.yml'), Loader=yaml.Loader)
branch_coordinates = figures["branch"]
cloud_coordinates = figures["cloudlet"]
size = figures["size"]
BLACK = figures["BLACK"]
WHITE = figures["WHITE"]
color = figures["colors"]
trunk = figures["trunk"]

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PHYSTECH VILLAGE")

done = False
clock = pygame.time.Clock()


def background(surface, width, height):
    '''
    Функция прорисовывает задний фон картинки.
    surface - объект pygame.Surface - поверхность картинки .
    width, height - ширина и высота картинки
    '''
    pygame.draw.rect(surface, color[6], (0, 0, width, height))
    pygame.draw.rect(surface, color[5], (0, 0, width, height // 2))


def house(surface, x, y, width, height):
    '''
    Функция рисует дом.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x, y - координаты верхней левой точки картинки дома.
    width, height - ширина и высота дома в пикселях.
    '''
    house_surface = pygame.Surface((585, 570), pygame.SRCALPHA)
    house_surface_scaled = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(
        house_surface, color[4], [(0, 150), (290, 0), (580, 150)])
    pygame.draw.polygon(
        house_surface, BLACK, [(0, 150), (290, 0), (580, 150)], 5)
    pygame.draw.rect(house_surface, color[1], (0, 150, 585, 420))
    pygame.draw.rect(house_surface, BLACK, (0, 150, 585, 420), 5)
    pygame.draw.rect(house_surface, color[2], (195, 300, 170, 150))
    pygame.draw.rect(house_surface, color[3], (200, 305, 160, 140))
    pygame.transform.smoothscale(
        house_surface, (width, height), house_surface_scaled)
    surface.blit(house_surface_scaled, (x, y))


def sun(surface, x, y, r, n):
    '''
    Функция рисует треугольчатое солнце.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x, y - координаты центра солнца.
    r - радиус солнца.
    n - натуральное число треугольников.
    '''
    angles = []
    angles_x_even = [
        int(np.cos(np.pi * i / n) * r + x) for i in range(0, 2 * n, 2)]
    angles_x_odd = [
        int(np.cos(np.pi * i / n) * 1.2 * r + x) for i in range(1, 2 * n, 2)]
    angles_y_even = [
        int(np.sin(np.pi * i / n) * r + y) for i in range(0, 2 * n, 2)]
    angles_y_odd = [
        int(np.sin(np.pi * i / n) * 1.2 * r + y) for i in range(1, 2 * n, 2)]
    c = []
    for i in range(n):
        c.append((angles_x_even[i], angles_y_even[i]))
        c.append((angles_x_odd[i], angles_y_odd[i]))
    pygame.draw.polygon(surface, color[7], c)
    pygame.draw.polygon(surface, BLACK, c, 1)


def branch(surface, x, y, r):
    '''
    Функция рисует листву дерева в виде зелёного круга.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x, y - координаты центра круга.
    r - целое число, обозначающее радиус круга в пикселях.
    '''
    pygame.draw.circle(surface, BLACK, (x, y), int(1.05 * r))
    pygame.draw.circle(surface, color[0], (x, y), r)


def tree(surface, x, y, width, height):
    '''
    Функция рисует дерево.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x, y - координаты верхнего левого угла изображения дерева.
    width, height - ширина и высота дерева в пикселях.
    '''
    x_surface = int(max([i[0] + 1.05 * i[2] for i in branch_coordinates]))
    y_surface = trunk[1][1]
    tree_surface = pygame.Surface((x_surface, y_surface), pygame.SRCALPHA)
    tree_surface_scaled = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.line(tree_surface, BLACK, trunk[0], trunk[1], trunk[2])
    for i in branch_coordinates:
        branch(tree_surface, i[0], i[1], i[2])
    pygame.transform.smoothscale(
        tree_surface, (width, height), tree_surface_scaled)
    surface.blit(tree_surface_scaled, (x, y))


def cloud(surface, x, y, r):
    '''
    Функция рисует круглое облачко.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x,y - координаты центра круга.
    r - радиус облака.
    '''
    pygame.draw.circle(surface, BLACK, (x, y), int(r * 1.05))
    pygame.draw.circle(surface, WHITE, (x, y), r)


def cloudlet(surface, x, y, width, height):
    '''
    Функция рисует тучу из облаков.
    surface - объект pygame.Surface (поверхность,
    на которой требуется изобразить объект).
    x, y - координаты верхнего левого угла изображения тучи.
    width, height - ширина и высота облака в пикселях.
    '''
    x_surface = int(max([i[0] + 1.05 * i[2] for i in cloud_coordinates]))
    y_surface = int(max([i[1] + 1.05 * i[2] for i in cloud_coordinates]))
    clouds_surface = pygame.Surface((x_surface, y_surface), pygame.SRCALPHA)
    clouds_surface_scaled = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in cloud_coordinates:
        cloud(clouds_surface, i[0], i[1], i[2])
    pygame.transform.smoothscale(
        clouds_surface, (width, height), clouds_surface_scaled)
    surface.blit(clouds_surface_scaled, (x, y))


while not done:
    clock.tick(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    background(screen, size[0], size[1])

    house(screen, 250, 125, 117, 114)

    tree(screen, 168, 128, 80, 107)
    tree(screen, 780, 178, 67, 89)
    tree(screen, 340, 178, 67, 89)

    sun(screen, 340, 40, 30, 20)

    house(screen, 600, 156, 117, 114)
    house(screen, 16, 96, 140, 137)

    cloudlet(screen, 20, 10, 102, 54)
    cloudlet(screen, 220, 30, 102, 54)
    cloudlet(screen, 570, 30, 153, 81)
    cloudlet(screen, 500, 0, 102, 54)
    cloudlet(screen, 380, 60, 102, 54)

    pygame.display.flip()

pygame.quit()
