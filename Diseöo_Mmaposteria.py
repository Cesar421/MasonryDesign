# SEFI Software
# Programmierung: Cesar Fernando Gamba Tiusaba
# Version 1.0 - 01.01.2021
# Man kann die Mauern des Mauerwerks design, braucht man nur 2 CSV file.
# Diese CSV  heißen 'Datos muros(Diseöo_Mmaposteria.py).csv' und
# 'Propiedades (Diseöo_Mmaposteria.py).csv',
# dort kann man die ganzen Angaben, um die Mauern zu Design finden

import numpy as num
import pandas as pd

# Se debe ubicar estos CSV en la carpeta del programa (por el momento), hasta
# que se desarrolle una GUI para SEFI
df = pd.read_csv('Datos muros(prueb.py).csv')
df1 = pd.read_csv('Propiedades (prueb.py).csv')

# Se debe cambiar el porcentaje de celdas rellenas para cada piso,
# la convención para rellenar estos valores es la siguiente: 1 = 100% y 0 = 0%
# El valor final de celdas llenas, no son necesariamente las que se
# colocan en las matriz, ya que el numero de celdas es un entero (int) y
# los porcentajes son float el programa ajusta a un numero par entero de celdas.
porcentaje_Celdas_Rellenas = [0.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

# Esta es la matriz maestra, en la cual se almacena todos los cálculos iniciales
# (cambiar el numero de columnas si se necesitan).
a = num.zeros([len(df), 100])

# Aca se calcula el número de ladrillos por muro, generalmente solo existen dos
# tipos de unidades de mampostería, bloque completo y bloque medio, ademas se
# determina el espesor del mortero de pega, necesario para ajustarse
# a la distancia del muro
for i in range(0, len(df)):

    # Estos contadores se reinician para cada muro, el uso de estos contadores
    # es adicionar bloques de  mampostería de la siguiente manera
    # 1) primero se adiciona unidades completas de los bloques
    # 2) Luego unidades bloques medios
    # 3) por ultimo se ajusta el espesor de pañete para llegar a ajustar
    # las unidades y el mortero a la longitud requerida
    # El error que se puede tener por muro es de un 0.01 (m),
    # como se ve en la linea de código 40, con el while
    diferencia_total: float = 1.0
    contador_NumeroDeBloquesCompletos: int = 0
    contador_NumeroDeBloquesMedios: int = 0
    contador_EspesorMorteroDePega: float = 0.

    a[i, 0] = df.loc[i, 'Numero Muro']
    a[i, 1] = df.loc[i, 'Longitud muro (m)']

    while diferencia_total > 0.001:

        if diferencia_total > df1.loc[6, 'Valores'] / 100 + df1.loc[4, 'Valores'] / 100:
            contador_NumeroDeBloquesCompletos = 1 + contador_NumeroDeBloquesCompletos
            diferencia_total = df.loc[i, 'Longitud muro (m)'] - (df1.loc[
                                      4, 'Valores'] / 100 + df1.loc[
                                      12, 'Valores'] / 100) * contador_NumeroDeBloquesCompletos

            # Numero de bloques completos
            a[i, 2] = contador_NumeroDeBloquesCompletos
            # Espesor mortero de pega
            a[i, 4] = contador_EspesorMorteroDePega + df1.loc[12, 'Valores'] / 100

        elif diferencia_total > df1.loc[6, 'Valores'] / 100:
            contador_NumeroDeBloquesMedios = 1 + contador_NumeroDeBloquesMedios
            diferencia_total = df.loc[i, 'Longitud muro (m)'] - ((df1.loc[
                                       4, 'Valores'] / 100 + df1.loc[
                                       12, 'Valores'] / 100) *
                                       contador_NumeroDeBloquesCompletos) - (
                                       df1.loc[6, 'Valores'] /
                                       100 + df1.loc[
                                       12, 'Valores'] / 100) * contador_NumeroDeBloquesMedios

            # Numero de bloques medios
            a[i, 3] = contador_NumeroDeBloquesMedios
            # Espesor mortero de pega
            a[i, 4] = contador_EspesorMorteroDePega + df1.loc[12, 'Valores'] / 100

        elif diferencia_total < df1.loc[6, 'Valores'] / 100:
            diferencia_total = df.loc[i, 'Longitud muro (m)'] - ((df1.loc[
                                            4, 'Valores'] / 100 + df1.loc[
                                            12, 'Valores'] / 100 + contador_EspesorMorteroDePega) *
                                            contador_NumeroDeBloquesCompletos) - (
                                           df1.loc[6, 'Valores'] / 100 + df1.loc[
                                               12, 'Valores'] / 100 + contador_EspesorMorteroDePega) * \
                               contador_NumeroDeBloquesMedios
            contador_EspesorMorteroDePega = contador_EspesorMorteroDePega + 0.0001

            # Espesor mortero de pega por muro
            a[i, 4] = contador_EspesorMorteroDePega + df1.loc[12, 'Valores'] / 100

    # Numero de celdas por muro
    a[i, 5] = a[i, 2] * df1.loc[18, 'Valores'] + a[i, 3] * df1.loc[19, 'Valores']

    # Aca se hace esto con el mortero de pega para dejar el mortero solamente al interior del muro
    a[i, 4] = a[i, 4]*(a[i, 2]+a[i, 3])/(a[i, 2]+a[i, 3]-1)

# Aca se determina el numero de celdas rellenas, siempre se deja un numero
# par de celdas y se debe suministrar el porcentaje de celdas por cada piso,
# esto se hace en la linea de código 14 con la variable porcentaje_Celdas_
# Rellenas
for i in range(0, len(df)):

    for j in range(0, len(porcentaje_Celdas_Rellenas)):
        a[i, j + 6] = a[i, 5] * porcentaje_Celdas_Rellenas[j]
        a[i, j + 6] = int(round(a[i, j + 6]))

        if (a[i, j + 6] % 2) == 0:
            a[i, j + 6] = a[i, j + 6]

        else:
            # Esto garantiza que si hay un caso en el que el numero de celdas
            # es impar y menor a 2 (ejem Num celdas = 1) el programa no
            # lo trate como numero impar y le reste 1 unidad
            # lo cual de Num celdas = 0, que incurre en un error.
            if a[i, j + 6] > 2:
                a[i, j + 6] = a[i, j + 6] - 1
            else:
                a[i, j + 6] = 2

# aca se determina la distancia de cada barra (di), por el momento solo se hace del primer piso, hay
# que modificarlo para que calcule para todos los pisos------------------------------------------------------------------------------------------------------------------------------.

matriz_distancias = num.zeros([int(max(a[:, 6])), int(len(df))])

for i in range(0, len(df)):
    # longitud del muro en metros
    longitud_muro = a[i, 1]
    longitud_muro1 = 0
    for j in range(0, int(a[i, 6]/2)):
        # si es la primera o la utlima celda, el valor dado es
        if j == 0:
            matriz_distancias[j, i] = longitud_muro - df1.loc[22, 'Valores']/100
            longitud_muro = matriz_distancias[j, i]
            matriz_distancias[int(a[i, 6]-1), i] = df1.loc[22, 'Valores'] / 100
            longitud_muro1 = matriz_distancias[int(a[i, 6]-1), i]

        elif j == int(a[i, 6] - 1):
            matriz_distancias[int(a[i, 6]), i] = df1.loc[22, 'Valores'] / 100
            longitud_muro1 = matriz_distancias[int(a[i, 6]), i]

        else:
            if j % 2 == 0:
                # números pares distancia entre bloques
                matriz_distancias[j, i] = longitud_muro - 2*df1.loc[22, 'Valores']/100 - a[i, 4]
                longitud_muro = matriz_distancias[j, i]
                matriz_distancias[int((a[i, 6])-1-j), i] = longitud_muro1\
                                                    + 2*df1.loc[22, 'Valores']/100 - a[i, 4]
                longitud_muro1 = matriz_distancias[int((a[i, 6])-j-1), i]
            else:
                # números impares distancia entre celdas
                matriz_distancias[j, i] = longitud_muro - df1.loc[21, 'Valores']/100
                longitud_muro = matriz_distancias[j, i]
                matriz_distancias[int((a[i, 6])-j-1), i] = longitud_muro1 + df1.loc[21, 'Valores'] / 100
                longitud_muro1 = matriz_distancias[int((a[i, 6])-j-1), i]


# Aca se calcula el area efectiva y el espesor efectivo de cada muro, esto
# se hace por cada piso de la estructura
for i in range(0, len(df)):

    for j in range(0, len(porcentaje_Celdas_Rellenas)):
        # Area efectiva total en (m2)
        a[i, j + 6 + len(porcentaje_Celdas_Rellenas)] = a[i, 6 + j] * df1.loc[
            1, 'Valores'] + (df1.loc[13, 'Valores'] / 100) * a[i, 1] * 2

        # Espesor efectivo total en (m)
        a[i, j + 6 + len(porcentaje_Celdas_Rellenas) * 2] = a[
        i, j + 6 +len(porcentaje_Celdas_Rellenas)] / a[i, 1]

# Aca se calcula el efecto de pandeo D.5.4.2 no puede ser mayor a 25, es 2 si no lo cumple y 1 si lo
# cumple.
if df1.loc[11, 'Valores'] / (df1.loc[5, 'Valores'] * 10) < 25:
    # Si cumple entra aca
    # determinación del factor de reducción R para el calculo de la maxima
    # carga axial a compresión  D.5.5
    a[:, 6 + len(porcentaje_Celdas_Rellenas) * 3] = 1
    a[:, 7 + len(porcentaje_Celdas_Rellenas) * 3] = 1 - (
                df1.loc[11, 'Valores'] / ((df1.loc[5, 'Valores'] * 10) * 42)) ** 2
else:
    # Si no cumple entra aca D.5.5.2
    a[:, 6 + len(porcentaje_Celdas_Rellenas) * 3] = 2
    a[:, 7 + len(porcentaje_Celdas_Rellenas) * 3] = ((21 * (df1.loc[5, 'Valores'] * 10)) / df1.loc[
        11, 'Valores']) ** 2

# la carga maxima resistencia compresión teorica esta en KN, véase D.5.5.1
for i in range(0, len(df)):
    for j in range(0, len(porcentaje_Celdas_Rellenas)):
        # f'm*Ae
        a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 3] = \
            a[i, j + 6 + len(porcentaje_Celdas_Rellenas)]*df1.loc[8, 'Valores']*1000
        # 0.8*f'm*(Ae-Ast)+Ast*fy
        a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 4] = 0.8 * df1.loc[8, 'Valores']*1000*(a[
                i, j + 6 + len(porcentaje_Celdas_Rellenas) * 1]-(df1.loc[20, 'Valores']/(100**2)) * a[
                i, j + 6]) + (df1.loc[20, 'Valores']/(100**2)) * a[
                i, j + 6]*df1.loc[9, 'Valores']*1000

        # la carga maxima resistencia compresión teorica esta en KN, véase D.5.5.1 aca se hace
        # esa comprobación, si se cumple asigna un valor de uno a la celda del muro, si no se
        # cumple asigna un valor de 0

        if a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 3] > \
                a[i, j + 8 +len(porcentaje_Celdas_Rellenas) * 4]:
            a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 5] = 1
            # Calculo de Pu =phi * 0.8 * Re * P0 , en donde Phi = 0.6
            a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 6] = \
                0.6 * 0.8 * a[i,7 + len(porcentaje_Celdas_Rellenas) * 3] *\
                a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 4]
        else:
            a[i, j + 8 + len(porcentaje_Celdas_Rellenas) * 5] = 0

