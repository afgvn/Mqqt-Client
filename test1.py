import numpy as np


print("Hello World")
print("Hello World2")
print("Hello World3")
print("Hello World4")

import time
tiempo_segundos = time.time()
print(tiempo_segundos)

tiempo_cadena = time.ctime(tiempo_segundos) # 1488651001.7188754 seg
print(tiempo_cadena)

fruits = ["apple", "banana", "cherry"]
for x in fruits:
 print(x)
 print(x * 2 )