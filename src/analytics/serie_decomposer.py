import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 

class Serie_Decomposer():
    def __init__(self, data:pd.DataFrame):
        self.data = data
    
    def sazo(self):
        print('===='*50)
        print()
        print('Sazonalidade:')
        sazo = self.data.diff()
        print(sazo)
        fig, ax = plt.subplots(len(self.data.columns), 1, figsize=(14, 4 * len(self.data.columns)))
        for axes, plot in zip(ax, self.data.columns):
            axes.plot(sazo[plot], color='orange')
            axes.set_title(f'Sazonalidade - {plot}')
            fig.tight_layout()
            fig.show()
    
    def move_avg(self, window):
        print('===='*50)
        print()
        if window <= 12:
            try:
                print(f'Média movel para janela de {window} meses:')
                move_avg = self.data.rolling(window).mean()
                print(move_avg)
                fig, ax = plt.subplots(len(self.data.columns), 1, figsize=(14, 4 * len(self.data.columns)))
                for axes, plot in zip(ax, self.data.columns):
                    axes.plot(move_avg[plot], label='media movel', color='red')
                    axes.plot(self.data[plot], color='blue')
                    axes.set_title(f'Media movel - {plot}')
                plt.legend()
                fig.tight_layout()
                fig.show()
            except ValueError:
                print('Por conta de se tratar de valores mensais, escolha janelas em um intervalo de 1 a 12 meses')