# aca se calcula el momento resistente de los muros y la carga axial, es decir su diagrama de
# interacción, el valor de 100 es el numero de puntos para la curva de interaccion,
# se puede cambiar pero ojo, tiene que cambiarse en todos los elementos

# la matriz matriz_m_p es donde se va a almacenar los diferentes puntos para la curva de interacción
matriz_Momento_M = num.zeros([100, int(len(df))])
matriz_Carga_P = num.zeros([100, int(len(df))])
matriz_Momento_Carga_P_M = num.zeros([100, int(len(df))*2])
# Esta es una matriz de 3 dimensiones , 1000 puntos de fond, para este caso, 20 filas y 12 columnas
fsi = num.zeros((100, int(max(a[:, 6])), int(len(df))))
Tsi = num.zeros((100, int(max(a[:, 6])), int(len(df))))
Msi = num.zeros((100, int(max(a[:, 6])), int(len(df))))
SumTsi = num.zeros((100, int(len(df))))
SumMsi = num.zeros((100, int(len(df))))


# Aca se determina el numero de ejes neutros para determinar los diferentes
# puntos para la curva de interacción, eje neutro c
c = num.zeros([100, int(len(df))])
# Cm carga a compresión de la mamposteria Cm = 0.8*f'm*a*te en donde a = 0.85*c
Cm = num.zeros([100, int(len(df))])
# Aca se determina el valor Cm y el valor c ( eje neutro)
for i in range(0, len(df)):
    for j in range(0, 100):
        c[j, i] = a[i, 1] - (a[i, 1]/100)*j
        Cm[j, i] = 0.8 * df1.loc[8, 'Valores'] * 1000 * c[j, i] * 0.85 * \
                   a[i, 6 + len(porcentaje_Celdas_Rellenas) * 2]

