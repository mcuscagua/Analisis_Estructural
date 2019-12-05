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

        for i in range(len(self.tipo)):
            if self.tipo[i] == "puntual":
                ref += -self.magnitud[i]
                Ltotal += self.longitud[i]

            if self.tipo[i] == "distribuida":
                ref += -self.magnitud[i] * self.longitud[i]
                Ltotal += self.longitud[i]

            if self.tipo[i] == "triangular":
                ref += -0.5 * self.magnitud[i] * self.longitud[i]
                Ltotal += self.longitud[i]

            if self.tipo[i] == "reaccion":
                ref += self.magnitud[i]
                Ltotal += self.longitud[i]

            if self.tipo[i] == "nada":
                ref += self.magnitud[i]
                Ltotal += self.longitud[i]

            self.Y.append(ref)
            self.X.append(Ltotal)

        fig = plt.figure(figsize=(10, 10))
        plt.plot(self.X, self.Y)
        for i_x, i_y in zip(self.X, np.round(self.Y, 2)):
            plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
        plt.grid()
        plt.show()

