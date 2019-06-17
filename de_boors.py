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
    derivative_sum += generic_b(d, i, k, x, knots) * (ctrl_y[i+1] - ctrl_y[i])

  return derivative_sum

def generic_b(d, i, k, x, knots):
  if d==0:
    return B(i, k, x, knots)

  if (knots[i+k] - knots[i]) == 0:
    print(generic_b(d-1, i, k-1, x, knots))
  if (knots[i+k+1] - knots[i+1]) == 0:
    print(generic_b(d-1, i, k-1, x, knots))

  b_first = k * (generic_b(d-1, i, k-1, x, knots) / (knots[i+k] - knots[i]))
  b_second = k * (generic_b(d-1, i+1, k-1, x, knots) / (knots[i+k+1] - knots[i+1]))

  return b_first - b_second