# Aca se determina el esfuerzo fsi en cada varilla de cada muro, para cada variación del eje neutro
for k in range(0, len(df)):
    for i in range(0, 100):
        for j in range(0, int(a[k, 6])):
            # el valor fsi = Es*(c-di)*(emu/c)
            fsi[i, j, k] = df1.loc[24, 'Valores'] * \
                           (c[i, k]-matriz_distancias[j, k])*(df1.loc[10, 'Valores']/c[i, k])
            # Fuerzas de tension son negativas es decir -420 y fuerzas de compresión son positivas
            if abs(fsi[i, j, k]) <= 420:
                fsi[i, j, k] = fsi[i, j, k]
                Tsi[i, j, k] = fsi[i, j, k] * (df1.loc[20, 'Valores'] / (100**2)) * 1000
                SumTsi[i, k] = SumTsi[i, k] + Tsi[i, j, k]
                Msi[i, j, k] = Tsi[i, j, k] * (a[k, 1]/2 - matriz_distancias[j, k])
                SumMsi[i, k] = SumMsi[i, k] + Msi[i, j, k]

            elif abs(fsi[i, j, k]) > 420:
                if fsi[i, j, k] < 0:
                    fsi[i, j, k] = -420
                    Tsi[i, j, k] = fsi[i, j, k] * (df1.loc[20, 'Valores'] / (100 ** 2)) * 1000
                    SumTsi[i, k] = SumTsi[i, k] + Tsi[i, j, k]
                    Msi[i, j, k] = Tsi[i, j, k] * (a[k, 1] / 2- matriz_distancias[j, k])
                    SumMsi[i, k] = SumMsi[i, k] + Msi[i, j, k]
                elif fsi[i, j, k] > 0:
                    fsi[i, j, k] = 420
                    Tsi[i, j, k] = fsi[i, j, k] * (df1.loc[20, 'Valores'] / (100 ** 2)) * 1000
                    SumTsi[i, k] = SumTsi[i, k] + Tsi[i, j, k]
                    Msi[i, j, k] = Tsi[i, j, k] * (a[k, 1] / 2 - matriz_distancias[j, k])
                    SumMsi[i, k] = SumMsi[i, k] + Msi[i, j, k]

        matriz_Carga_P[i, k] = Cm[i, k] + SumTsi[i, k]
        matriz_Momento_M[i, k] = ( a[k, 1] / 2 - (c[i, k] * 0.85) / 2) * Cm[i, k] + SumMsi[i, k]

