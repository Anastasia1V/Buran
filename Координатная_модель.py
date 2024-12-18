import matplotlib.pyplot as plt


# Функция для чтения данных из файла
def read_data(file_path):
    time = []
    height = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                data = line.split(',')
                try:
                    time.append(float(data[0]))
                    height.append(float(data[3]))
                except ValueError:
                    continue

    return time, height


# Путь к файлу с данными
file_path = 'buran_telemetry.txt'

# Чтение данных из файла
time, height = read_data(file_path)

# Построение графика
plt.plot(time, height, marker='o', color='b', label='Высота полёта')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.title('График зависимости высоты полёта от времени полёта')
plt.legend()
plt.grid(True)
plt.show()
