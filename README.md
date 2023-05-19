   ![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)


# People Counter Tiendas Cortitelas

## Manual de usuario

Este proyecto fue creado con la finalidad de poder llevar un conteo
del tráfico en las Tiendas Cortitelas, el cual guarda un registro 
de la cantidad de personas que ingresan a las tiendas a diario.

En este apartado se describirán las instrucciones de configuración 
del entorno de esta aplicación para su uso y mantenimiento.

### - Conexion a Base de datos
1. Configurar entorno de Microsoft SQL Server Management Studio 
para conexion remota.
2. Asegurese de estar conectado en red y tener acceso a la base de 
datos de manera remota.


### - Ejecutable
El archivo ejecutable se encuentra en el directorio PCounter/build - copia/exe.win-amd64-3.10.
El nombre del archivo es ContadorCTPv2.exe, para ejecutarlo unicamente dar
doble clic y esperar a que cargue la interfaz.

La interfaz de People Counter es sencilla ya que unicamente debe iniciar  
la aplicación y esta empezará a realizar un conteo al mismo tiempo que este 
muestra una tabla y una grafica con los datos almacenados en tiempo real

********
## Manual Técnico
### - Base de datos y conexión
La base de datos consta de una única tabla en donde se almacena el conteo 
de tráfico de las tiendas, la cual cuenta con campos de fecha y entrada.

la lógica de la base es que va a ingresar el valor de 1 por cada entrada 
que exista, es decir, que cada vez que una persona ingrese, se insertará 
a la tabla la fecha de ingreso y en entradas un 1. Esto para poder actualizar
en tiempo real las gráficas.

para visualizar los datos se utilizan procedimientos almacenados los cuales
suman la cantidad de veces que se ingresó un registro con la misma fecha, con el
mismo mes o con el mismo año.


### - Librerías utilizadas

