import matplotlib.pylab as plt
import numpy as np
import pandas as pd

class graficador():
    def __init__(self, Viga):
        self.viga = Viga
        self.coordenadas = pd.DataFrame()

        j = 0
        for tramo in self.viga.tramos:

            influencia = ['reaccion']
            X = [0]
            Y = [self.viga.Rs[j]]

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
            df = df.sort_values(['X'], )
            df = df.reset_index(drop=True)

            T, X1, Y1 = ['nada', influencia[0]], [0, X[0]], [0, Y[0]]

            dis_click = False
            for i in range(1, df.shape[0]):

                if df.iloc[i, 0] == 'puntual' and not dis_click:
                    T += ['nada','puntual']
                    X1 += [df.iloc[i, 1] - df.iloc[i - 1, 1], 0]
                    Y1 += [0, df.iloc[i, 2]]

                elif df.iloc[i, 0] == 'puntual' and dis_click:
                    T += ['puntual']
                    X1 += [0]
                    Y1 += [df.iloc[i, 2]]

                if df.iloc[i, 0] == 'distribuida' and not dis_click:
                    if df.iloc[i - 1, 0] == 'puntual' and df.iloc[i - 1, 1] == df.iloc[i, 1]:
                        T += ['distribuida', 'distribuida']
                        X1 += [0, df.iloc[i + 1, 1] - df.iloc[i, 1]]
                        Y1 += [0, df.iloc[i, 2] * (df.iloc[i + 1, 1] - df.iloc[i, 1])]
                        dis_click = True
                    else:
                        T += ['distribuida']
                        X1 += [df.iloc[i + 1, 1]]
                        Y1 += [df.iloc[i, 2] * (df.iloc[i + 1, 1] - df.iloc[i, 1])]
                        dis_click = True

                elif df.iloc[i, 0] == 'distribuida' and dis_click:

                    if df.iloc[i - 1, 0] == 'distribuida':
                        T += ['nada']
                        X1 += [0]
                        Y1 += [0]

                        dis_click = False
                    else:
                        T += ['distribuida', 'nada']
                        X1 += [df.iloc[i, 1] - df.iloc[i - 1, 1], 0]
                        Y1 += [df.iloc[i, 2] * (df.iloc[i, 1] - df.iloc[i - 1, 1]), 0]

                        dis_click = False
            T += ['nada']
            X1 += [tramo['L'] - sum(X1)]
            Y1 += [0]


            df = pd.DataFrame([T, X1, Y1], index=['tipo', 'X', 'Y']).T.fillna(0)
            self.coordenadas = pd.concat([self.coordenadas, df], ignore_index=True)
            j += 1


        dff = pd.DataFrame(['Reaccion', 0, self.viga.Rs[-1]], index=['tipo', 'X', 'Y']).T.fillna(0)

        self.coordenadas = pd.concat([self.coordenadas, dff], ignore_index=True)



    def grafica_cortante(self):
        self.X_cortante = self.coordenadas['X'].cumsum()
        self.Y_cortante = self.coordenadas['Y'].cumsum()
        self.plot_momento = pd.DataFrame([self.coordenadas['tipo'], self.X_cortante, self.Y_cortante], index=['tipo', 'X', 'Y']).T
        fig = plt.figure(figsize=(10, 10))
        plt.plot(self.X_cortante, self.Y_cortante)
        for i_x, i_y in zip(self.X_cortante, np.round(self.Y_cortante, 2)):
            plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))
        plt.grid()
        plt.show()

