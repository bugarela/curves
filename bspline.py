import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

k = 4
t = [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 5]
ctrl_x = [0, 50, 100, 150, 200, 250, 300, 350, 400]
ctrl_y = [0, 0, 0, 0, 500, 0, 0, 0, 0]

# k = 2
# t = [150, 160, 170, 180, 190, 200, 210]
# ctrl_x = [ 250, 300, 350, 400]
# ctrl_y = [ 500, 200, 200, 100]

n = len(t) - k - 1
u = np.arange(t[k-1],t[n+1], 0.01)

def B(i, k, x):
  if k==1:
    return (1 if t[i] <= x < t[i+1] else 0)
  else:
    b1 = B(i, k-1, x)
    safe1 = b1 * (x-t[i])/(t[i+k-1] - t[i]) if b1 > 0 else 0

    b2 = B(i+1, k-1, x)
    safe2 = b2 * (t[i+k] - x)/(t[i+k] - t[i+1]) if b2 > 0 else 0

    return safe1 + safe2

def fill_pixel_array_with_curve():

  n = len(t) - k - 1
  t.sort()
  u = np.arange(t[k-1],t[n], 0.01)
  print('ctrl_x', ctrl_x, 'ctrl_y', ctrl_y,'t', t, 'n', n, 'len(t)', len(t))

  print(t)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    for i in range(0,n):
      b = B(i, k, u[j])
      print(u[j], i, b)
      x[j] += b * ctrl_x[i]
      y[j] += b * ctrl_y[i]
    if j > 0:
      pygame.draw.line(screen, FG, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()

  # for j in range(0, len(u)-1):
  #   pygame.draw.line(screen, FG, [x[j],y[j]], [x[j+1],y[j+1]], 2)
  #   pygame.display.flip()


  return x,y


pygame.init()

BG = (51, 54, 82)
FG = (250, 208, 44)
USED_DOTS =  (233, 234, 236)
SELECTED_DOTS = (186, 104, 131)

size = [600, 600]
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
    for (x, y) in zip(ctrl_x, ctrl_y):
        pygame.draw.circle(screen, USED_DOTS, (x, y), 5)

    for x in t:
        pygame.draw.circle(screen, USED_DOTS, (x, 595), 5)

    pygame.display.flip()
    fill_pixel_array_with_curve()
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
