import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

n = 9
k = 4
t = [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 5]
u = np.arange(t[k-1],t[n+1], 0.001)
ctrl_x = [0, 50, 100, 150, 200, 250, 300, 350, 400]
ctrl_y = [0, 0, 0, 0, 1000, 0, 0, 0, 0]

def B(i, k, x):
  xi = int(1000*x)
  if B_memo[i][k][xi] != -1:
    return B_memo[i][k][xi]
  # print(i,k,x,t[i],t[i+1])
  if k==1:
    return (1 if t[i] <= x < t[i+1] else 0)
  else:
    b1 = B(i, k-1, x)
    safe1 = b1 * (x-t[i])/(t[i+k-1] - t[i]) if b1 > 0 else 0

    b2 = B(i+1, k-1, x)
    safe2 = b2 * (t[i+k] - x)/(t[i+k] - t[i+1]) if b2 > 0 else 0

    return safe1 + safe2

def fill_pixel_array_with_curve():

  print(t)

  x = np.zeros(len(u))
  y = np.zeros(len(u))

  for j in range(0,len(u)):
    for i in range(0,n):
      x[j] += B(i, k, u[j]) * ctrl_x[i]
      y[j] += B(i, k, u[j]) * ctrl_y[i]
    print(x[j],y[j])

  for j in range(0, len(u)-1):
    pygame.draw.line(screen, WHITE, [x[j],y[j]], [x[j+1],y[j+1]], 3)

  return x,y



# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = ( 10,  10,  10)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

B_memo = [[[-1 for x in range(0,len(u))] for k in range(0,5)] for i in range(0,1000*(n+k))]

# Set the height and width of the screen
size = [500, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
redraw = True
clock = pygame.time.Clock()

control_index = 0
knot_index = 0

while not done:
  clock.tick(10)

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          done=True

  if redraw:
    screen.fill(BLACK)
    fill_pixel_array_with_curve()

    for (x, y) in zip(ctrl_x, ctrl_y):
        pygame.draw.circle(screen, BLUE, (x, y), 5)

    for x in t:
        pygame.draw.circle(screen, GREEN, (x, 495), 5)

    pygame.display.flip()
    redraw = False

  m1, m2, m3 = pygame.mouse.get_pressed()
  if m1 == 1 or m3 == 1:
    pos1, pos2 = pygame.mouse.get_pos()
    if m1 == 1:
      pygame.draw.circle(screen, RED, (pos1, pos2), 5)
      ctrl_x[control_index] = pos1
      ctrl_y[control_index] = pos2
      control_index = 0 if control_index + 1 == len(ctrl_x) else control_index + 1
    else:
      pygame.draw.circle(screen, RED, (pos1, 0), 5)
      t[knot_index] = pos1
      knot_index = 0 if knot_index + 1 == len(ctrl_x) else knot_index + 1

  pygame.display.flip()
  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    redraw = True
