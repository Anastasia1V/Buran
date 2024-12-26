import numpy as np
import matplotlib.pyplot as plt
from math import exp

time = 270
V = [0]
H = [0]

C = 0.4
g = 9.81
k = 3744000 / 295000
alpha = 0.82 * np.pi / 180
M2 = 19800
P2 = 374400
p0 = 101325
air_M = 0.029
R = 287
air_T = 293


def mass(t):
        return M2 - k * t


def ro(H):
    p = p0 * exp(-air_M * g * H / (R * air_T))
    return p / (R * air_T)


def v(t):
    if t == 0:
        return 0
    m = mass(t)
    term1 = m / t
    exponent = (m * g) / (R * air_T)
    term_inside_sqrt = (term1) ** 2 - (2 * (P2 - (m * g * np.cos(alpha) * exp(exponent))) ) / (C * ro(H[-1]) * p0)
    if term_inside_sqrt < 0:
        term_inside_sqrt = 0
    term2 = np.sqrt(term_inside_sqrt)
    return term1 + term2


def a_after_sep(t):
    if t == 0:
        return 0
    m = mass(t)
    rho = ro(H[-1])
    term = (-m * g * 2) / (C * rho) + (2 * P2) / (C * rho) + (m**2) / ((t * C * rho)**2)
    if term < 0:
        term = 0
    a = (np.sqrt(term) - m / (t * C * rho)) / t
    return a


X = np.arange(0, time, 1)



for i in range(1, len(X)):
    t = X[i]
    acceleration = a_after_sep(t)
    velocity = V[-1] + acceleration
    V.append(velocity)
    height = H[-1] + V[-1] * np.sin(alpha)
    H.append(height)


plt.figure(figsize=(7, 6))
plt.plot(X, V, '-r', label="Скорость относительно поверхности")
plt.legend()
plt.title("Зависимость скорости от времени, модель")
plt.xlabel("Время (с)")
plt.ylabel("Наземная скорость (м/с)")
plt.grid(True)
plt.show()
