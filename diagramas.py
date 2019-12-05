import matplotlib.pylab as plt
import numpy as np
import pandas as pd

class graficador():
    def __init__(self):
        self.tipo = []
        self.magnitud = []
        self.longitud = []

        aux = True
        i = 0
        while aux:
            self.tipo.append(input("Escriba el tipo de la carga/reaccion " + str(i + 1) + ": "))
            self.magnitud.append(float(input("Escriba la magnitud de la carga/reaccion: ")))
            self.longitud.append(float(input("Escriba la longitud de la carga/reaccion: ")))

            mas_pedazos = input("Hay mas trozos?: ")

            print("\n")

            i += 1

            if mas_pedazos == 'no':
                aux = False

    def grafica_1(self):

        ref = 0
        Ltotal = 0

        self.Y = [ref]
        self.X = [Ltotal]

        for i in range(len(Graficas.tipo)):
            if Graficas.tipo[i] == "puntual":
                ref += -Graficas.magnitud[i]
                Ltotal += Graficas.longitud[i]

            if Graficas.tipo[i] == "distribuida":
                ref += -Graficas.magnitud[i] * Graficas.longitud[i]
                Ltotal += Graficas.longitud[i]

            if Graficas.tipo[i] == "triangular":
                ref += -0.5 * Graficas.magnitud[i] * Graficas.longitud[i]
                Ltotal += Graficas.longitud[i]

            if Graficas.tipo[i] == "reaccion":
                ref += Graficas.magnitud[i]
                Ltotal += Graficas.longitud[i]

            if Graficas.tipo[i] == "nada":
                ref += Graficas.magnitud[i]
                Ltotal += Graficas.longitud[i]

            self.Y.append(ref)
            self.X.append(Ltotal)

        plt.figure()
        plt.plot(self.X, self.Y)
        plt.show()

