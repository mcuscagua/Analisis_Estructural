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


    def grafica_momento(self):
        df = self.plot_momento.copy()

        YY = []
        XX = []

        for i in range(0, df.shape[0] - 1):

            p1 = df.iloc[i, :]
            p2 = df.iloc[i + 1, :]

            if p1['X'] == p2['X']:
                XX.append(np.array([0]))
                YY.append(np.array([0]))

            elif p1['Y'] == p2['Y']:
                x1 = 0
                y1 = 0
                x2 = p2['X'] - p1['X']
                y2 = x2 * p2['Y']

                refx = np.linspace(0, x2)
                refy = (y2 / x2) * (refx - x2) + y2
                XX.append(refx)
                YY.append(refy)
            else:

                if p2['Y'] < 0 and p1['Y'] < 0:
                    refx = np.linspace(0, p2['X'] - p1['X'])

                    a = (p2['Y'] - p1['Y']) / (2 * (p2['X'] - p1['X']))
                    b = -p2['X'] * (p2['Y'] - p1['Y']) / (p2['X'] - p1['X'])
                    d = p2['Y']
                    refy = (-a * refx ** 2) + b * refx + d * refx
                    XX.append(refx)
                    YY.append(-refy)
                else:
                    refx = np.linspace(0, p2['X'] - p1['X'])

                    a = (p2['Y'] - p1['Y']) / (2 * (p2['X'] - p1['X']))
                    b = -p2['X'] * (p2['Y'] - p1['Y']) / (p2['X'] - p1['X'])
                    d = p2['Y']
                    refy = (a * refx ** 2) + b * refx + d * refx

                    XX.append(refx)
                    YY.append(refy)

        XF = XX[0]
        YF = YY[0]

        for i in range(1, len(XX)):
            if len(XX[i]) > 1:
                XF = np.concatenate((XF, XX[i] + XF[-1]), axis=None)
                YF = np.concatenate((YF, YY[i] + YF[-1]), axis=None)

        self.Final = pd.DataFrame()
        self.Final['X'] = XF
        self.Final['Y'] = YF

        Xi = []

        referentes = df['X'].unique()
        for i in range(len(referentes)):
            Xi += np.where(self.Final['X'] == referentes[i])[0].tolist()

        Yi = self.Final.iloc[Xi, 1].values.tolist()

        Xi = np.array(Xi)
        Yi = [np.round(j,2) for j in Yi]

        plt.figure(figsize=(10, 10))
        plt.plot(self.Final['X'], self.Final['Y'])
        plt.grid()
        #for i in range(len(Xi)):
        #    plt.annotate("("+str(Xi[i])+","+str(Yi[i])+")", (Xi[i], Yi[i]), (Xi[i], Yi[i]))
        plt.show()
        