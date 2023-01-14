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
    entrada = app.Entradas()

    # Instânciar o Objeto

    # Encontrar o produto
    # entrada.buscar_produto(codigo_produto=15)
    
    # # Definir a quantidade
    # entrada.quantidade_entrada()    
    
    # # Converter data de vencimento de str para datetime
    # data_vencimento = '2026-10-01'
    # entrada.conversao_data(data_vencimento=data_vencimento)

    # # Definir o Lote
    # entrada.lote_entrada('20261001ABX')

    # # Realizar a entrada
    # entrada()

    # Reliazar Saída
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
    saidas = app.Saida('Pedidos_Itens.xls', **columns_saidas)


    join_entrada_produto = app.conn.query(
                    app.banco_Entradas.id_entrada,
                    app.banco_Produto.codigo_produto,
                    app.banco_Produto.nome_produto,
                    app.banco_Produto.id_produto
                ).join(
                    app.banco_Produto,
                    app.banco_Produto.id_produto == app.banco_Entradas.id_produto
                ).filter_by(id_produto = 21).all()


    for consulta in join_entrada_produto:
        print(consulta)
        