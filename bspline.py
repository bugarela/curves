import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

k = 4
bspline_knots = [0, 0, 0, 0, 0, 10, 20, 30, 40, 50, 50, 50, 50, 50]
bspline_ctrl_x = [0, 50, 100, 150, 200, 250, 300, 350, 400]
bspline_ctrl_y = [0, 0, 0, 0, 500, 0, 0, 0, 0]

nurbs_knots = [0, 0, 0, 0, 0, 10, 20, 30, 40, 50, 50, 50, 50, 50]
nurbs_ctrl_x = [0, 50, 100, 150, 200, 250, 300, 350, 400]
nurbs_ctrl_y = [0, 0, 0, 0, 500, 0, 0, 0, 0]
# nurbs_knots = [400, 400, 400, 400, 400, 410, 420, 430, 440, 450, 450, 450, 450, 450]
# nurbs_ctrl_x = [400, 450, 500, 550, 700, 850, 900, 950, 1000]
# nurbs_ctrl_y = [30, 45, 50, 55, 10, 85, 90, 95, 100]
nurbs_weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]

# n = len(t) - k - 1
# u = np.arange(t[k-1],t[n], 0.01)

def B(i, k, x, t):
  if k==1:
    return (1 if t[i] < x <= t[i+1] else 0)
  else:
    b1 = B(i, k-1, x, t)
    safe1 = b1 * (x-t[i])/(t[i+k-1] - t[i]) if b1 > 0 else 0

    b2 = B(i+1, k-1, x, t)
    safe2 = b2 * (t[i+k] - x)/(t[i+k] - t[i+1]) if b2 > 0 else 0

    return safe1 + safe2

def draw_bspline():
  bspline_knots.sort()
  n = len(bspline_knots) - k - 1
  u = np.arange(bspline_knots[k-1],bspline_knots[n], 0.01)
  print('ctrl_x', bspline_ctrl_x, 'ctrl_y', bspline_ctrl_y,'knots', bspline_knots, 'n', n)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    for i in range(0,n):
      b = B(i, k, u[j], bspline_knots)
      x[j] += b * bspline_ctrl_x[i]
      y[j] += b * bspline_ctrl_y[i]
    if j > 0:
      pygame.draw.line(screen, FG, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()

  return x,y

def draw_nurbs():
  nurbs_knots.sort()
  n = len(nurbs_knots) - k - 1
  u = np.arange(nurbs_knots[k-1],nurbs_knots[n], 0.01)
  print('ctrl_x', nurbs_ctrl_x, 'ctrl_y', nurbs_ctrl_y,'knots', nurbs_knots, 'n', n)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    b = np.zeros(n)
    total_weights = 0.0
    for i in range(0,n):
      b[i] = B(i, k, u[j], nurbs_knots)
      total_weights += b[i] * nurbs_weights[i]
    for i in range(0,n):
      if total_weights == 0:
        total_weights = 1
      print(b[i], nurbs_ctrl_x[i], nurbs_weights[i], total_weights)
      x[j] += b[i] * nurbs_ctrl_x[i] * nurbs_weights[i] / total_weights
      y[j] += b[i] * nurbs_ctrl_y[i] * nurbs_weights[i] / total_weights
      print(x[j], y[j])
    if j > 0:
      pygame.draw.line(screen, FG, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()


  return x,y


pygame.init()

BG = (51, 54, 82)
FG = (250, 208, 44)
USED_DOTS =  (233, 234, 236)
SELECTED_DOTS = (186, 104, 131)

size = [1200, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

done = False
redraw = True
clock = pygame.time.Clock()

while not done:
  clock.tick(20)

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          done=True

  if redraw:
    screen.fill(BG)
    for (x, y) in zip(bspline_ctrl_x, bspline_ctrl_y):
        pygame.draw.circle(screen, USED_DOTS, (x, y), 5)

    for (x, y) in zip(nurbs_ctrl_x, nurbs_ctrl_y):
        pygame.draw.circle(screen, FG, (x, y), 5)

    # for x in t:
    #     pygame.draw.circle(screen, USED_DOTS, (x, 595), 5)

    pygame.display.flip()
    # draw_bspline()
    draw_nurbs()
    redraw = False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    screen.fill(BG)
    pygame.display.flip()
    t = []
    ctrl_x = []
    ctrl_y = []
    time.sleep(0.3)

  m1, m2, m3 = pygame.mouse.get_pressed()
  if m1 == 1 or m3 == 1:
    pos1, pos2 = pygame.mouse.get_pos()
    if m1 == 1:
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, pos2), 5)
      pygame.display.flip()

      ctrl_x.append(pos1)
      ctrl_y.append(pos2)
    else:
      pygame.draw.circle(screen, SELECTED_DOTS, (pos1, 595), 5)
      pygame.display.flip()

      t.append(pos1)
    time.sleep(0.3)


  pygame.display.flip()
  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    if len(ctrl_x) == len(t) - k - 1:
      redraw = True
    else:
      n = len(t) - k - 1
      screen.fill(BG)
      pygame.display.flip()

      print('ERRO')
      print('ctrl_x', ctrl_x, 'ctrl_y', ctrl_y,'t', t)
      print('Nós:', len(t))
      print('Pontos de controle:', n, 'len(ctrl_x)', len(ctrl_x))
      t = []
      ctrl_x = []
      ctrl_y = []

    time.sleep(0.3)
