import pandas as pd 
import numpy as np 
import sys 
import os 
import re 
import datetime
from collections import namedtuple
from time import sleep

collections_entrada = namedtuple('Entrada', 'id_entrada unidade_entrada quantidade_entrada data_entrada lote_entrada vencimento id_produto')

class Excel:
    '''
        Classe responsável por converter um arquivo excel em uma matriz 
        que contém somente as colunas especificicas nos argumentos

        • nome_arquivo - type:str : nome do arquivo a ser analisado, juntamento com sua extensão.
            Arquivos disponíveis: (.xls, .xlsx)
        
        Para realizar a filtragem das colunas e retonar a matriz, é necessário 
        chamar o objeto em questão passando o seguinte paramento:
        
        • columns_select - type:dict : dicionário das colunas selecionadas do dataframe como chave, e como valor 
            os respectivos nomes desejados.
    '''
        
    data_frames_analise = 0
    
    def __init__(self, nome_arquivo:str, **columns_select:dict):

        EXTENSOES_ACEITAS = {'xlsx', 'xls'} 
        
        self.dict_columns = columns_select
        self.columns_select = [value for value in columns_select.keys()] 
        self.nome_arquivo = nome_arquivo
        
        if self.nome_arquivo.rsplit('.')[1] not in EXTENSOES_ACEITAS:
            raise TypeError(
                'Não há suporte para a extensão do arquivo: %s ' % self.nome_arquivo.rsplit('.')[1]
            )

        try:
            self._arquivo = pd.read_excel(os.path.join(os.getcwd(), 'static', self.nome_arquivo))
        except:
            raise ValueError

    @classmethod
    def dataframe_em_uso(cls):
        cls.data_frames_analise += 1
        return f'Está em uso: {cls.data_frames_analise}'

    def __getitem__(self, index):
        try:
            return np.array(self.data_frame_filter).T[index]
        except:
            raise TypeError

    def __repr__(self) -> str:
        try:
            return f'{self.data_frame_filter}'
        except:
            raise TypeError

    def filter_frame(self):
        columns_drop = []
        
        for columns_frame in self._arquivo.columns:
            if columns_frame not in self.columns_select:
                columns_drop.append(columns_frame)
        
        self.data_frame_filter = self._arquivo.drop(columns_drop, axis=1).rename(columns=self.dict_columns)
        
        return self.data_frame_filter