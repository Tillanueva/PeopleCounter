import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data import traficoMensual, traficoDia, traficoAnual


class dashboard:
    plt.rcParams["axes.prop_cycle"] = plt.cycler(
        color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

    # Chart 1: Bar chart of sales data
    fig1, ax1 = plt.subplots()
    ax1.bar(traficoDia.keys(), traficoDia.values())
    ax1.set_title("Tráfico los últimos 5 días")
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Tráfico")
    ax1.invert_xaxis()
    # plt.show()

    # Chart 2: Horizontal bar chart of inventory data
    fig2, ax2 = plt.subplots()
    ax2.bar(traficoMensual.keys(), traficoMensual.values())
    ax2.set_title("Tráfico los últimos 5 meses")
    ax2.set_xlabel("Mes")
    ax2.set_ylabel("Tráfico")

    root = tk.Tk()
    root.title("Dashboard")
    root.state('zoomed')

    side_frame = tk.Frame(root, bg="#4C2A85")
    side_frame.pack(side="left", fill="y")

    label = tk.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
    label.pack(pady=50, padx=20)

    charts_frame = tk.Frame(root)
    charts_frame.pack()

    upper_frame = tk.Frame(charts_frame)
    upper_frame.pack(fill="both", expand=True)

    canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

    lower_frame = tk.Frame(charts_frame)
    lower_frame.pack(fill="both", expand=True)

    root.mainloop()
