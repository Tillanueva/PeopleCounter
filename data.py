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