M_Balanceado = num.zeros(int(len(df)))
P_Balanceado = num.zeros(int(len(df)))
for i in range(0, len(df)):
    Mmax = max(matriz_Momento_M[:, int(i)])
    for j in range(0, 100):
        if matriz_Momento_M[j, int(i)] == Mmax:
            M_Balanceado[i] = Mmax*0.85
            P_Balanceado[i] = matriz_Carga_P[j, int(i)]*0.85

for i in range(0, len(df)*2, 2):
    for j in range(0, 100):
        if matriz_Carga_P[j, int(i/2)] <= P_Balanceado[int(i/2)] \
                and matriz_Momento_M[j, int(i / 2)] <= M_Balanceado[int(i/2)]:
            if matriz_Carga_P[j, int(i/2)] <= 0.9 * P_Balanceado[int(i/2)] \
                    and matriz_Momento_M[j, int(i / 2)] <= 0.9*M_Balanceado[int(i/2)]:
                matriz_Momento_Carga_P_M[j, i + 1] = 0.85*matriz_Carga_P[j, int(i / 2)]
                matriz_Momento_Carga_P_M[j, i] = 0.85*matriz_Momento_M[j, int(i / 2)]
            elif matriz_Carga_P[j, int(i / 2)] <= P_Balanceado[int(i / 2)] \
                    and matriz_Momento_M[j, int(i / 2)] <= M_Balanceado[int(i / 2)]:
                matriz_Momento_Carga_P_M[j, i + 1] = 0.65 * matriz_Carga_P[j, int(i / 2)]
                matriz_Momento_Carga_P_M[j, i] = 0.65 * matriz_Momento_M[j, int(i / 2)]
        else:
            matriz_Momento_Carga_P_M[j, i + 1] = 0.60 * matriz_Carga_P[j, int(i / 2)]
            matriz_Momento_Carga_P_M[j, i] = 0.60 * matriz_Momento_M[j, int(i / 2)]


df2 = pd.DataFrame({'Número del Muro': a[:, 0], 'Longitud del Muro (m)': a[:, 1],
                    'Número de Bloques de'.format(df1.loc[4, 'Valores']): a[:, 2],
                    'Número de Bloques de'.format(df1.loc[6, 'Valores']): a[:, 3],
                    'Espesor mortero de pega (m)': a[:, 4],
                    'Numero de celdas por muro': a[:, 5]})

df2.to_csv(index=False)
