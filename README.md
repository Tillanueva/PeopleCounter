   ![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)


# People Counter Tiendas Cortitelas

## Manual de usuario

Este proyecto fue creado con la finalidad de poder llevar un conteo
del tráfico en las Tiendas Cortitelas, el cual guarda un registro 
de la cantidad de personas que ingresan a las tiendas a diario.

En este apartado se describirán las instrucciones de configuración 
del entorno de esta aplicación para su uso y mantenimiento.

### - Base de datos
1. Configurar entorno de Microsoft SQL Server Management Studio 
para conexion remota.
2. Asegurese de estar conectado en red y tener acceso a la base de 
datos de manera remota.


### - Ejecutable
1. Buscar en la carpeta "bulid" el archivo ejecutable llamado ContadorCT
2. Dae doble click para iniciar.


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


