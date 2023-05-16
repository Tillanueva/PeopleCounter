   ![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)


# People Counter Tiendas Cortitelas

## Manual de usuario

Este proyecto fue creado con la finalidad de poder llevar un conteo
del tráfico en las Tiendas Cortitelas, el cual guarda un registro 
de la cantidad de personas que ingresan a las tiendas a diario.

En este apartado se describirán las instrucciones de configuración 
del entorno de esta aplicación para su uso y mantenimiento.

### - Base de datos

1. Instalar Backup de PROJECT_PC01
2. Configurar entorno de Microsoft SQL Server Management Studio 
para conexion remota

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

### - Librerías importadas

![libreriasContador](https://github.com/Tillanueva/PeopleCounter/assets/128622581/d06fb6b8-0db0-4c5c-90a2-5978878f5504)

Estas son las librerías utilizadas en el módulo principal de la aplicación.







