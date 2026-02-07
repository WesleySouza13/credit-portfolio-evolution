import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
class MonteCarlo():
    def __init__(self, years:int, data:pd.DataFrame, cenary:int, cols_sim:list, stress_dict: dict):
        """"
                days: dias que queremos dar passos para frente aos dados
                data: dados que queremos simular
                cenary: quantos cenarios diferentes queremos estimar"""
        self.years = years*252 
        self.data = data
        self.cenary = cenary
        self.cols_sim = cols_sim
        self.stress_dict = stress_dict
    def normal_input(self):
        if 'data' in self.data.columns:
            self.data['data'] = pd.to_datetime(self.data['data'])
            self.data = self.data.set_index('data')
        mean = self.data.mean().values
        std = self.data.std().values          
        print('==='*50)
        print()
        print(f'media dos dados: {mean}')
        print()
        print('==='*50)
        print(f'dimensoes media: {mean.shape}')
        #print(f'dimensoes cov: {cov.shape}')
        X_sim = np.random.normal(mean, std, size=(self.cenary, self.data.shape[1]))
        #X = np.random.multivariate_normal(mean=mean, cov=cov, size=(self.cenary, self.years))
        print(f'media - cenario normal: {X_sim.mean()}')
        print(f'Criando cenario de normalidade em {self.cenary} cenários')
        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                [X_sim[s]],
                columns=self.cols_sim
            )
            #df_s['cenario'] = s
            #df_s['t'] = np.arange(1, self.years + 1)
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'Cenario NORMAL | {self.cenary} cenarios | horizonte {self.years}')
        return df_sim
    
    def stress_cenario(self):
        if 'data' in self.data:
            self.data['data'] = pd.to_datetime(self.data['data'])
            self.data = self.data.set_index('data')
        X = self.data[self.cols_sim]
        mean = X.mean().values
        std = X.std().values
        cov = X.cov().values
        shock_vector = np.array([self.stress_dict[j] for j in self.cols_sim])
        shock_mu = mean + shock_vector *std
        X_shock = np.random.multivariate_normal(shock_mu, cov, size=(self.cenary, self.years))
        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                X_shock[s],
                columns=self.cols_sim
            )
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'Cenário PESSIMISTA | {self.cenary} cenários | horizonte {self.years}')

        return df_sim
    
    def optimism(self, optimism_dict:dict):
        if 'data' in self.data:
            self.data['data'] = pd.to_datetime(self.data['data'])
            self.data = self.data.set_index('data')
        X = self.data[self.cols_sim]
        
        mean = self.data.mean()
        std = self.data.std()
        cov = self.data.cov()
        
        shock_vector = np.array([optimism_dict[j] for j in self.cols_sim])
        shock_mu = mean + shock_vector *std
        X_shock = np.random.multivariate_normal(shock_mu, cov, size=(self.cenary, self.years))
        
        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                X_shock[s],
                columns=self.cols_sim
            )
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'Cenário OTIMISTA | {self.cenary} cenários | horizonte {self.years}')
        
        return df_sim