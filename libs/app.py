
from libs.models import Produtos as banco_Produto
from libs.models import Fornecedores as banco_Fornecedores
from libs.models import Entradas as banco_Entradas
from libs.models import Saida as banco_Saida
from libs.models import Estoque as banco_Estoque
from libs.models import conn

import pandas as pd 
import numpy as np 
import sys 
import os 
import re 
import datetime
from collections import namedtuple
from time import sleep

from sqlalchemy import func
from sqlalchemy import update

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
            raise TypeError

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

class Fornecedores(Excel):
    def __init__(self, nome_arquivo: str, **columns_select: dict):
        super().__init__(nome_arquivo, **columns_select)
    

    def inclusao_banco(self):
        self.matriz_dados = np.array(self.filter_frame()).T
        for codigo, nome, cnpj in zip(self.matriz_dados[0], self.matriz_dados[1], self.matriz_dados[2]):
            # print(f'Codigo Fornecedor: {codigo} | Nome Fornecedor: {nome} | CNPJ: {cnpj}')
            consulta_banco = conn.query(banco_Fornecedores).filter_by(codigo_fornecedor = codigo).all()
            if not consulta_banco:
                # Codigo para cadastro no banco.
                fornecedor = banco_Fornecedores(
                    codigo_fornecedor = int(codigo),
                    nome_fornecedor = str(nome),
                    cnpj_fornecedor = str(cnpj),
                    comissao_fornecedor = float(0.00)
                    )
                
                conn.add(fornecedor)
                conn.commit()
                
                print(f'Codigo {codigo} | Fornecedor: {nome} cadastrado com sucesso !')
                sleep(0.2)        
        
        conn.close()

    # Consulta
    class Meta:
        my_atributte_bd = conn.query(banco_Fornecedores).order_by(banco_Fornecedores.codigo_fornecedor).all()

class Produtos(Excel):
    def __init__(self, nome_arquivo: str, **columns_select: dict):
        super().__init__(nome_arquivo = nome_arquivo, **columns_select)

    def inclusao_banco(self):
            self.matriz_dados = np.array(self.filter_frame()).T
            for codigo, nome, grupo, unidade, codigo_for, controle, comissao in zip(
                self.matriz_dados[0], 
                self.matriz_dados[1], 
                self.matriz_dados[2],
                self.matriz_dados[3],
                self.matriz_dados[4],
                self.matriz_dados[5],
                self.matriz_dados[6]):

                consulta_banco = conn.query(banco_Produto).filter_by(nome_produto = nome).all()
                if not consulta_banco:
                    # Codigo para cadastro no banco.
                    produto = banco_Produto(
                        codigo_produto = int(codigo),
                        nome_produto = str(nome),
                        unidade_produto = str(unidade),
                        controle_produto = bool(controle),
                        grupo_produto =  str(grupo),
                        comissao_produto = float(comissao),
                        codigo_fornecedor = int(codigo_for),
                    )

                    conn.add(produto)
                    conn.commit()
    
                    print(f'Codigo {codigo} | Produto: {nome} cadastrado com sucesso !')
                    sleep(0.1)        

            conn.close()
    
    class Meta:
        my_atributte_bd = conn.query(banco_Produto).order_by(banco_Produto.id_produto).all()

