import pygame
import time
import numpy as np
import matplotlib.pyplot as plt

from de_boors import B, derivative

BG = (51, 54, 82)

class Nurbs:
  def __init__(self, screen):
    self.k = 3
    self.knots = [250, 250, 250, 402, 405, 410, 440, 445, 450, 450, 450, 450]
    self.ctrl_x = [205, 250, 300, 350, 400, 450, 500, 550]
    self.ctrl_y = [405, 420, 420, 420, 460, 420, 460, 420]
    self.weights = [1, 1, 1, 1, 2, 1, 1, 1]
    self.screen = screen
    self.curve_color = (250, 208, 44)
    self.dots_color = (93, 226, 108)

  def x(self):
    return self.ctrl_x

  def y(self):
    return self.ctrl_y

  def w(self):
    return self.weights

  def update(self, ctrl_x, ctrl_y, weights):
    if len(ctrl_x) != len(self.knots) - self.k - 1:
      return False

    self.ctrl_x = ctrl_x
    self.ctrl_y = ctrl_y
    self.weights = weights

    return True

  def clear(self):
    self.update([], [], [])

  def deslocate(self, point, direction, amount):
    if direction == 'x':
      self.ctrl_x[point] += amount
    else:
      self.ctrl_y[point] += amount

  def draw(self, iterative=False):
    self.draw_points()
    self.draw_curve(iterative)

  def draw_points(self):
    for (x, y, w) in zip(self.ctrl_x, self.ctrl_y, self.weights):
      pygame.draw.circle(self.screen, self.dots_color, (x, y), w * 2)

  def draw_curve(self, iterative):
    self.knots.sort()
    n = len(self.knots) - self.k - 1
    u = np.arange(self.knots[self.k-1],self.knots[n], 0.1)
    # print('ctrl_x', self.ctrl_x, 'ctrl_y', self.ctrl_y,'knots', self.knots, 'n', n)

    x = np.zeros(len(u))
    y = np.zeros(len(u))

    for j in range(0,len(u)):
      b = np.zeros(n)
      total_weights = 0.0

      for i in range(0,n):
        b[i] = B(i, self.k, u[j], self.knots)
        total_weights += b[i] * self.weights[i]

      for i in range(0,n):
        if total_weights == 0:
          total_weights = 1
        x[j] += b[i] * self.ctrl_x[i] * self.weights[i] / total_weights
        y[j] += b[i] * self.ctrl_y[i] * self.weights[i] / total_weights

      if iterative and j > 0:
        pygame.draw.line(self.screen, self.curve_color, [x[j-1],y[j-1]], [x[j],y[j]], 2)
        pygame.display.flip()

    if not iterative:
      for j in range(1,len(u)):
        pygame.draw.line(self.screen, self.curve_color, [x[j-1],y[j-1]], [x[j],y[j]], 2)
      pygame.display.flip()

    return x,y

  def first_derivative(self, point):
    return derivative(1, 0, self.k, self.ctrl_x[point], self.knots, self.ctrl_y)

  def second_derivative(self, point):
    return derivative(2, 0, self.k, self.ctrl_x[point], self.knots, self.ctrl_y)
