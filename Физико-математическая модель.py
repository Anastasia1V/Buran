import numpy as np
import matplotlib.pyplot as plt
import math

# Константы
G = 6.67430e-11  # Гравитационная постоянная, м^3/(кг*с^2)
planet_mass = 5.29e22  # Масса Кербина, кг
planet_radius = 600000  # Радиус Кербина, м
base_pressure = 101325  # Па (нормальное атмосферное давление на уровне моря)
scale_height = 7000  # м (характерная высота атмосферы Кербина)
drag_coefficient = 0.4  # Коэффициент аэродинамического сопротивления
cross_sectional_area = math.pi * (1.875**2)  # Площадь сечения ракеты, м^2
isp = 350  # Удельный импульс двигателя, с

# Исходные параметры
initial_mass = 500000  # Начальная масса, кг
fuel_mass = 400000  # Масса топлива, кг
burn_rate = 2500  # Расход топлива в секунду, кг/с
thrust = isp * 9.81 * burn_rate  # Тяга, Н

def gravitational_acceleration(altitude):
    return G * planet_mass / (planet_radius + altitude)**2

def atmospheric_pressure(altitude):
    return base_pressure * math.exp(-altitude / scale_height)

def air_density(pressure, altitude):
    return pressure / (287.05 * (288.15 - 0.0065 * altitude))

def drag_force(density, velocity):
    return 0.5 * density * velocity**2 * drag_coefficient * cross_sectional_area

# Массивы для графиков
time = []
altitude = []
velocity = []

# Начальные условия
current_mass = initial_mass
current_altitude = 0
current_velocity = 0
t = 0
dt = 0.1  # Шаг времени, с

# Основной цикл расчета
while current_mass > (initial_mass - fuel_mass):
    g = gravitational_acceleration(current_altitude)
    pressure = atmospheric_pressure(current_altitude)
    density = air_density(pressure, current_altitude)
    drag = drag_force(density, current_velocity)

    # Уравнение движения: тяга - сопротивление - гравитация
    acceleration = (thrust - drag - current_mass * g) / current_mass

    # Обновление параметров
    current_velocity += acceleration * dt
    current_altitude += current_velocity * dt
    current_mass -= burn_rate * dt
    t += dt

    # Запись данных
    time.append(t)
    altitude.append(current_altitude)
    velocity.append(current_velocity)

# Построение графиков
plt.figure(figsize=(12, 6))

# График высоты
plt.subplot(2, 1, 1)
plt.plot(time, altitude, label='Высота')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.title('Изменение высоты с течением времени')
plt.grid(True)
plt.legend()

# График скорости
plt.subplot(2, 1, 2)
plt.plot(time, velocity, label='Скорость', color='orange')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.title('Изменение скорости с течением времени')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