class Entradas:
    def __init__(self) -> None:
        self.entradas = []     

    def conversao_data(self, data_vencimento:str):
        '''Insira ambas as datas como str com a seguinte formatação:
            • ano-mes-dia
        '''
        
        self.data_vencimento = data_vencimento
        if isinstance(self.data_vencimento, str):
            try:
                self.vencimento = datetime.datetime.strptime(str(self.data_vencimento), '%Y-%m-%d')
            except:
                print('A formatação não coincide com: dia-mes-ano.')

    def buscar_produto(self, codigo_produto:int):
        self.codigo_produto = codigo_produto
        
        # Procurar o produto selecionado
        lista_ids = []
        
        consulta_em_produtos = conn.query(banco_Produto).filter(banco_Produto.codigo_produto == self.codigo_produto).all()
        if consulta_em_produtos:
            for r in consulta_em_produtos:
                print(f'ID: {r.id_produto} | Produto: {r.nome_produto} | Codigo Interno {r.codigo_produto} | Unidade {r.unidade_produto}')
                lista_ids.append(r.id_produto)

            id_selecionado = int(input('Digite o ID selecionado para entrada: '))
            if id_selecionado in lista_ids:
                print('Codigo pego')
                self.id_selecionado = id_selecionado
            
            else:
                print("Por favor, selecione um dos ID's acima")
        else:
            print('Produto não cadastrado. Por favor importe o arquivo de produtos para atualizar a listagem.')

    def quantidade_entrada(self):
        consulta = conn.query(banco_Produto).filter_by(id_produto = self.id_selecionado).all()
        for i in consulta:
            print(f'Produto: {i.nome_produto} | Unidade: {i.unidade_produto}')
        quantidade = int(input(f'Qual a quantidade de entrada em {i.unidade_produto} para o produto acima: '))
        self.quantidade = quantidade
    
    def quantidade_caixa_master(self):
        consulta = conn.query(banco_Produto).filter_by(id_produto = self.id_selecionado).all()
        for i in consulta:
            print(f'Produto: {i.nome_produto} | Unidade: {i.unidade_produto}')
        quantidade = int(input(f'Qual a quantidade do(a) {i.unidade_produto} para o produto acima: '))
        self.quantidade_caixa = quantidade
    
    def lote_entrada(self, lote):
        self.lote = lote

    def __call__(self):
        consulta = conn.query(banco_Produto).filter_by(id_produto = self.id_selecionado).all()
        for c in consulta:
            dict_data_for_entradas = {
                'unidade_entrada':c.unidade_produto,
                'quantidade_entrada':self.quantidade,
                'quantidade_caixa_master':self.quantidade_caixa,
                'data_entrada':datetime.datetime.today(),
                'lote_entrada':self.lote,
                'vencimento_produto':self.vencimento,
                'id_produto':self.id_selecionado
            }             
            self.registro_entradas(**dict_data_for_entradas)

            join_entrada_produto = conn.query(
                banco_Entradas.id_entrada,
                banco_Produto.codigo_produto,
                banco_Produto.nome_produto,
            ).join(
                banco_Produto,
                banco_Produto.id_produto == banco_Entradas.id_produto
            ).filter_by(
                id_produto = self.id_selecionado
            ).all()

            dict_data_for_estoque = {
                'codigo_produto':join_entrada_produto[0].codigo_produto, # S
                'nome_produto':join_entrada_produto[0].nome_produto, # S
                'id_entrada':join_entrada_produto[0].id_entrada, # S
                'unidade_produto':c.unidade_produto, # N
                'quantidade_produto':self.quantidade, # N 
                'data_entrada':datetime.datetime.today(), # N
                'lote_entrada':self.lote, # N
                'vencimento_produto':self.vencimento, # N
                'id_produto':self.id_selecionado
            }

            self.registro_estoque(**dict_data_for_estoque)  

            conn.close()
            break

    def registro_estoque(self, **kwargs):
        self.dados_estoque = kwargs
        
        estoque = \
            banco_Estoque(
                codigo_produto = self.dados_estoque['codigo_produto'],
                nome_produto = self.dados_estoque['nome_produto'],
                unidade_produto = self.dados_estoque['unidade_produto'],
                quantidade_produto = self.dados_estoque['quantidade_produto'],
                data_entrada = self.dados_estoque['data_entrada'],
                lote_entrada = self.dados_estoque['lote_entrada'],
                vencimento_produto = self.dados_estoque['vencimento_produto'],
                id_entrada = self.dados_estoque['id_entrada'],
                id_produto = self.dados_estoque['id_produto'],
            )
        conn.add(estoque)
        conn.commit()
        print('Inclusão na tabela ESTOQUE concluída com sucesso')

    def registro_entradas(self, **kwargs):
        self.dados_entrada = kwargs

        entradas = \
            banco_Entradas(
                unidade_entrada = self.dados_entrada['unidade_entrada'],
                quantidade_entrada = self.dados_entrada['quantidade_entrada'],
                quantidade_caixa_master = self.dados_entrada['quantidade_caixa_master'],
                data_entrada = self.dados_entrada['data_entrada'],
                lote_entrada = self.dados_entrada['lote_entrada'],
                vencimento_produto = self.dados_entrada['vencimento_produto'],
                id_produto = self.dados_entrada['id_produto'],
            )

        conn.add(entradas)
        conn.commit()
        print('Inclusão na tabela ENTRADAS concluída com sucesso')

