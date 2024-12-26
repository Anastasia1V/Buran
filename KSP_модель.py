import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv("buran.csv", delimiter=',', encoding='utf-8')


data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Speed'] = pd.to_numeric(data['Speed'], errors='coerce')


data = data.dropna(subset=['Time', 'Speed'])


plt.figure(figsize=(7, 6))


plt.subplot(1, 1, 1)
plt.plot(data['Time'], data['Speed'], label='Скорость относительно поверхности', linewidth=2)
plt.title("Зависимость скорости от времени, KSP")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/c)")
plt.grid(True)
plt.legend()


plt.tight_layout()
plt.show()
