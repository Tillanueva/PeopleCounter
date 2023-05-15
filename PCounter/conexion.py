import pyodbc
import os


class conex:
    connec = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.4.56;DATABASE=PROJECT_PC01')

    consulta = "INSERT INTO conteo(fecha, entradas) VALUES (?, ?);"