class Saida(Excel):

    def __init__(self, nome_arquivo: str, **columns_select: dict):
        super().__init__(nome_arquivo, **columns_select)


    # Adicionar Funcionabilidade
    def __repr__(self):
        pass 

    def __getitem__(self, index):
        return super().__getitem__(index)

    # Adicionar Funcionabilidade
    def __call__(self):
        pass

    def consulta_quantidade_estoque(self, codigo_produto):
        consulta_join = conn.query(
            banco_Estoque.id_produto,
            banco_Produto.nome_produto.label('Produto'),
            banco_Entradas.quantidade_caixa_master.label('Unidade'),
            func.sum(banco_Estoque.quantidade_produto*banco_Entradas.quantidade_caixa_master).label('Total')
        ).join(
            banco_Entradas,
            banco_Entradas.id_entrada == banco_Estoque.id_entrada
        ).join(
            banco_Produto,
            banco_Produto.id_produto == banco_Entradas.id_produto
        ).filter_by(codigo_produto = codigo_produto).all()
        
        return consulta_join

    def att_tabela(self, codigo_produto, quantidade_unidade):
        # Consulta atráves do código do produto nesse caso 254 e pega todos os registros da tabela. 
        consulta = conn.query(banco_Estoque).order_by(banco_Estoque.vencimento_produto).filter_by(codigo_produto = codigo_produto).all()

        # Quantidade em Unidade que irá sair
        quantidade_unidade = quantidade_unidade

        resto = False 
        
        # Itera sobre todas as linhas encontradas para o produto 
        # procurado, sendo nesse caso, o codigo_produto.
        for c in range(len(consulta)):
            consulta_ttr = conn.query(
                banco_Estoque.id_produto,
                banco_Estoque.nome_produto,
                banco_Estoque.vencimento_produto,
                banco_Estoque.codigo_produto,
                banco_Estoque.controle,
                banco_Estoque.quantidade_produto.label('Total'),
                banco_Entradas.quantidade_caixa_master.label('Unidade'),
                ).join(
                    banco_Estoque,
                    banco_Entradas.id_entrada == banco_Estoque.id_entrada
                ).order_by(
                    banco_Estoque.vencimento_produto
                ).filter_by(
                    codigo_produto = codigo_produto
                ).offset(c).limit(1)

            # Faz a conversão da quantidade do produto
            quantidade_total = consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']

            if not resto:
                retirada = None

            # Para retirada da Unidade
            if consulta_ttr[0]['Unidade'] == 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']) - quantidade_unidade
                # print(f'Unidade {retirada}')

            # Para retirada de fardo
            elif consulta_ttr[0]['Unidade'] != 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total']) - (quantidade_unidade / consulta_ttr[0]['Unidade'])
                # print(f'Fardo {retirada}')

            # Campo a ser atualizado
            campo_att = conn.query(
                banco_Estoque
                ).order_by(
                banco_Estoque.vencimento_produto
                ).filter_by(
                codigo_produto = consulta_ttr[0].codigo_produto
                ).offset(c).limit(1).first()

            # A iteração dentro da tabela, não encontrou produto com quantidade, setando retirada para None
            if retirada is None:
                continue
            
            # Retirada do produto para o seguinte caso: A quantidade de saída não excede a quantide disponível por linha
            if retirada >= 0 and not resto:
                campo_att.quantidade_produto = retirada
                # print(campo_att.quantidade_produto)

                # Salva os dados
                conn.add(campo_att)
                conn.commit()
                conn.close()
                break

            # Retirada do produto para o seguinte caso: A quantidade de saída, excede a quantidade disponível por linha
            if retirada > 0 and resto:
                campo2 = conn.query(
                banco_Estoque
                ).order_by(
                banco_Estoque.vencimento_produto
                ).filter_by(
                codigo_produto = consulta_ttr[0].codigo_produto
                ).offset(c - 1).limit(1).first()

                # Seta o campo anterior (campo2) para zero e vai para a próxima linha
                campo2.quantidade_produto = 0
                
                # Salva os dados
                conn.add(campo2)
                conn.commit()
                conn.close()
            
                # Itera novamente sobre as linhas da tabela, mas nesse caso, para distribuir o resto faltante perante as demais linha
                for i in range(len(consulta)):
                    consulta_for_resto = conn.query(
                        banco_Estoque.id_produto,
                        banco_Estoque.nome_produto,
                        banco_Estoque.vencimento_produto,
                        banco_Estoque.codigo_produto,
                        banco_Estoque.controle,
                        banco_Estoque.quantidade_produto.label('Total'),
                        banco_Entradas.quantidade_caixa_master.label('Unidade'),
                        ).join(
                            banco_Estoque,
                            banco_Entradas.id_entrada == banco_Estoque.id_entrada
                        ).order_by(
                            banco_Estoque.vencimento_produto
                        ).filter_by(
                            codigo_produto = codigo_produto
                        ).offset(i).limit(1)

                    # Para retirada da unidade
                    if consulta_for_resto[0]['Unidade'] == 1 and consulta_for_resto[0]['Total'] > 0:
                        retirada = retirada * consulta_for_resto[0]['Unidade']
                        # print(f'Unidade {retirada}')
                    
                    # Para retirada de fardo
                    elif consulta_for_resto[0]['Unidade'] != 1 and consulta_for_resto[0]['Total'] > 0:
                        retirada = (retirada / consulta_for_resto[0]['Unidade'])
                        # print(f'Fardo {retirada}')

                    # Campo que será atualizado
                    campo_att_resto = conn.query(
                    banco_Estoque
                    ).order_by(
                    banco_Estoque.vencimento_produto
                    ).filter_by(
                    codigo_produto = consulta_ttr[0].codigo_produto
                    ).offset(i).limit(1).first()

                    
                    # Campo da tabela a ser atualizado (campo_att_resto), necessita ser maior que 0
                    if campo_att_resto.quantidade_produto > 0:

                        # O campo a ser atualizado (campo_att_resto) contém a quantidade necessária para abater a quantidade do produto sem sobrar resto
                        if campo_att_resto.quantidade_produto - retirada >=0:
                            campo_att_resto.quantidade_produto = campo_att_resto.quantidade_produto - retirada
                            # print(campo_att_resto.quantidade_produto)
                            
                            # Salva os dados
                            conn.add(campo_att_resto)
                            conn.commit()
                            conn.close()
                            break

                        # O campo a ser atualizado, não contém a quantidade total do produto, gerando um resto
                        elif campo_att_resto.quantidade_produto - retirada < 0:
                            retirada = campo_att_resto.quantidade_produto - retirada
                            campo_att_resto.quantidade_produto = 0

                            # Salva os dados
                            conn.add(campo_att_resto)
                            conn.commit()
                            conn.close()
                            retirada = retirada * -1
                            continue
            
            elif retirada < 0:
                retirada = retirada * consulta_ttr[0]['Unidade'] * -1
                resto = True
                continue
                
            # Encerrando a função
            break

    def atualizacao_estoque(self):
        # Matriz de dados
        consulta_items = np.array(self.filter_frame()).T        

        # Itens que serão iteráveis
        codigo_produto = consulta_items[8]        
        quantidade_produto = consulta_items[3]
        produto = consulta_items[4]
        pedido_numero = consulta_items[0]

        for produto, quantidade, nome_produto, numero_pedido in zip(
            codigo_produto, 
            quantidade_produto, 
            produto,
            pedido_numero
        ):
            consulta_join = conn.query(
                banco_Estoque.id_estoque,
                banco_Estoque.id_produto,
                banco_Produto.id_produto,
            ).join(
                banco_Produto,
                banco_Produto.id_produto == banco_Estoque.id_produto
            ).filter_by(
                codigo_produto = produto
            ).first()

            consulta = self.consulta_quantidade_estoque(produto)

            if consulta[0]["Total"] != None:                

                # Quantidade de saída em unidade
                quantidade_saida = consulta[0]['Unidade'] * quantidade

                if consulta[0]['Total'] >= quantidade_saida:
                    self.att_tabela(produto, quantidade_saida)
                    atualizacao = banco_Saida(
                        numero_pedido = numero_pedido,
                        unidade_saida = consulta[0]['Unidade'],
                        quantidade_saida = quantidade_saida,
                        id_produto = consulta_join.id_produto,
                        id_estoque = consulta_join.id_estoque
                    )    
                    conn.add(atualizacao)
                    conn.commit()
                    conn.close()
                else:
                    print('Não há quantidade suficiente em estoque')
            else:
                print('Produto %s não existe em estoque.' % nome_produto)


     


if __name__ == '__main__':
    print('Ok') 