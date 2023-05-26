import pyodbc
import os


class conex:
    connec = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-O6UFVI0;DATABASE=PROJECT_PC01;UID=Project01;PWD'
                            '=PProject01')

    consulta = "INSERT INTO conteo(fecha, entradas) VALUES (?, ?);"

