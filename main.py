from libs import app


if __name__ == '__main__':

    columns_produtos = \
        {
        'D04_cod':'Codigo Produto', 
        'D04_Descricao':'Nome Produto',
        'D04_UniPro':'Unidade',
        'Controle':'Controle',
        'xgrupo':'Grupo',
        'Comissao':'Comissao',
        'Combinação47':'Codigo Fornecedor'
       }

    columns_fornecedor = \
        {
            'D01_Cod_Cliente':'Codigo Fornecedor',
            'D01_Fantasia':'Nome Fornecedor',
            'D01_CNPJ':'Cnpj Fornecedor'
        }

    produtos = app.Produtos(nome_arquivo = 'D04_Produto_Completo.xls', **columns_produtos)
    fornecedores = app.Fornecedores(nome_arquivo = 'D08_Fornecedor.xls', **columns_fornecedor) 

    # Instânciar o Objeto
    entrada = app.Entradas()

    # Encontrar o produto
    entrada.buscar_produto(codigo_produto=255)
    
    # Definir a quantidade
    entrada.quantidade_entrada()    
    
    # Converter data de vencimento de str para datetime
    data_vencimento = '2026-10-01'
    entrada.conversao_data(data_vencimento=data_vencimento)

    # Definir o Lote
    entrada.lote_entrada('20261001ABX')

    # Realizar a entrada
    entrada()