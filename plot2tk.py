import serial
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from itertools import count
import time

x_value, humidity, temperature, moisture, light = [], [], [], [], []
index = count()

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)


def data_points():
    # 範圍最大值
    LIMIT = 20

    global x_value, humidity, temperature, moisture, light
    while True:
        response = str(ser.readline().decode())
        if response.startswith("hum:"):
            hum = response[5:7]
            tem = response[15:19]
            moi = response[-15:-11]
            lig = response[-5:-2].strip("/n")
            # 這邊沒看到需要移除字符是甚麼 需要自行補上

            templateData = {"tem": tem, "hum": hum, "moi": moi, "lig": lig}
            print(f"Humidity:{hum}% Temperature:{tem} Moisture:{moi} Light:{lig}")

            x_value.append(next(index))
            humidity.append(hum)
            temperature.append(tem)
            moisture.append(moi)
            light.append(lig)

        # 截取更新範圍
        if len(x_value) > LIMIT:
            x_value = x_value[-LIMIT:]
            humidity = humidity[-LIMIT:]
            temperature = temperature[-LIMIT:]
            moisture = moisture[-LIMIT:]
            light = light[-LIMIT:]


def app():
    root = Tk()
    root.title("Plantes Surveillance System")
    root.config(background="white")
    root.geometry("1280x720")

    fig = Figure()
    fig.suptitle("Plantes Surveillance Chart")
    axes = fig.subplots(2, 2)
    ax1, ax2 = axes[0]
    ax3, ax4 = axes[1]

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def plotter():
        while True:
            ax1.cla()
            ax1.set_title("Humidity")
            ax1.axes.xaxis.set_visible(False)
            ax2.cla()
            ax2.set_title("Temperature")
            ax2.axes.xaxis.set_visible(False)
            ax3.cla()
            ax3.set_title("Moisture")
            ax3.axes.xaxis.set_visible(False)
            ax4.cla()
            ax4.set_title("Light")
            ax4.axes.xaxis.set_visible(False)

            ax1.plot(x_value, humidity, marker='o', color='orange')
            ax2.plot(x_value, temperature, marker='o', color='orange')
            ax3.plot(x_value, moisture, marker='o', color='orange')
            ax4.plot(x_value, light, marker='o', color='orange')

            graph.draw()
            # 更新畫面時間間隔 有需要可以改成隨data_points更新
            time.sleep(0.5)

    threading.Thread(target=plotter).start()
    root.mainloop()


if __name__ == '__main__':
    threading.Thread(target=data_points).start()
    app()
