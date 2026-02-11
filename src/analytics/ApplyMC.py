import numpy as np 
import matplotlib.pyplot as plt
class AppMC():
    def __init__(self, y_pred, residual:float):
        self.y_pred = y_pred
        self.residual = residual
        #self.cenary = cenary
    
    def sim_mc(self):
        mu_resid = self.residual.mean()
        std_resid = self.residual.std()
        print('==='*50)
        print(f'Média dos residuos:{mu_resid}')
        print()
        print(f'Desvio padrão dos residuos: {std_resid}')
        print('==='*50)
        if std_resid <=1 and mu_resid == 0:
            print('==='*50)
            print('Notas:')
            print('[1] os residuos se aproximam da normalidade, pelo menos olhando para os desvios e médias dos mesmos.')
        
            print('==='*50)

        eps = np.random.normal(mu_resid, std_resid, len(self.y_pred))
        y_mc = self.y_pred + eps
        self.y_hat = y_mc.mean(axis=0)
        self.y_ac_mu = np.cumsum(y_mc)/np.arange(1, len(y_mc)+1)
        
        print('==='*50)
        print('resultados:')
        print(f'[1] Média estimada: {self.y_hat} ')
        print(f'[2] Médias acumuladas: {self.y_ac_mu} ')
        print('==='*50)
    def plot_results(self, name_sim:str):
        plt.figure(figsize=(12,8))
        plt.title(f'Resultados simulação de Monte Carlo - Cenários simulados: {len(self.y_pred)} - {name_sim}')
        plt.axhline(self.y_hat, color='black', linestyle='--', label=f'Média Simulada - {np.round(self.y_hat, 3)}')
        plt.plot(self.y_ac_mu, color='red', label='Valores esperados E[Y|X]')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        