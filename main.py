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

    columns_saidas = \
        {
            'Numero':'Numero Pedido',
            'Combinação22':'Codigo Vendedor',
            'DATA':'Data Entrega',
            'QUANT':'Quantidade',
            'Texto28':'Nome Produto',
            'Vl_Prod':'Valor Custo',
            'Texto37':'Unidade',
            'Combinacação42':'Natureza Operacao',
            'Texto66':'Cidade',
            'Texto68':'Codigo Produto',
            'Texto73':'Valor Venda',
            'Combinação47':'Nome Fornecedor',
            'Texto14':'Nome Cliente',
            'CODCLI':'Codigo Cliente',
            'xvencimento':'Metodo de Pagamento'
        }

    produtos = app.Produtos(nome_arquivo = 'D04_Produto_Completo.xls', **columns_produtos)
    fornecedores = app.Fornecedores(nome_arquivo = 'D08_Fornecedor.xls', **columns_fornecedor) 
    entrada = app.Entradas()
    saidas = app.Saida(nome_arquivo= 'Pedidos_Itens.xls', **columns_saidas)

    # Instânciar o Objeto

    # Encontrar o produto
    # entrada.buscar_produto(codigo_produto=130)
    
    # Definir a quantidade
    # entrada.quantidade_entrada()    
    
    # Definir a quantidade da caixa
    # entrada.quantidade_caixa_master()

    # Converter data de vencimento de str para datetime
    # data_vencimento = '2023-02-01'
    # entrada.conversao_data(data_vencimento=data_vencimento)

    # Definir o Lote
    # entrada.lote_entrada('20261001ABX')

    # Realizar a entrada
    # entrada()

    # Reliazar Saída
    # saidas.produto_em_estoque(254)

    
    # consulta_join = app.conn.query(
    #     app.banco_Entradas.id_produto,
    #     app.func.sum(app.banco_Entradas.quantidade_entrada*app.banco_Entradas.quantidade_caixa_master).label("Total"),
    #     app.banco_Produto.nome_produto
    #     ).join(
    #         app.banco_Produto,
    #         app.banco_Produto.id_produto == app.banco_Entradas.id_produto
    #     ).filter_by(
    #         codigo_produto = 10
    #     ).all()
    # if consulta_join[0].Total != None:
    #     print('consulta_join[0].Total')
    
    # print(saidas.consulta_estoque(1))
    
    saidas.consulta_existencia()
