import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

from bspline import Bspline
from nurbs import Nurbs

weight = 1

def translade(nurbs, bspline):
  ctrl_x = nurbs.x()
  ctrl_y = nurbs.y()

  diff_x = nurbs.x()[0] - bspline.x()[-1]
  diff_y = nurbs.y()[0] - bspline.y()[-1]

  for i in range(len(ctrl_x)):
    print(i, ctrl_x, ctrl_y)
    ctrl_x[i] -= diff_x
    ctrl_y[i] -= diff_y

  nurbs.update(ctrl_x, ctrl_y, nurbs.w())
  redraw_all()

def c1(bspline, nurbs):
  bspline_derivative = bspline.first_derivative(-1)
  nurbs_derivative = nurbs.first_derivative(0)
  print(bspline_derivative, nurbs_derivative)

  old_diff = diff = abs(bspline_derivative - nurbs_derivative)

  amount = 1
  direction = 'y'
  count = 0

  while diff > 0.001:
    # bspline.deslocate(-1, direction, amount)
    nurbs.deslocate(1, direction, amount)

    bspline_derivative = bspline.first_derivative(-1)
    nurbs_derivative = nurbs.first_derivative(0)
    print(bspline_derivative, nurbs_derivative)
    redraw_all()

    diff = abs(bspline_derivative - nurbs_derivative)

    if diff > old_diff+1:
      old_diff = diff
      amount *= -1
    else:
      amount = int((amount)/abs(amount)) * int(1 + diff/2)

    count += 1
    if count >= 15:
      count = 0
      direction = 'y' if direction == 'x' else 'x'
      amount = 1
      print(f'changing direction to {direction}')

  print('c1 atingido')
  return True

def c2(bspline, nurbs):
  bspline_derivative = bspline.second_derivative(-1)
  nurbs_derivative = nurbs.second_derivative(0)
  print(bspline_derivative, nurbs_derivative)


  diff = abs(bspline_derivative - nurbs_derivative)

  amount = 1
  direction = 'x'
  count = 0

  while diff > 0.001:
    amount = int((amount)/abs(amount)) * int(1 + diff/2)
    print(bspline_derivative, nurbs_derivative)

    nurbs.deslocate(2, direction, amount)

    # bspline_derivative = bspline.second_derivative(-1)
    nurbs_derivative = nurbs.second_derivative(0)
    redraw_all()

    old_diff = diff
    diff = abs(bspline_derivative - nurbs_derivative)

    if diff >= old_diff:
      amount *= -1

    count += 1
    if count >= 15:
      count = 0
      direction = 'y' if direction == 'x' else 'x'
      amount = 1
      print(f'changing direction to {direction}')

  print('c2 atingido')

def set_weight(keys, weight):
  if keys[pygame.K_0]:
    weight = 0
  if keys[pygame.K_1]:
    weight = 1
  if keys[pygame.K_2]:
    weight = 2
  if keys[pygame.K_3]:
    weight = 3
  if keys[pygame.K_4]:
    weight = 4
  if keys[pygame.K_5]:
    weight = 5
  if keys[pygame.K_6]:
    weight = 6
  if keys[pygame.K_7]:
    weight = 7
  if keys[pygame.K_8]:
    weight = 8
  if keys[pygame.K_9]:
    weight = 9

  return weight

def redraw_all(iterative=False):
  if iterative:
    screen.fill(BG)
  bspline.draw(iterative=iterative)
  nurbs.draw(iterative=iterative)

pygame.init()

BG = (51, 54, 82)
FG = (250, 208, 44)
SELECTED_DOTS = (186, 104, 131)

size = [600, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

done = False
redraw_bspline = True
redraw_nurbs = True
spline = False
weight = 1
got_c1 = False
clock = pygame.time.Clock()

bspline = Bspline(screen)
nurbs = Nurbs(screen)
redraw_all(iterative=True)

ctrl_x = nurbs.x()
ctrl_y = nurbs.y()
weights = nurbs.w()

while not done:
  clock.tick(20)

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          done=True

  keys = pygame.key.get_pressed()
  if keys[pygame.K_t]:
    translade(nurbs, bspline)
    redraw_bspline = True
    redraw_nurbs = True
    time.sleep(0.3)

  elif keys[pygame.K_c]:
    if not got_c1:
      print('buscando c1')
      got_c1 = c1(bspline, nurbs)
    else:
      print('buscando c2')
      c2(bspline, nurbs)
    time.sleep(0.3)

  elif keys[pygame.K_ESCAPE]:
    screen.fill(BG)
    pygame.display.flip()
    bspline.clear()
    nurbs.clear()
    ctrl_x = []
    ctrl_y = []
    spline = True
    got_c1 = False
    time.sleep(0.3)

  if spline and len(ctrl_x) == 9:
    if bspline.update(ctrl_x, ctrl_y):
      spline = False
      screen.fill(BG)
      bspline.draw(iterative=True)
      ctrl_x = []
      ctrl_y = []
    else:
      print('erro Bspline', len(ctrl_x))
  elif (not spline) and len(ctrl_x) == 8:
    if nurbs.update(ctrl_x, ctrl_y, weights):
      spline = True
      nurbs.draw(iterative=True)
    else:
      print('erro NURBS', len(ctrl_x))


  if spline:
    m1, m2, m3 = pygame.mouse.get_pressed()
    if m1 == 1:
      pos1, pos2 = pygame.mouse.get_pos()
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, pos2), 5)
      pygame.display.flip()

      ctrl_x.append(pos1)
      ctrl_y.append(pos2)
      time.sleep(0.3)
  else:
    keys = pygame.key.get_pressed()
    maybe_weight = set_weight(keys, weight)
    if maybe_weight:
      weight = maybe_weight

    m1, m2, m3 = pygame.mouse.get_pressed()
    if m1 == 1:
      pos1, pos2 = pygame.mouse.get_pos()
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, pos2), 1 + weight * 3)
      pygame.display.flip()

      ctrl_x.append(pos1)
      ctrl_y.append(pos2)
      weights.append(weight)
      time.sleep(0.3)