![requirements](https://github.com/Tillanueva/PeopleCounter/assets/128622581/1f0c3d51-2f8a-495d-8271-74a1c9b7e4b2)

En el archivo requirementes.txt se encuentran enumeradas las linbrerías que 
son necesarias para que la aplicación pueda ser ejecutada de manera correcta. 
De esta forma todas las librerías se instalarán automáticamente de manera 
instantánea. Aulgunas de estas librerías no se importan directamente en el códio de 
la aplicación sino que se ejecutan en segundo plano.

### - Código
#### - Librerías 

![libreriasContador](https://github.com/Tillanueva/PeopleCounter/assets/128622581/5b3740ef-24f7-48aa-8ca2-a47a4b460eea)

Estas son las librerías utilizadas en el módulo principal de la aplicación. Muchas 
de ellas se instalaron previamente en los requerimientos para poder 
ser importadas, otras se instalan automáticamente cuando se instala python
como datetime, PIL, math o tkinter.

#### - Conexión a Base de Datos

![llamadaConex](https://github.com/Tillanueva/PeopleCounter/assets/128622581/f6f69dcc-76d0-4949-a149-915f0be01355)

En esta linea se llama a la cadena de conexión ubicada en el 
archivo conexion.py. Se crea la variable de conn y se le da 
el valor de la linea de conexión. A la variable cursor se le
asigna el método cursor() para poder comunicarse con la base 
de datos.

#### - Modelo YOLO
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

Ultralytics es una librería de una red neuronal la cual se puede 
entrenar por medio del modelo YOLO, a este se le envían distintos
objetos y este los reconoce. Para poder entrenar el modelo de YOLO, se 
estableció una lista con distintos nombres de objetos, entre ellos
persona.

#### - Variables de conteo

    # Variables de conteo
    conteo = []
    global count
    # Coordenadas límites verticales para poder contar a la persona
    limitsUp = [0, 300, 1280, 300]  # Entrada
    # variable de seguimiento de objetos
    trackers = Sort(max_age=20, min_hits=3, iou_threshold=0.3)


Aquí se inicializan las variables de lectura y conteo. se crea
la lista conteo la cual se utiliza para contabilizar el reconocimiento
de objetos. limitsUp es una lista que contiene cordenadas en 
forma vertical. Por último , trackers es una variable a la cual
se le asigna el método Sort() el cual re organiza la lista de conteo.


#### - Función Visualizar

    def visualizar():
        if cap is not None:
    
            fecha = times()
            # CONSULTA A LA BASE DE DATOS
    
            ret, frame = cap.read()



La función visualizar es la que contiene la mayor parte de la funcionalidad 
de la aplicación, ya que aquí se gestiona la funcionalidad de la cámara 
y el reconocimiento de objetos en tiempo real para poder llevar el conteo.

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

Dentro de la funcuón se define la variable results que es la encargada 
de que el modelo yolo pueda leer lo que captura la cámara en tiempo real 
al igual que se declara la variable detection la cual Crea y devuelve
una referencia a un array vacío con las dimensiones especificadas en 
la tupla dimensiones. Posteriormente se crea un for anidado en el cual
se especifican los parametros para poder enmarcar los objetos que reconoce
yolo.

#### Si el objeto es una persona, dibuja un recuadro alrededor
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

Se crea la condición que indica si lo que lee el modelo yolo mediante 
la variable cls es una persona, si la condición se cumple, dibuja un 
recuadro al rededor de la persona. Posteriormente se actualiza el tracker con lo que acaba de 
detectar el modelo.

     for results in resultsTracker:
        # Parametros para el punto medio
        x1, y1, x2, y2, id1 = results
        x1, y1, x2, y2 = int(x1), int(x1), int(x2), int(y2)

        w, h = x2 - x1, y2 - y1
        # Ecuación de definición de punto medio
        cx, cy = x1 + w // 2, y1 + h // 2
    
        # Dibuja un punto medio en el recuadro de la persona
        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    
Con los resultados capturados anteriormente, dentro de un for se
especifican parametros para dibujar un punto medio dentro del
recuadro. Este punto medio aydará a contabilizar las personas.


 #### si la persona pasa la linea límite se suma al contador de personas que entran
                if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
                    if conteo.count(id1) == 0:
                        conteo.append(id1)
                        try:
                            with cursor:
                                cursor.execute(consulta, (fecha, 1))
                                print("Almacenado")
                                mostrarDia()
                                mostrarMes()
                        except Exception as e:
                            print("Ocurrió un error al insertar: ", e)

                        cv2.line(frame, (limitsUp[3], limitsUp[2]), (limitsUp[1], limitsUp[0]), (0, 255, 0), 5)

Con esta condición se establece que si el pinto medio que se acaba
de dibujar dentro del recuadro, cruza la linea límite que se definió
al inicio, el contador va a aumentar. Posteriormente dentro de un try except
con el método cursor que definimos anteriormente se ingresa el conteo 
a la base de datos. Las funciones que se invocan en el fragmento de código
(mostrarDia(), mostrarMes) ejecuta vistas de la base de datos y las muestra
en tablas.


    def Mostrardashboard():
        dashboard()
    
    
    def times():
        fechaC = datetime.today()  # Capruta date actual
        current_date = fechaC.strftime("%Y-%m-%d")
        lblFecha.config(text=current_date, font="Sans-serif")
        return current_date

La funcion Mostrardashboard unicamente invoca la función dashboard() 
definida en el archivo dashbard.py. Por otro lado times() captura la fecha
actual y la muestra en un label.


#### - Función mostrarMes y mostrarDia
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
    

Estas dos funciones son similares y se encargan de rellenar las tablas
para poder mostrar los datos de la base de datos.

#### - Interfaz de usuario

    pantalla = Tk()
    pantalla.title("Tiendas Cortitelas | People Counter")
    pantalla.state('zoomed')  # Dimensión de la ventana
    
    icon = PhotoImage(file="icon.png")
    
    texto1 = Label(pantalla, text="Video en tiempo real: ")
    texto1.config(font="Sans-serif")
    texto1.place(x=400, y=20)
    
    lblFecha = Label(pantalla)
    lblFecha.place(x=10, y=20)
    times()  # Función captura fecha actual

En este fragmento es donde se crea la interfaz en la que se llamarán las 
distintas funciones. Es aquí donde se creará la ventana que visualizará
el usuario y se colocarán los elementos visuales de la aplicación, como los
labels que muestran los títulos y la fecha. También es en esta parte donde 
define el ícono de la aplicación y las dimensiones de la misma.

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
    
Estos son igualmente los elementos que se mostrarán en la ventana, que son un botón
que llama la función de mostrarDashboard, una tabla para mostrar el tráfico por
día y la otra para mostrar el trafico por mes.

    cap = cv2.VideoCapture(0)
    cap.set(1, 1700)
    cap.set(4, 520)
    
    visualizar()
    mostrarMes()
    mostrarDia()
    
    pantalla.iconphoto(True, icon)
    pantalla.mainloop()

Finalmente, se crea la variable cap, esta variable es muy importante ya que es
la que se encarga de encender la cámara y capturarla, tambíen se le envían las respectivas
dimensiones. También se invoca la función visualizar para que se muestre en la interfaz, 
igualmente se invocan las funciones que actualizan las tablas que se definieron 
anteriormente. Al final se invoca el método mainloop, este método siempre debe ir
al final del código ya que es la que hará que la ventana no se cierre hasta que el
usuario no la cierre.

### DATA

    import os
    import pyodbc
    from conexion import conex
    
    # CONEXION BASE DE DATOS
    conn = conex.connec
    cursor = conn.cursor()
    
    cursor.execute(" exec TraficoDiario5")
    fecha = [i for i in cursor.fetchall()]
    traficoDia = dict((i[0],i[1])for i in fecha)
    
    cursor.execute(" exec ConteoMesDesc")
    Mes = [i for i in cursor.fetchall()]
    traficoMensual = dict((i[0],i[1])for i in Mes)
    
    cursor.execute("exec conteoAnual")
    year = [i for i in cursor.fetchall()]
    traficoAnual = dict((i[0],i[1])for i in year)

Este módulo tiene la función de extraer la data de la base para posteriormente
colocarla en diccionarios, los diccionarios contienen información del tráfico
por día, por més y por año, de esta forma será más fácil poder colocar los 
datos en el dashboard para que este pueda mostrar gráficas por medio de la 
librería matplotlib.


### DASHBOARD
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    from data import traficoMensual, traficoDia, traficoAnual

Para el dashboard se necesitaron las librerías de tkinter, matplotlib
y se importaron los diccionarios definidos anteriormente para poder
mostrar los datos en el dashboard.

    def dashboard():
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
    

El dashboard se encuentra contenido en una función con el mismo nombre
para poder invocarla en el módulo principal. Dentro de la función
se define la información que contenerá la gráfica, y traerá los datos
de los diccionarios han sido definidos anteriormente. 

        root = tk.Tk()
        root.title("Dashboard")
        root.state('zoomed')
    
        side_frame = tk.Frame(root, bg="#4C2A85")
        side_frame.pack(side="left", fill="y")
    
        label = tk.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
        label.pack(pady=5, padx=0)
        label.config(width=20, height=2)
    
        charts_frame = tk.Frame(root)
        charts_frame.pack()
    
        upper_frame = tk.Frame(charts_frame)
        upper_frame.pack(fill="both", expand=True)

En este fragmento de código se inicializa la ventana del dashboard
y se crean distintos frames para poder darle un mejor diseño a la
interfaz.

    canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

    lower_frame = tk.Frame(charts_frame)
    lower_frame.pack(fill="both", expand=True)

    root.mainloop()

Finalmente se muestran los gráficos  con el método FigureCanvasTkAgg
y se les posiciona en alguno de los frames de la ventana dashboard y se
asigna el método mainloop a la ventana.



