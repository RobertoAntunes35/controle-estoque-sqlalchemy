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

    

    consulta = app.conn.query(app.banco_Estoque).order_by(app.banco_Estoque.vencimento_produto).filter_by(codigo_produto = 254).all()
    
    quantidade_unidade = 168

    # 6 estoque

    resto = False

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
        
        # Conversão para unidade de venda
        quantidade_total = consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']

        if not resto:
            # Inicio Func 
            retirada = None

            # Para retirada da unidade
            if consulta_ttr[0]['Unidade'] == 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total'] * consulta_ttr[0]['Unidade']) - quantidade_unidade
                print(f'Unidade {retirada}')
            
            # Para retirada de fardo
            elif consulta_ttr[0]['Unidade'] != 1 and consulta_ttr[0]['Total'] > 0:
                retirada = (consulta_ttr[0]['Total']) - (quantidade_unidade / consulta_ttr[0]['Unidade'])
                print(f'Fardo {retirada}')
            # Fim func RETURN retirada

            # Campo a ser atualizado
        campo_att = app.conn.query(
            app.banco_Estoque
            ).order_by(
            app.banco_Estoque.vencimento_produto
            ).filter_by(
            codigo_produto = consulta_ttr[0].codigo_produto
            ).offset(c).limit(1).first()

        if retirada is None:
            continue            

        if retirada >= 0 and not resto:
            campo_att.quantidade_produto = retirada
            print(campo_att.quantidade_produto)

            app.conn.add(campo_att)
            app.conn.commit()
            app.conn.close()
            break

        if retirada > 0 and resto:

            campo2 = app.conn.query(
            app.banco_Estoque
            ).order_by(
            app.banco_Estoque.vencimento_produto
            ).filter_by(
            codigo_produto = consulta_ttr[0].codigo_produto
            ).offset(c - 1).limit(1).first()

            print(campo2.quantidade_produto)
            campo2.quantidade_produto = 0
            print(campo2.quantidade_produto)
            
            app.conn.add(campo2)
            app.conn.commit()
            app.conn.close()



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
                # Fim func RETURN retirada



                campo_att_resto = app.conn.query(
                app.banco_Estoque
                ).order_by(
                app.banco_Estoque.vencimento_produto
                ).filter_by(
                codigo_produto = consulta_ttr[0].codigo_produto
                ).offset(i).limit(1).first()


                if campo_att_resto.quantidade_produto > 0:

                    if campo_att_resto.quantidade_produto - retirada >=0:

                        campo_att_resto.quantidade_produto = campo_att_resto.quantidade_produto - retirada
                        print(campo_att_resto.quantidade_produto)
                        app.conn.add(campo_att_resto)
                        app.conn.commit()
                        app.conn.close()
                        break

                    elif campo_att_resto.quantidade_produto - retirada < 0:
                        retirada = campo_att_resto.quantidade_produto - retirada
                        campo_att_resto.quantidade_produto = 0

                        app.conn.add(campo_att_resto)
                        app.conn.commit()
                        app.conn.close()
                        retirada = retirada * -1
                        continue
            
        elif retirada < 0:
            retirada = retirada * consulta_ttr[0]['Unidade'] * -1
            resto = True
            continue
    
        break
        


        # if resto == 0:
        #     if retirada >= 0:
        #         consulta_ttr[0].quantidade_produto = retirada

        #         app.conn.commit()
        #         app.conn.close()
                
        #         print('Quantidade ok %s' % retirada)
        #         break

        #     elif retirada < 0:
        #         resto = retirada * -1
        #         consulta_ttr[0].quantidade_produto = quantidade - resto
        #         continue 
        
        # elif resto != 0:
            
        #     if resto > 0:
        #         consulta_ttr[0].quantidade_produto = consulta_ttr[0].Total - resto
        #         app.conn.commit()
        #         app.conn.close()
        #         print('Quantidade atualizada')
        #         break  
        
        # print(consulta_ttr[0])