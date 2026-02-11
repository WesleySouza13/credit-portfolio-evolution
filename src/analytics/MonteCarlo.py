import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
class MonteCarlo:
    def __init__(self, years, data, cenary, cols_sim, stress_dict):
        self.years = years * 252
        self.data = data.copy()
        self.cenary = cenary
        self.cols_sim = cols_sim
        self.stress_dict = stress_dict

        if 'data' in self.data.columns:
            self.data['data'] = pd.to_datetime(self.data['data'])
            self.data = self.data.set_index('data')
    def _base_params(self):
        X = self.data[self.cols_sim]
        mean = X.mean().values
        std = X.std().values
        cov = X.cov().values
        return mean, std, cov
    def normal_input(self):
        mean, std, cov = self._base_params()
        X_sim = np.random.multivariate_normal(
            mean=mean,
            cov=cov,
            size=(self.cenary, self.years)
        )
        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                X_sim[s],
                columns=self.cols_sim
            )
            #df_s['cenario'] = s
            #df_s['t'] = np.arange(self.years)
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'CENÁRIO NORMAL | {self.cenary} cenários | horizonte {self.years}')
        return df_sim
    def stress_cenario(self, intensity=2.0):
        mean, std, cov = self._base_params()
        shock_signal = np.array(
            [np.sign(self.stress_dict[c]) for c in self.cols_sim]
        )
        shock_mu = mean + intensity * shock_signal * std
        X_shock = np.random.multivariate_normal(
            mean=shock_mu,
            cov=cov,
            size=(self.cenary, self.years)
        )
        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                X_shock[s],
                columns=self.cols_sim
            )
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'CENÁRIO PESSIMISTA | {self.cenary} cenários | {intensity}σ')
        return df_sim
    def optimism(self, optimism_dict, intensity=1.0):
        mean, std, cov = self._base_params()
        shock_signal = np.array(
            [np.sign(optimism_dict[c]) for c in self.cols_sim]
        )
        shock_mu = mean + intensity * shock_signal * std
        X_shock = np.random.multivariate_normal(
            mean=shock_mu,
            cov=cov,
            size=(self.cenary, self.years)
        )

        dfs = []
        for s in range(self.cenary):
            df_s = pd.DataFrame(
                X_shock[s],
                columns=self.cols_sim
            )
            dfs.append(df_s)
        df_sim = pd.concat(dfs, ignore_index=True)
        print(f'CENÁRIO OTIMISTA | {self.cenary} cenários')
        return df_sim
