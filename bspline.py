import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

from de_boors import B, derivative

BG = (51, 54, 82)
class Bspline:
  def __init__(self, screen):
    self.k = 4
    self.knots = [250, 250, 250, 250, 402, 405, 410, 440, 445, 450, 450, 450, 450, 450]
    self.ctrl_x = [50, 125, 150, 175, 200, 225, 250, 260, 270]
    self.ctrl_y = [10, 220, 220, 300, 500, 300, 170, 175, 180]
    self.screen = screen
    self.curve_color = (250, 208, 44)
    self.dots_color = (219, 164, 76)

  def x(self):
    return self.ctrl_x

  def y(self):
    return self.ctrl_y

  def update(self, ctrl_x, ctrl_y):
    if len(ctrl_x) != len(self.knots) - self.k - 1:
      return False

    self.ctrl_x = ctrl_x
    self.ctrl_y = ctrl_y

    return True

  def clear(self):
    self.update([], [])

  def deslocate(self, point, direction, amount):
    if direction == 'x':
      self.ctrl_x[point] += amount
    else:
      self.ctrl_y[point] += amount

  def draw(self, iterative=False):
    self.draw_points()
    self.draw_curve(iterative)
    self.draw_points()

  def draw_points(self):
    for (x, y) in zip(self.ctrl_x, self.ctrl_y):
      pygame.draw.circle(self.screen, self.dots_color, (x, y), 4)

  def draw_curve(self, iterative):
    self.knots.sort()
    n = len(self.knots) - self.k - 1
    u = np.arange(self.knots[self.k-1],self.knots[n], 0.1)
    # print('ctrl_x', self.ctrl_x, 'ctrl_y', self.ctrl_y,'knots', self.knots, 'n', n)

    x = np.zeros(len(u))
    y = np.zeros(len(u))

    for j in range(0,len(u)):
      for i in range(0,n):
        b = B(i, self.k, u[j], self.knots)
        x[j] += b * self.ctrl_x[i]
        y[j] += b * self.ctrl_y[i]
      if iterative and j > 0:
        pygame.draw.line(self.screen, self.curve_color, [x[j-1],y[j-1]], [x[j],y[j]], 2)
        pygame.display.flip()

    if not iterative:
      self.screen.fill(BG)
      for j in range(1,len(u)):
        pygame.draw.line(self.screen, self.curve_color, [x[j-1],y[j-1]], [x[j],y[j]], 2)

  def first_derivative(self, point1, point2):
    return (
      derivative(1, 0, self.k, self.ctrl_x[point2], self.knots, self.ctrl_y)
      - derivative(1, 0, self.k, self.ctrl_x[point1], self.knots, self.ctrl_y)
    )
  def second_derivative(self, point1, point2):
    return (
      derivative(2, 0, self.k, self.ctrl_x[point2], self.knots, self.ctrl_y)
      - derivative(2, 0, self.k, self.ctrl_x[point1], self.knots, self.ctrl_y)
    )
