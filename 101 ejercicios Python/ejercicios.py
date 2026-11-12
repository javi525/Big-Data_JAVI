# ==========================================
# NIVEL 1: BLOQUE BÁSICO
# ==========================================

print("=" * 80)
print(" NIVEL 1: BLOQUE BÁSICO - EJERCICIOS RESUELTOS")
print("=" * 80)

# 1.
print("\n[Ejercicio 1] Escribir un programa que guarde tu nombre en una variable e imprima un saludo personalizado.")
nombre = "Carlos"
print(f"-> Solución: Hola, {nombre}! Bienvenido a Python.")

# 2.
print("\n[Ejercicio 2] Declarar dos variables numéricas, sumarlas y mostrar el resultado por pantalla.")
a, b = 10, 15
print(f"-> Solución: La suma de {a} y {b} es: {a + b}")

# 3.
print("\n[Ejercicio 3] Crear una variable con el precio de un producto y otra con el IVA (21%). Calcular y mostrar el precio total.")
precio_producto = 100.0
iva = 0.21
precio_total = precio_producto * (1 + iva)
print(f"-> Solución: Precio base: {precio_producto} | IVA: {iva*100}% | Precio total: {precio_total}")

# 4.
print("\n[Ejercicio 4] Solicitar al usuario su año de nacimiento y calcular su edad actual.")
anho_nacimiento = 2000
edad_actual = 2026 - anho_nacimiento
print(f"-> Solución: Año de nacimiento: {anho_nacimiento} | Edad actual calculada: {edad_actual} años")

# 5.
print("\n[Ejercicio 5] Pedir un número al usuario y determinar si es positivo, negativo o cero utilizando un condicional simple.")
numero = 5
if numero > 0:
    res_cond = "El número es positivo."
elif numero < 0:
    res_cond = "El número es negativo."
else:
    res_cond = "El número es cero."
print(f"-> Solución para el número {numero}: {res_cond}")

# 6.
print("\n[Ejercicio 6] Escribir un programa que pida un número entero y determine si es par o impar.")
n = 8
par_impar = "par" if n % 2 == 0 else "impar"
print(f"-> Solución: El número {n} es {par_impar}.")

# 7.
print("\n[Ejercicio 7] Solicitar dos números al usuario y mostrar cuál de los dos es el mayor.")
num1, num2 = 42, 19
mayor = num1 if num1 > num2 else num2
print(f"-> Solución: Entre {num1} y {num2}, el mayor es: {mayor}")

# 8.
print("\n[Ejercicio 8] Declarar una variable booleana que indique si un usuario está logueado y mostrar un mensaje acorde.")
logueado = True
msg = "Acceso concedido. ¡Bienvenido de nuevo!" if logueado else "Por favor, inicie sesión."
print(f"-> Solución: Estado logueado={logueado} -> {msg}")

# 9.
print("\n[Ejercicio 9] Utilizar un bucle para imprimir los números del 1 al 10 en orden ascendente.")
print("-> Solución: ", end="")
for i in range(1, 11):
    print(i, end=" ")
print()

# 10.
print("\n[Ejercicio 10] Utilizar un bucle para imprimir los números del 10 al 1 en orden descendente.")
print("-> Solución: ", end="")
for i in range(10, 0, -1):
    print(i, end=" ")
print()

# 11.
print("\n[Ejercicio 11] Calcular la suma de todos los números enteros del 1 al 50 utilizando un bucle.")
suma_50 = sum(range(1, 51))
print(f"-> Solución: La suma del 1 al 50 es: {suma_50}")

# 12.
print("\n[Ejercicio 12] Mostrar la tabla de multiplicar del número 5 utilizando un bucle del 1 al 10.")
print("-> Solución:")
for i in range(1, 11):
    print(f"   5 x {i} = {5 * i}")

# 13.
print("\n[Ejercicio 13] Pedir una palabra al usuario y mostrarla por pantalla 5 veces consecutivas usando un ciclo.")
palabra = "Python"
print(f"-> Solución (palabra: '{palabra}'):")
for _ in range(5):
    print(f"   {palabra}")

