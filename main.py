import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

k_bspline = 4
bspline_knots = [0, 0, 0, 0, 10, 10, 20, 30, 40, 50, 50, 50, 50, 50]
bspline_ctrl_x = [0, 50, 100, 150, 200, 250, 300, 350, 400]
bspline_ctrl_y = [20, 20, 20, 20, 500, 20, 20, 20, 20]

k_nurbs = 3
nurbs_knots = [400, 400, 400, 402, 405, 410, 440, 445, 450, 450, 450, 450]
nurbs_ctrl_x = [405, 450, 500, 550, 700, 850, 900, 950]
nurbs_ctrl_y = [405, 420, 420, 420, 460, 420, 460, 420]
nurbs_weights = [1, 1, 1, 1, 2, 1, 1, 1]
weight = 1

def B(i, k, x, t):
  if k==1:
    return (1 if t[i] <= x < t[i+1] else 0)
  else:
    b1 = B(i, k-1, x, t)
    safe1 = b1 * (x-t[i])/(t[i+k-1] - t[i]) if b1 > 0 else 0

    b2 = B(i+1, k-1, x, t)
    safe2 = b2 * (t[i+k] - x)/(t[i+k] - t[i+1]) if b2 > 0 else 0

    return safe1 + safe2

def draw_bspline():
  bspline_knots.sort()
  n = len(bspline_knots) - k_bspline - 1
  u = np.arange(bspline_knots[k_bspline-1],bspline_knots[n], 0.1)
  # print('ctrl_x', bspline_ctrl_x, 'ctrl_y', bspline_ctrl_y,'knots', bspline_knots, 'n', n)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    for i in range(0,n):
      b = B(i, k_bspline, u[j], bspline_knots)
      x[j] += b * bspline_ctrl_x[i]
      y[j] += b * bspline_ctrl_y[i]
    if j > 0:
      pygame.draw.line(screen, FG, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()

  return x,y

def draw_nurbs():
  nurbs_knots.sort()
  n = len(nurbs_knots) - k_nurbs - 1
  u = np.arange(nurbs_knots[k_nurbs-1],nurbs_knots[n], 0.1)
  # print('ctrl_x', nurbs_ctrl_x, 'ctrl_y', nurbs_ctrl_y,'knots', nurbs_knots, 'n', n)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    b = np.zeros(n)
    total_weights = 0.0

    for i in range(0,n):
      b[i] = B(i, k_nurbs, u[j], nurbs_knots)
      total_weights += b[i] * nurbs_weights[i]

    for i in range(0,n):
      if total_weights == 0:
        total_weights = 1
      x[j] += b[i] * nurbs_ctrl_x[i] * nurbs_weights[i] / total_weights
      y[j] += b[i] * nurbs_ctrl_y[i] * nurbs_weights[i] / total_weights

    if j > 0:
      pygame.draw.line(screen, FG, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()

  return x,y

def translade(nurbs_ctrl_x, nurbs_ctrl_y):
  last_bspline_x = bspline_ctrl_x[-1]
  last_bspline_y = bspline_ctrl_y[-1]

  first_nurbs_x = nurbs_ctrl_x[0]
  first_nurbs_y = nurbs_ctrl_y[0]

  for i in range(len(nurbs_ctrl_x)):
    nurbs_ctrl_x[i] -= first_nurbs_x - last_bspline_x
    nurbs_ctrl_y[i] -= first_nurbs_y - last_bspline_y

    print(first_nurbs_y + last_bspline_y)
    # for (x, y, w) in zip(nurbs_ctrl_x, nurbs_ctrl_y, nurbs_weights):
    #   pygame.draw.circle(screen, NURBS_DOTS, (x, y), 1 + w * 3)
    #   pygame.display.flip()

  return [nurbs_ctrl_x, nurbs_ctrl_y]

def c1(bspline_ctrl_x):
  last_bspline_x = bspline_ctrl_x[-1]


  bspline = first_derivative(bspline_ctrl_x[-1], bspline_knots, k_bspline, bspline_ctrl_y)
  nurbs = first_derivative(bspline_ctrl_x[-1], nurbs_knots, k_nurbs, nurbs_ctrl_y)

  while bspline != nurbs:
    print(bspline, nurbs)
    nurbs_ctrl_y[0] += 1
    bspline_ctrl_y[-1] += 1

    bspline = first_derivative(bspline_ctrl_x[-1], bspline_knots, k_bspline, bspline_ctrl_y)
    nurbs = first_derivative(bspline_ctrl_x[-1], nurbs_knots, k_nurbs, nurbs_ctrl_y)
    screen.fill(BG)
    for (x, y) in zip(bspline_ctrl_x, bspline_ctrl_y):
        pygame.draw.circle(screen, BSPLINE_DOTS, (x, y), 5)
    draw_bspline()
    for (x, y, w) in zip(nurbs_ctrl_x, nurbs_ctrl_y, nurbs_weights):
        pygame.draw.circle(screen, NURBS_DOTS, (x, y), 1 + w * 3)
    draw_nurbs()

def first_derivative(x, knots, k, ctrl_y):
  derivative = 0
  n = len(knots) - k - 1
  for i in range(0,n-1):
    b = B(i+1, k-1, x, knots)
    ctrl = k / (knots[i+k+1] - knots[i+1]) * (ctrl_y[i+1] - ctrl_y[i])
    derivative += b * ctrl

  return derivative

def nurbs_first_derivative(x):
  derivative_nurbs = 0
  n = len(nurbs_knots) - k_nurbs - 1
  for i in range(0,n):
    b = B(i, k_nurbs-1, x, nurbs_knots)
    derivative_nurbs += b * nurbs_ctrl_y[i]

  return derivative_nurbs

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

pygame.init()

BG = (51, 54, 82)
FG = (250, 208, 44)
BSPLINE_DOTS =  (233, 234, 236)
NURBS_DOTS = (93, 226, 108)
SELECTED_DOTS = (186, 104, 131)

size = [1200, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

done = False
redraw_bspline = True
redraw_nurbs = True
spline = False
weight = 1
clock = pygame.time.Clock()
screen.fill(BG)

while not done:
  clock.tick(20)

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          done=True

  if redraw_bspline:
    screen.fill(BG)
    for (x, y) in zip(bspline_ctrl_x, bspline_ctrl_y):
        pygame.draw.circle(screen, BSPLINE_DOTS, (x, y), 5)
    draw_bspline()
    redraw_bspline = False

  if redraw_nurbs:
    for (x, y, w) in zip(nurbs_ctrl_x, nurbs_ctrl_y, nurbs_weights):
        pygame.draw.circle(screen, NURBS_DOTS, (x, y), 1 + w * 3)
    draw_nurbs()
    redraw_nurbs = False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_t]:
    nurbs_ctrl_x, nurbs_ctrl_y = translade(nurbs_ctrl_x, nurbs_ctrl_y)
    redraw_bspline = True
    redraw_nurbs = True
  elif keys[pygame.K_c]:
    c1(bspline_ctrl_x)
    # nurbs_ctrl_x, nurbs_ctrl_y = translade(nurbs_ctrl_x, nurbs_ctrl_y)
    # redraw_bspline = True
    # redraw_nurbs = True
  elif keys[pygame.K_ESCAPE]:
    screen.fill(BG)
    pygame.display.flip()
    bspline_ctrl_x = []
    bspline_ctrl_y = []
    nurbs_ctrl_x = []
    nurbs_ctrl_y = []
    nurbs_weights = []
    time.sleep(0.3)

  if spline:
    m1, m2, m3 = pygame.mouse.get_pressed()
    if m1 == 1:
      pos1, pos2 = pygame.mouse.get_pos()
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, pos2), 5)
      pygame.display.flip()

      bspline_ctrl_x.append(pos1)
      bspline_ctrl_y.append(pos2)
      time.sleep(0.3)
  else:
    keys = pygame.key.get_pressed()
    maybe_weight = set_weight(keys, weight)
    if maybe_weight:
      weight = maybe_weight

    m1, m2, m3 = pygame.mouse.get_pressed()
    if m1 == 1:
      pos1, pos2 = pygame.mouse.get_pos()
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, pos2), 1 + w * 3)
      pygame.display.flip()

      nurbs_ctrl_x.append(pos1)
      nurbs_ctrl_y.append(pos2)
      nurbs_weights.append(weight)
      time.sleep(0.3)



  pygame.display.flip()
  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    if spline:
      if len(bspline_ctrl_x) == len(bspline_knots) - k_bspline - 1:
        spline = False
        redraw_bspline = True
      else:
        bspline_ctrl_x = []
        bspline_ctrl_y = []
        print('erro Bspline', len(bspline_ctrl_xs))
    else:
      if len(nurbs_ctrl_x) == len(nurbs_knots) - k_nurbs - 1:
        redraw_nurbs = True
      else:
        print('erro NURBS', len(nurbs_ctrl_x))
        nurbs_ctrl_x = []
        nurbs_ctrl_y = []
        nurbs_weights = []
    time.sleep(0.3)
