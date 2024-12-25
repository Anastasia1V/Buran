import krpc
import time
import math

# Подключение к KSP
conn = krpc.connect(name='Буран Автопилот')
vessel = conn.space_center.active_vessel

# Подготовка файлов для записи данных
altitude_file = open('Высота_относительно_планеты.txt', 'w')
speed_file = open('Скорость_относительно_планеты.txt', 'w')

altitude_file.write("Time (s)\tAltitude (m)\n")
speed_file.write("Time (s)\tSpeed (m/s)\n")

# Получение референсов
flight = vessel.flight()
orbit = vessel.orbit

# Функция расчета скорости по формуле Циолковского
def tsiolkovsky_velocity(isp, initial_mass, final_mass):
    g0 = 9.81  # Ускорение свободного падения на поверхности Кербина (аналогично Земле)
    return isp * g0 * math.log(initial_mass / final_mass)

# Функция для расчёта силы аэродинамического сопротивления
def drag_force(density, velocity, drag_coefficient, cross_sectional_area):
    return 0.5 * density * velocity**2 * drag_coefficient * cross_sectional_area

# Функция для расчёта изменения давления с высотой (барометрическая формула)
def atmospheric_pressure(base_pressure, scale_height, altitude):
    return base_pressure * math.exp(-altitude / scale_height)

# Константы для расчётов
base_pressure = 101325  # Па (нормальное давление на уровне моря)
scale_height = 7000  # м (характерная высота атмосферы Кербина)
drag_coefficient = 0.4  # Коэффициент аэродинамического сопротивления
cross_sectional_area = math.pi * (1.875**2)  # Площадь сечения ракеты

def gravitational_acceleration(planet_mass, radius, altitude):
    G = 6.67430e-11  # Гравитационная постоянная
    return G * planet_mass / (radius + altitude)**2

planet_mass = 5.29e22  # Масса Кербина в кг
planet_radius = 600000  # Радиус Кербина в метрах

# Константы ступеней
stages = [
    {"isp": 350, "initial_mass": 500000, "final_mass": 100000},  # 1-я ступень
    {"isp": 450, "initial_mass": 100000, "final_mass": 25000},   # 2-я ступень
    {"isp": 380, "initial_mass": 25000, "final_mass": 15000}    # 3-я ступень
]

# Расчет дельта-V для каждой ступени
total_delta_v = 0
for stage in stages:
    delta_v = tsiolkovsky_velocity(stage["isp"], stage["initial_mass"], stage["final_mass"])
    total_delta_v += delta_v
    print(f"Delta-V for stage: {delta_v:.2f} m/s")

print(f"Total Delta-V: {total_delta_v:.2f} m/s")

# Начальные настройки
vessel.control.sas = True
vessel.control.throttle = 0.5

# Взлёт
vessel.control.activate_next_stage()  # Активация двигателей
print("Взлёт!")
time.sleep(2)  # Задержка перед увеличением тяги

# Основной цикл полёта
start_time = time.time()
while True:
    elapsed_time = time.time() - start_time

    altitude = flight.mean_altitude
    speed = flight.speed

    # Расчёт атмосферного давления и силы сопротивления
    pressure = atmospheric_pressure(base_pressure, scale_height, altitude)
    density = pressure / (287.05 * (288.15 - 0.0065 * altitude))  # Уравнение состояния идеального газа
    drag = drag_force(density, speed, drag_coefficient, cross_sectional_area)

    # Расчёт гравитационного ускорения
    gravity = gravitational_acceleration(planet_mass, planet_radius, altitude)

    # Запись данных
    altitude_file.write(f"{elapsed_time:.2f}\t{altitude:.2f}\n")
    speed_file.write(f"{elapsed_time:.2f}\t{speed:.2f}\n")

    # Управление тягой и этапы
    if altitude > 10000 and vessel.control.throttle < 0.8:
        vessel.control.throttle += 0.1  # Постепенное увеличение тяги
    if altitude > 70000:  # Выход из атмосферы
        vessel.control.sas_mode = conn.space_center.SASMode.prograde

    if orbit.apoapsis_altitude > 250000:
        vessel.control.throttle = 0  # Остановка двигателей
        print("Выход на орбиту завершён.")
        break

    time.sleep(0.1)

# Орбитальный этап
print("Орбитальный этап.")
time.sleep(5)

# Завершение записи
altitude_file.close()
speed_file.close()
print("Данные записаны в файлы.")

# Подготовка к посадке (упрощённая симуляция)
vessel.control.throttle = 0.2
vessel.control.sas_mode = conn.space_center.SASMode.retrograde
print("Снижение начато.")

while flight.mean_altitude > 0:
    elapsed_time = time.time() - start_time

    altitude = flight.mean_altitude
    speed = flight.speed

    # Запись данных для посадки
    altitude_file = open('Высота_относительно_планеты.txt', 'a')
    speed_file = open('Скорость_относительно_планеты.txt', 'a')

    altitude_file.write(f"{elapsed_time:.2f}\t{altitude:.2f}\n")
    speed_file.write(f"{elapsed_time:.2f}\t{speed:.2f}\n")

    altitude_file.close()
    speed_file.close()

    if altitude < 5000:
        vessel.control.throttle = 0.1  # Уменьшение тяги перед посадкой
    if altitude < 100:
        vessel.control.throttle = 0  # Полное выключение тяги перед касанием

    time.sleep(0.1)

print("Посадка завершена.")
