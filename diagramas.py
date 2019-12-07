import matplotlib.pylab as plt
import numpy as np
import pandas as pd

class graficador():
    def __init__(self, Viga):
        self.viga = Viga
        self.coordenadas = pd.DataFrame()

        i = 0
        for tramo in self.viga.tramos:

            influencia = ['reaccion']
            X = [0]
            Y = [self.viga.Rs[i]]

            for car,carac in tramo['cargas'].items():
                if carac['tipo'] == 'puntual':
                    influencia.append('puntual')
                    X.append(carac['distancia'])
                    Y.append(-carac['magnitud'])

                if carac['tipo'] == 'distribuida':
                    influencia += ['distribuida', 'distribuida']
                    X += [carac['distancia'], carac['distancia'] + carac['longitud']]
                    Y += [-carac['magnitud'], -carac['magnitud']]

            df = pd.DataFrame([influencia, X, Y], index=['tipo', 'X', 'Y']).T.fillna(0)

            T, X1, Y1 = [influencia[0]], [X[0]], [Y[0]]


            dis_click = False
            for i in range(1, df.shape[0]-1):
                if df['tipo'][i] == 'puntual':
                    T += ['nada', 'puntual']
                    X1 += [df['X'][i], 0]
                    Y1 += [0, df['Y'][i]]



                if df['tipo'][i] == 'distribuida' and not dis_click and df['tipo'][i+1] != 'distribuida':
                    T += ['nada', 'distribuida']
                    X1 += [0, df['X'][i]]
                    Y1 += [0, df['Y'][i] * (df['X'][i+1] - df['X'][i])]

                    dis_click = True

                elif df['tipo'][i] == 'distribuida' and dis_click and df['tipo'][i - 1] == 'distribuida':
                    T += ['nada']
                    X1 += [0]
                    Y1 += [0]

                    dis_click = False

                elif df['tipo'][i] == 'distribuida' and not dis_click and df['tipo'][i+1] == 'distribuida':
                    T += ['nada', 'distribuida']
                    X1 += [0, df['X'][i]]
                    Y1 += [0, df['Y'][i] * (df['X'][i + 1] - df['X'][i])]

                    dis_click = True

                elif df['tipo'][i] == 'distribuida' and dis_click and df['tipo'][i - 1] != 'distribuida':
                    T += ['nada', 'distribuida']
                    X1 += [0, df['X'][i]]
                    Y1 += [0, df['Y'][i] * (df['X'][i -1] - df['X'][i])]

                    dis_click = False

            T.append('reaccion')
            X1.append(0)
            Y1.append(self.viga.Rs[-1])

            df = pd.DataFrame([T, X1, Y1], index=['tipo', 'X', 'Y']).T.fillna(0)

            self.coordenadas = pd.concat([self.coordenadas, df.sort_values('X')])

            i += 1


        #     INF1, X1, Y1, =
        #
        #     for i in range(1,df.shape[0]-1):

        #
        #         if df['tipo'][i] == 'distribuida' and df['tipo'][i+1] == 'puntual':
        #             if i+1 == len(list(range(1,df.shape[0]-1))):
        #                 INF1 += ['nada', 'distribuida']
        #                 X1 += [df['X'][i], 0]
        #                 Y1 += [0, df['Y'][i]]
        #             else:
        #
        #
        #
        #
        #
        #     i += 1
        #
        # influencia.append('reaccion')
        # X.append(0)
        # Y.append(self.viga.Rs[-1])
        #
        #
        # self.coordenadas = pd.DataFrame([influencia, X, Y], index = ['tipo', 'X', 'Y']).T.fillna(0)
        #
        # self.coordenadas['Xaxis'] = self.coordenadas['X'].cumsum()
        # self.coordenadas['Yaxis'] = self.coordenadas['Y'].cumsum()
        #
        # self.coordenadas = self.coordenadas.sort_values('Xaxis')





        # ref = 0
        # Ltotal = 0
        #
        # self.Y_cortante = [ref]
        # self.X_cortante = [Ltotal]
        #
        # for i in range(len(self.tipo)):
        #     if self.tipo[i] == "puntual":
        #         ref += -self.magnitud[i]
        #         Ltotal += self.longitud[i]
        #
        #     if self.tipo[i] == "distribuida":
        #         ref +=
        #         Ltotal += self.longitud[i]
        #
        #     # if self.tipo[i] == "triangular":
        #     #     ref += -0.5 * self.magnitud[i] * self.longitud[i]
        #     #     Ltotal += self.longitud[i]
        #     #
        #     # if self.tipo[i] == "reaccion":
        #     #     ref += self.magnitud[i]
        #     #     Ltotal += self.longitud[i]
        #
        #     if self.tipo[i] == "nada":
        #         ref += self.magnitud[i]
        #         Ltotal += self.longitud[i]
        #
        #     self.Y.append(ref)
        #     self.X.append(Ltotal)
        #
        # for tramo in viga.tramos:
        #
        #
        #
        #
        # aux = True
        # i = 0
        # while aux:
        #     self.tipo.append(input("Escriba el tipo de la carga/reaccion " + str(i + 1) + ": "))
        #     self.magnitud.append(float(input("Escriba la magnitud de la carga/reaccion: ")))
        #     self.longitud.append(float(input("Escriba la longitud de la carga/reaccion: ")))
        #
        #     mas_pedazos = input("Hay mas trozos?: ")


    def encontrar_coordenadas(self):



        fig = plt.figure(figsize=(10, 10))
        plt.plot(self.X, self.Y)
        for i_x, i_y in zip(self.X, np.round(self.Y, 2)):
            plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
        plt.grid()
        plt.show()

