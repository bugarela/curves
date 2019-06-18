def B(i, k, x, t):
  if k==1:
    return (1 if t[i] <= x < t[i+1] else 0)
  else:
    b1 = B(i, k-1, x, t)
    safe1 = b1 * (x-t[i])/(t[i+k-1] - t[i]) if b1 > 0 else 0

    b2 = B(i+1, k-1, x, t)
    safe2 = b2 * (t[i+k] - x)/(t[i+k] - t[i+1]) if b2 > 0 else 0

    return safe1 + safe2

# def derivative(d, x, knots, k, ctrl_y):
#   derivative = 0
#   n = len(knots) - k - 1
#   for i in range(0,n-d):
#     b = B(i+d, k-d, x, knots)
#     ctrl = k / (knots[i+k+d] - knots[i+d]) * (ctrl_y[i+d] - ctrl_y[i])
#     derivative += b * ctrl

#   return derivative


# def derivative(d, i, k, x, knots, ctrl_y):
#   if d==0:
#     return B(i, k, x, knots)

#   derivative_sum = 0
#   n = len(knots) - k - 1
#   start = 0 if d == 1 else 1
#   for i in range(start,n-1):
#     print(d, k, knots[i+k+d], knots[i+d])
#     b_first = k / (knots[i+k] - knots[i]) * derivative(d-1, i+1, k-1, x, knots, ctrl_y)
#     b_second = k / (knots[i+k+d] - knots[i+d]) * derivative(d-1, i, k-1, x, knots, ctrl_y)

#     b = b_first - b_second
#     derivative_sum += b * ctrl_y[i]

#   return derivative_sum

def derivative(d, i, k, x, knots, ctrl_y):
  derivative_sum = 0

  n = len(knots) - k - 1
  for i in range(0+d-1,n-d):
    derivative_sum += B(i, k-d, x, knots) * P(d, i, k, x, knots, ctrl_y)

  return derivative_sum

def P(d, i, k, x, knots, ctrl_y):
  if d==0:
    return ctrl_y[i]

  return (k - d + 1) / (knots[i+k+1] - knots[i+d]) * (P(d-1, i+1, k, x, knots, ctrl_y) - P(d-1, i, k, x, knots, ctrl_y))
