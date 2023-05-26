import cv2
import math
import cvzone
import tkinter as tk
import matplotlib.pyplot as plt
from ultralytics import YOLO
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from sort import *
from datetime import *
from conexion import conex
from dashboard import dashboard

# CONEXION BASE DE DATOS
conn = conex.connec
cursor = conn.cursor()


# Colores
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

# inicializar el Modelo de YOLOY
model = YOLO("Yolo-Weights/yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Variables de conteo
conteo = []
global count
# Coordenadas límites verticales para poder contar a la persona
limitsUp = [0, 300, 1280, 300]  # Entrada
# variable de seguimiento de objetos
trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)


def visualizar():
    if cap is not None:

        fecha = times()
        # CONSULTA A LA BASE DE DATOS

        ret, frame = cap.read()

        if ret:

            if rgb == 1 and hsv == 0 and gray == 0:
                # Color BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Color HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif rgb == 0 and hsv == 0 and gray == 1:
                # Color GRAY
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # captura el modelo del frame que capturó la cámara web y la lee en tiempo real
            results = model(frame, stream=True)

            detections = np.empty((0, 5))

            for r in results:

                # Dibujar recuadro del objeto
                boxes = r.boxes

                for box in boxes:

                    # parametros del recuadro
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    # la variable cls captura los distintos objetos que se encuentran alrededor
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])

                    # Si el objeto es una persona, dibuja un recuadro alrededor
                    if classNames[cls] == "person" and conf > 0.3:
                        # cornerRect dibuja el cuadro con los parámetros anteriores
                        cvzone.cornerRect(frame, (x1, y1, w, h))

                        # Coloca el nombre del objeto (persona)
                        cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1,
                                           thickness=1)

                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))
            # Actualiza en tiempo real lo que captura el video
            resultsTracker = trackers.update(detections)

            for results in resultsTracker:
                # Parametros para el contador
                x1, y1, x2, y2, id1 = results
                x1, y1, x2, y2 = int(x1), int(x1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1
                # Ecuación de definición de punto medio
                cx, cy = x1 + w // 2, y1 + h // 2

                # Dibuja un punto medio en el recuadro de la persona
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # si la persona pasa la linea límite se suma al contador de personas que entran
                if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
                    if conteo.count(id1) == 0:
                        conteo.append(id1)
                        try:
                            with cursor:
                                cursor.execute(conex.consulta, (fecha, 1))
                                print("Almacenado")
                                mostrarDia()
                                mostrarMes()
                        except Exception as e:
                            print("Ocurrió un error al insertar: ", e)

                        cv2.line(frame, (limitsUp[3], limitsUp[2]), (limitsUp[1], limitsUp[0]), (0, 255, 0), 5)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo = Label(pantalla)
            lblVideo.place(x=10, y=95)

            # Mostramos en el GUI
            lblVideo.config(image=img)
            lblVideo.image = img
            lblVideo.after(5, visualizar)

            # Muestra en conteo de personas en la ventana
            global count
            count = str(len(conteo))
            lblConteo = Label(pantalla, text="Ingreso de personas hoy: " + count)
            lblConteo.config(font="Sans-serif")
            lblConteo.place(x=1000, y=20)

        else:

            cap.release()


def Mostrardashboard():
    dashboard()


def times():
    fechaC = datetime.today()  # Capruta date actual
    current_date = fechaC.strftime("%Y-%m-%d")
    lblFecha.config(text=current_date, font="Sans-serif")
    return current_date


def mostrarDia():
    # Ejecuta procedimiento almacenado a partir de cadena de conexión
    cursor.execute(" exec ConeoDiarioDesc")
    records = cursor.fetchall()
    # lee todos los datos de la tabla
    global count
    count = 0
    # Elimina todos los datos del tree
    for record in tree.get_children():
        tree.delete(record)
    # Una vez que el tree está vacío llena la tabla con el procedimiento almacenado
    for record in records:
        if count == 0:
            tree.insert('', 'end', values=(record[0], record[1]), tags=('evenrow',))
        else:
            tree.insert('', 'end', values=(record[0], record[1]), tags=('oddrow',))


def mostrarMes():
    # Ejecuta procedimiento almacenado a partir de cadena de conexión
    cursor.execute("exec ConteoMesDesc")
    # lee todos los datos de la tabla
    records = cursor.fetchall()
    # Contador para ver la cantidad de datos en el tree
    global count
    count = 0
    # Elimina todos los datos del tree
    for record in tree1.get_children():
        tree1.delete(record)
    # Una vez que el tree está vacío llena la tabla con el procedimiento almacenado
    for record in records:
        if count == 0:
            tree1.insert('', 'end', values=(record[0], record[1]), tags=('evenrow',))
        else:
            tree1.insert('', 'end', values=(record[0], record[1]), tags=('oddrow',))


# VARIABLES
cap = None
rgb = 1
hsv = 0
gray = 0

# INTERFAZ
pantalla = Tk()
pantalla.title("Tiendas Cortitelas | People Counter")
pantalla.state('zoomed')  # Dimensión de la ventana

icon = PhotoImage(file="icon.png")

lblFecha = Label(pantalla)
lblFecha.place(x=10, y=20)
times()  # Función captura fecha actual

btnDashboard = Button(pantalla, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25, command=Mostrardashboard)
btnDashboard.pack(pady=5, padx=0)
btnDashboard.config(width=20, height=2)
btnDashboard.place(x=1135, y=95)

# Muestra la tabla de tráfico por día
tree = ttk.Treeview(pantalla, columns=('0', '1'), show="headings", height=10, )
tree.grid(row=4, column=0, columnspan=2)
tree.column('0', anchor=CENTER)
tree.column('1', anchor=CENTER)
tree.heading('0', text='Fecha', anchor=CENTER)
tree.heading('1', text='Total Personas', anchor=CENTER)
tree.place(x=710, y=95)

# Muestra la tabla de tráfico por mes
tree1 = ttk.Treeview(pantalla, height=10, columns=('0', '1'), show="headings")
tree1.grid(row=4, column=0, columnspan=2)
tree1.column('0', anchor=CENTER)
tree1.column('1', anchor=CENTER)
tree1.heading('0', text='Mes', anchor=CENTER)
tree1.heading('1', text='Total Personas', anchor=CENTER)
tree1.place(x=710, y=345)
# Video

#Inicio cámara
cap = cv2.VideoCapture(0)
cap.set(1, 1700)
cap.set(4, 520)

visualizar()
mostrarMes()
mostrarDia()

pantalla.iconphoto(True, icon)
pantalla.mainloop()
