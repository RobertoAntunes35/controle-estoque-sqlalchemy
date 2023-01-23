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

    print(saidas.consulta_quantidade_estoque(254))


    # # Instânciar o Objeto

    # # Encontrar o produto
    # entrada.buscar_produto(codigo_produto=254)
    
    # # Definir a quantidade
    # entrada.quantidade_entrada()    
    
    # # Definir a quantidade da caixa
    # entrada.quantidade_caixa_master()

    # # Converter data de vencimento de str para datetime
    # data_vencimento = '2023-12-01'
    # entrada.conversao_data(data_vencimento=data_vencimento)

    # # Definir o Lote
    # entrada.lote_entrada('20261001ABX')

    # # Realizar a entrada
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

    

    

'''
    # Consulta atráves do código do produto nesse caso 254 e pega todos os registros da tabela. 
    consulta = app.conn.query(app.banco_Estoque).order_by(app.banco_Estoque.vencimento_produto).filter_by(codigo_produto = 254).all()
    

    # Quantidade em unidade que irá sair.
    quantidade_unidade = 168

    resto = False

    # Itera sobre todas as linhas encontradas para o produto procurado, sendo nesse caso, o 254.
    for c in range(len(consulta)):
        consulta_ttr = app.conn.query(
            app.banco_Estoque.id_produto,
            app.banco_Estoque.nome_produto,
            app.banco_Estoque.vencimento_produto,
            app.banco_Estoque.codigo_produto,
            app.banco_Estoque.controle,
            app.banco_Estoque.quantidade_produto.label('Total'),
            app.banco_Entradas.quantidade_caixa_master.label('Unidade'),
            ).join(
                app.banco_Estoque,
                app.banco_Entradas.id_entrada == app.banco_Estoque.id_entrada
            ).order_by(
                app.banco_Estoque.vencimento_produto
            ).filter_by(
                codigo_produto = 254
            ).offset(c).limit(1)
        
        # Faz a conversão da quantidade do produto
        quantidade_total = consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']

        if not resto:

            retirada = None

            # Para retirada da unidade
            if consulta_ttr[0]['Unidade'] == 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']) - quantidade_unidade
                print(f'Unidade {retirada}')
            
            # Para retirada de fardo
            elif consulta_ttr[0]['Unidade'] != 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total']) - (quantidade_unidade / consulta_ttr[0]['Unidade'])
                print(f'Fardo {retirada}')

        # Campo a ser atualizado
        campo_att = app.conn.query(
            app.banco_Estoque
            ).order_by(
            app.banco_Estoque.vencimento_produto
            ).filter_by(
            codigo_produto = consulta_ttr[0].codigo_produto
            ).offset(c).limit(1).first()

        # A iteração dentro da tabela, não encontrou produto com quantidade, setando retirada para None
        if retirada is None:
            continue            

        # Retirada do produto para o seguinte caso: 
        # A quantidade de saída não excede a quantide disponível por linha
        if retirada >= 0 and not resto:
            campo_att.quantidade_produto = retirada
            print(campo_att.quantidade_produto)

            # Salva os dados
            app.conn.add(campo_att)
            app.conn.commit()
            app.conn.close()
            break

        # Retirada do produto para o seguinte caso: 
        # A quantidade de saída, excede a quantidade disponível por linha
        if retirada > 0 and resto:
            campo2 = app.conn.query(
            app.banco_Estoque
            ).order_by(
            app.banco_Estoque.vencimento_produto
            ).filter_by(
            codigo_produto = consulta_ttr[0].codigo_produto
            ).offset(c - 1).limit(1).first()

            # Seta o campo anterior (campo2) para zero e vai para a próxima linha
            campo2.quantidade_produto = 0
            
            # Salva os dados
            app.conn.add(campo2)
            app.conn.commit()
            app.conn.close()


            # Itera novamente sobre as linhas da tabela, 
            # mas nesse caso, para distribuir o resto faltante 
            # perante as demais linha
            for i in range(len(consulta)):
                consulta_for_resto = app.conn.query(
                    app.banco_Estoque.id_produto,
                    app.banco_Estoque.nome_produto,
                    app.banco_Estoque.vencimento_produto,
                    app.banco_Estoque.codigo_produto,
                    app.banco_Estoque.controle,
                    app.banco_Estoque.quantidade_produto.label('Total'),
                    app.banco_Entradas.quantidade_caixa_master.label('Unidade'),
                    ).join(
                        app.banco_Estoque,
                        app.banco_Entradas.id_entrada == app.banco_Estoque.id_entrada
                    ).order_by(
                        app.banco_Estoque.vencimento_produto
                    ).filter_by(
                        codigo_produto = 254
                    ).offset(i).limit(1)

                # Para retirada da unidade
                if consulta_for_resto[0]['Unidade'] == 1 and consulta_for_resto[0]['Total'] > 0:
                    retirada = retirada * consulta_for_resto[0]['Unidade']
                    print(f'Unidade {retirada}')
                
                # Para retirada de fardo
                elif consulta_for_resto[0]['Unidade'] != 1 and consulta_for_resto[0]['Total'] > 0:
                    retirada = (retirada / consulta_for_resto[0]['Unidade'])
                    print(f'Fardo {retirada}')

                # Campo que será atualizado
                campo_att_resto = app.conn.query(
                app.banco_Estoque
                ).order_by(
                app.banco_Estoque.vencimento_produto
                ).filter_by(
                codigo_produto = consulta_ttr[0].codigo_produto
                ).offset(i).limit(1).first()

                
                # Campo da tabela a ser atualizado (campo_att_resto), necessita ser maior que 0
                if campo_att_resto.quantidade_produto > 0:

                    # O campo a ser atualizado (campo_att_resto) contém a
                    # quantidade necessária para abater a quantidade do produto sem sobrar resto
                    if campo_att_resto.quantidade_produto - retirada >=0:
                        campo_att_resto.quantidade_produto = campo_att_resto.quantidade_produto - retirada
                        print(campo_att_resto.quantidade_produto)
                        
                        # Salva os dados
                        app.conn.add(campo_att_resto)
                        app.conn.commit()
                        app.conn.close()
                        break

                    # O campo a ser atualizado, não contém 
                    # a quantidade total do produto, gerando um resto
                    elif campo_att_resto.quantidade_produto - retirada < 0:
                        retirada = campo_att_resto.quantidade_produto - retirada
                        campo_att_resto.quantidade_produto = 0

                        # Salva os dados
                        app.conn.add(campo_att_resto)
                        app.conn.commit()
                        app.conn.close()
                        retirada = retirada * -1
                        continue
            
        elif retirada < 0:
            retirada = retirada * consulta_ttr[0]['Unidade'] * -1
            resto = True
            continue
            
        # Encerrando a função
        break

'''
