import numpy as np
import pandas as pd

from typing import Union
from copy   import deepcopy

class FilaPrioridade:

    def __init__(self) -> None:

        self.fila: np.array = np.array([])

        self.pai            = lambda x: (x-1)//2
        self.filho_direito  = lambda x: x*2 + 2
        self.filho_esquerdo = lambda x: x*2 + 1
        
        return None
    
    def inserir(self, item: np.array) -> "FilaPrioridade":

        self.fila = np.append(self.fila, item)

        i: int = np.shape(self.fila)[0] - 1

        while i > 0:

            pai = self.pai(i)

            if self.fila[pai, 0] < self.fila[i, 0]:

                self.fila[pai], self.fila[i] = self.fila[i], self.fila[pai]

                i = pai

            else:

                break

        return self
    
    def retirar(self) -> np.array:
        #vai funcionar tal qual o pop

        if np.shape(self.fila)[0] == 0:

            raise "Lista vazia"

        item: np.array = deepcopy(self.fila[0])

        self.fila[0] = self.fila[-1]
        
        self.fila = self.fila[:-1]
               
        i:   int = 0
        len: int = np.shape(self.fila)[0]

        while True:

            filho_d:int = self.filho_direito(i)
            filho_e:int = self.filho_esquerdo(i)

            if filho_e > len:

                break

            maior_filho = filho_e

            if filho_d < len and self.fila[filho_d, 0] > self.fila[filho_e, 0]:

                maior_filho = filho_d

            if self.fila[i, 0] < self.fila[maior_filho, 0]:

                self.fila[i], self.fila[maior_filho] = self.fila[maior_filho], self.fila[i]

                i = maior_filho

            else:

                break

        return item

class Date_ESEM:

    def __init__(self, file_path: Union[str, pd.DataFrame]) -> None:
        
        self.dado: pd.DataFrame = self.__ler_dado(file_path=file_path)

        return None
    
    def __ler_dado(self, file_path: Union[str, pd.DataFrame]) -> pd.DataFrame:

        if file_path is pd.DataFrame:

            return file_path

        elif file_path.endswith() == '.csv':

            return pd.read_csv(file_path)
        
        elif file_path.endswith() == '.xlsx' or file_path.endswith() == '.xls':

            return pd.read_excel(file_path)
        
        else:

            raise "A extenção do arquivo  deve ser .csv, .xlsx ou .xls; \n também é possivel passar a proprioa clss pandas.DataFrame."
        
    def __pontuacao(self, pessoa_0: pd.DataFrame, pessoa_1: pd.DataFrame) -> float:

        nome:        tuple[str] = pessoa_0['Nome'],        pessoa_1['Nome']
        genero:      tuple[str] = pessoa_0['Genero'],      pessoa_1['Genero']
        sexualidade: tuple[str] = pessoa_0['Sexualidade'], pessoa_1['Sexualidade']
        respostas:   np.array   = pessoa_0.drop(['Genero', 'Sexualidade'], axis=0).to_numpy() - pessoa_0.drop(['Genero', 'Sexualidade'], axis=0).to_numpy()

        combinacoes_incompativeis = {
            "Hetero": {
                ("F", "F"),
                ("M", "M")
            },
            "Gay": {
                ("M", "F"),
                ("F", "M"),
                ("F", "NB")
            },
            "Lesbica": {
                ("F", "M"),
                ("M", "F"),
                ("M", "NB")
            },
            "Bissexual": set(),
            "NB": set()
        }

        if (genero[0], genero[1]) in combinacoes_incompativeis.get(sexualidade[0]) | combinacoes_incompativeis.get(sexualidade[1]):

            return 100
        
        else:

            return np.array([np.linalg.multi_dot([respostas, respostas]), nome[0], nome[1]])
        
    def agrupar_casais(self, colunas_interesse: Union[list, None] = None) -> set:
        #Ao não adicionar parâmetro entende-se que tdas as colunas imputadas a classe são os dados de interresse

        if colunas_interesse is list:

            dado: pd.DataFrame = deepcopy(self.dado[colunas_interesse])

        elif  colunas_interesse is None:

            dado: pd.DataFrame = deepcopy(self.dado)

        else:

            raise ValueError('As colunas de interresse só são suportdadas para o tipo list ou entregue o data frame pronto ao carregar o objeto.')
        
        len: int =  dado.shape[0]
        
        fila_prioridade: FilaPrioridade = FilaPrioridade()

        for i in range(0, len):

            for j in range(0, len):

                if i != j:

                    fila_prioridade.inserir(self.__pontuacao(dado.iloc[i], dado.iloc[j]))

        pessoas: set = {}
        casais:  set = {}

        while fila_prioridade:

            par = fila_prioridade.retirar()

            if par[1] not in pessoas and par[2] not in pessoas:

                casais.add(par[1:3]) #[1:3] é para retirar apenas o nome do casal

            else:

                pass
                    
        return casais
        