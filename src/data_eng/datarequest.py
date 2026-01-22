import requests 
import pandas as pd
import sqlite3
import os 
class Series_requests():
    def __init__(self, codes:list, data_start:str, data_end:str):
        self.code = codes 
        self.data_start = data_start
        self.data_end = data_end
    
    def get_data(self):
        self.df_list = []
        for codes in self.code:
            print('codigo', codes)
            print(type(codes))
            print(f'iterando sobre o codigo: {codes}')
            url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codes}/dados?formato=json&dataInicial={self.data_start}&dataFinal={self.data_end}'
            response = requests.get(url)
            print('==='*50)
            print(f'saida da api:{response.status_code}')
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                df = df.sort_values(by='data')
                df['data']= pd.to_datetime(df['data'], dayfirst=True)
                #df = pd.to_numeric(df[df.columns], errors='coerce')
                df = df.set_index('data')
                df = df.apply(pd.to_numeric, errors='coerce')
                print(df.shape)
                #df = df.rename(columns={'valor':codes})
                self.df_list.append(df)
        
            
            #print(self.df_list)
    
    def concat(self):
        self.df_concat = pd.concat(self.df_list, ignore_index=True, axis=1)
        self.df_concat.columns = self.code
        #self.df_concat = pd.to_numeric(self.df_concat, errors='coerce')
        print(self.df_concat)
        return self.df_concat
    def to_parquet(self):
        data_path = os.path.join('..', 'data', 'VarMacroCredit.parquet')
        return self.df_concat.to_parquet(data_path)