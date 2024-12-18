import krpc
import time

# Подключение к KSP через kRPC
conn = krpc.connect(name='Buran')
vessel = conn.space_center.active_vessel

# Открытие файла для записи координат
output_file = open('buran_telemetry.txt', 'w')

# Функция для записи координат
def log_coordinates(t):
    flight_info = vessel.flight()
    latitude = flight_info.latitude
    longitude = flight_info.longitude
    altitude = flight_info.mean_altitude
    output_file.write(f"{t}, {latitude}, {longitude}, {altitude}\n")
    output_file.flush()

# Этап 1: Взлёт
vessel.control.sas = True
vessel.control.throttle = 1.0
vessel.control.activate_next_stage()
print("Взлёт")

start_time = time.time()

# Главный цикл для выхода на орбиту
while True:
    elapsed_time = time.time() - start_time
    # Запись координат
    log_coordinates(elapsed_time)

    # Высота и апогей
    altitude = vessel.flight().mean_altitude
    apoapsis = vessel.orbit.apoapsis_altitude

    # Снижение тяги при приближении к границам подходящей высоты
    if apoapsis >= 250000 and apoapsis < 260000:
        vessel.control.throttle = 0.3
    elif apoapsis >= 260000:  # Остановка тяги при высоте, превышающей 260 км
        vessel.control.throttle = 0
        print("Достигнуты 255-260 км.")
        break
    time.sleep(0.1)

# Этап 2: Круговая орбита
print("Круговая орбита")
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(0, 90)  # Горизонтальный полёт

# Манёвры для контроля высоты
while vessel.orbit.periapsis_altitude < 255000:
    vessel.control.throttle = 0.2
    time.sleep(1)
    vessel.control.throttle = 0
    time.sleep(0.5)

# Этап 3: Два витка вокруг Земли
print("Переход к виткам")
orbital_period = vessel.orbit.period

for orbit in range(2):  # Два витка
    print(f"Сделано {orbit + 1}...")
    start_orbit_time = time.time()
    while time.time() - start_orbit_time < orbital_period:
        apoapsis = vessel.orbit.apoapsis_altitude
        periapsis = vessel.orbit.periapsis_altitude

        # Проверка, чтобы не покинуть орбиту
        if apoapsis > 260000 or periapsis < 255000:
            vessel.control.throttle = 0.1
            vessel.auto_pilot.target_pitch_and_heading(0, 90)  # Корректировка орбиты
        else:
            vessel.control.throttle = 0

        time.sleep(1)

# Завершение миссии
output_file.close()
print("Посадка")