# 14.
print("\n[Ejercicio 14] Crear un programa que pida el radio de un círculo y calcule su área.")
import math
radio = 4.0
area = math.pi * (radio ** 2)
print(f"-> Solución: Para un radio de {radio}, el área es: {area:.2f}")

# 15.
print("\n[Ejercicio 15] Solicitar tres notas al usuario, calcular el promedio e indicar si está aprobado (nota >= 5).")
n1, n2, n3 = 6.0, 4.5, 7.0
promedio = (n1 + n2 + n3) / 3
estado = "Aprobado" if promedio >= 5 else "Reprobado"
print(f"-> Solución: Notas ({n1}, {n2}, {n3}) -> Promedio: {promedio:.2f} ({estado})")

# 16.
print("\n[Ejercicio 16] Imprimir todos los números pares que se encuentren entre el 1 y el 30.")
pares = [i for i in range(1, 31) if i % 2 == 0]
print(f"-> Solución: {pares}")

# 17.
print("\n[Ejercicio 17] Pedir al usuario una temperatura en grados Celsius y convertirla a Fahrenheit.")
celsius = 25.0
fahrenheit = (celsius * 9/5) + 32
print(f"-> Solución: {celsius}°C equivalen a {fahrenheit}°F")

# 18.
print("\n[Ejercicio 18] Crear un programa que convierta una cantidad de minutos introducida por el usuario a horas y minutos.")
total_minutos = 135
horas = total_minutos // 60
minutos_restantes = total_minutos % 60
print(f"-> Solución: {total_minutos} minutos son {horas} hora(s) y {minutos_restantes} minuto(s).")

# 19.
print("\n[Ejercicio 19] Solicitar al usuario un precio base y aplicar un descuento del 15% si el precio es mayor a 50.")
precio_base = 65.0
precio_final = precio_base * 0.85 if precio_base > 50 else precio_base
print(f"-> Solución: Precio base de {precio_base} -> Precio final con descuento: {precio_final}")

# 20.
print("\n[Ejercicio 20] Escribir un programa que cuente cuántas letras tiene una palabra introducida por el usuario.")
palabra_20 = "programacion"
print(f"-> Solución: La palabra '{palabra_20}' tiene {len(palabra_20)} letras.")

# 21.
print("\n[Ejercicio 21] Imprimir los múltiplos de 3 del rango del 1 al 30.")
multiplos_3 = [i for i in range(1, 31) if i % 3 == 0]
print(f"-> Solución: {multiplos_3}")

# 22.
print("\n[Ejercicio 22] Pedir al usuario dos palabras y comprobar si son idénticas utilizando un condicional.")
p1, p2 = "casa", "casa"
iguales = "Las palabras son idénticas." if p1 == p2 else "Las palabras son diferentes."
print(f"-> Solución: Palabras '{p1}' y '{p2}' -> {iguales}")

# 23.
print("\n[Ejercicio 23] Multiplicar todos los números del 1 al 5 (calcular el factorial de 5 de forma manual con bucle).")
factorial = 1
for i in range(1, 6):
    factorial *= i
print(f"-> Solución: El factorial de 5 es: {factorial}")

# 24.
print("\n[Ejercicio 24] Pedir al usuario un número y mostrar un mensaje si se encuentra en el rango de 10 a 20.")
num_eval = 15
en_rango = "está en el rango [10, 20]." if 10 <= num_eval <= 20 else "está fuera del rango."
print(f"-> Solución: El número {num_eval} {en_rango}")

# 25.
print("\n[Ejercicio 25] Crear una variable que almacene una contraseña fija y pedir al usuario que intente adivinarla una vez.")
pass_fija = "secreto123"
intento = "secreto123"
res_pass = "¡Contraseña correcta!" if intento == pass_fija else "Contraseña incorrecta."
print(f"-> Solución (Intento: '{intento}'): {res_pass}")

print("\n" + "=" * 80)
print(" FIN DEL NIVEL 1")
print("=" * 80)