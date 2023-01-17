from sqlalchemy import create_engine
from libs.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Acesso ao bd
conn = Session()

Base = declarative_base()

class Fornecedores(Base):
    __tablename__ = 'fornecedores'

    codigo_fornecedor = Column(Integer, nullable = False, primary_key= True, autoincrement= True)
    nome_fornecedor = Column(String(150), nullable = False)
    comissao_fornecedor = Column(Float, nullable = False)
    cnpj_fornecedor = Column(String(50), nullable = False)

    def __repr__(self):
        return f'Fornecedor: {self.nome_fornecedor}'

class Produtos(Base):
    __tablename__ = 'produtos'

    id_produto = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    codigo_produto = Column(Integer, nullable = False)
    nome_produto = Column(String(100), nullable = False)
    unidade_produto = Column(String(45), nullable = False)
    controle_produto = Column(Boolean, nullable = False)
    grupo_produto = Column(String(100), nullable = False)
    comissao_produto = Column(Float, nullable = False)

    # Foreign Key
    codigo_fornecedor = Column(Integer, nullable = False) 

    def __repr__(self):
        return f'Produto: {self.nome_produto}'

class Entradas(Base):
    __tablename__ ='entradas'

    id_entrada = Column(Integer, nullable = False, primary_key = True,autoincrement = True)
    unidade_entrada = Column(String(45), nullable=False)
    quantidade_entrada = Column(Integer, nullable=False)
    quantidade_caixa_master = Column(Integer, nullable = False)
    data_entrada = Column(DateTime, nullable=False)
    lote_entrada = Column(String(45), nullable=False)
    vencimento_produto = Column(DateTime, nullable=False)

    # Foreign Key
    id_produto = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Fornecedor: {self.id_entrada}'

class Estoque(Base):
    __tablename__ = 'estoque'

    id_estoque = Column(Integer, nullable = False, primary_key = True, autoincrement = True)
    codigo_produto = Column(Integer, nullable = False)
    nome_produto = Column(String(100), nullable = False)
    unidade_produto = Column(String(45), nullable = False)
    quantidade_produto = Column(Integer, nullable = False)
    data_entrada = Column(DateTime, nullable = False)
    lote_entrada = Column(String(45), nullable = False)
    vencimento_produto = Column(DateTime, nullable = False)

    # Foreign Key
    id_entrada = Column(Integer, nullable = False)
    id_produto = Column(Integer, nullable = False)

    def __repr__(self):
        return f'Produto: {self.nome_produto} | Vencimento: {self.vencimento_produto} | Quantidade {self.quantidade_produto}'

class Saida(Base):
    __tablename__ = 'saida'

    id_saida = Column(Integer, nullable = False, primary_key = True, autoincrement=True)
    unidade_saida = Column(String(45), nullable = False)
    quantidade_saida = Column(Integer, nullable = False)
    
    # Foreign Key
    id_produto = Column(Integer, nullable = False)
    id_estoque = Column(Integer, nullable = False)

    def __repr__(self):
        return f'ID_produto: {self.id_produto} | Quantidade Saída: {self.quantidade_saida} '