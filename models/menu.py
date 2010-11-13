# -*- coding: utf-8 -*- 

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    [T('Home'), False, 
     URL(request.application,'default','index'), []],
    ]

if not auth.is_logged_in():
  response.menu = [
           ['Login', False, None,  
            [
                   [T('Entrar'), False,
                    auth.settings.login_url],
                   [T('Perdi minha senha'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
           ]
else:
  response.menu = [
            ['Login',False,None,
             [
                    [T('Sair'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Editar Perfil'), False, 
                     URL(request.application,'default','user/profile')],
                    [T('Senha'), False,
                     URL(request.application,'default','user/change_password')]]
             ],
            ]

if auth.is_logged_in():
  # O primeiro usuário cadastrado é tido como o usuário master
  if auth.user.id==1:
    response.menu.append(['Admin',False,None,
                          [
                           ['Log',False,URL(r=request,c='default',f='log'),[]],
                           ['Usuários',False,URL(r=request,c='default',f='usuario'),[]],
                           ['Funções',False,URL(r=request,c='default',f='auth_group'),[]],
                           ['Função',False,URL(r=request,c='default',f='auth_membership'),[]],
                          ]
                        ])
  response.menu.append(['Relacionamentos',False,None,
                             [
                              ['Parceiros de Negócio',False,URL(r=request,c='default',f='parceiro'),[]],
                              ['Contatos',False,URL(r=request,c='default',f='contato'),[]],
                              ['Grupos',False,URL(r=request,c='default',f='grupo'),[]],
                              ['Agrupamento',False,URL(r=request,c='default',f='participacao'),[]]
                             ]
                            ])
  response.menu.append(['Caixa',False,None,
                             [
                              ['Entradas/Saídas',False,URL(r=request,c='default',f='movimento_caixa'),[]],
                              ['Transferência',False,URL(r=request,c='default',f='transferencia'),[]],
                              ['Plano de Contas',False,'',[
                                ['Planos',False,URL(r=request,c='default',f='conta'),[]],
                                ['Bancos',False,URL(r=request,c='default',f='banco'),[]],
                                                                                  ]],
                             ['Relatórios',False,'',[
                                ['Saldos',False,URL(r=request,c='default',f='saldo'),[]],
                                ['Fluxo',False,URL(r=request,c='default',f='rel_fluxo_caixa'),[]],
                                                                                  ]],
                             ]
                            ])
  response.menu.append(['Contas',False,None,
                             [
                              ['A Receber',False,URL(r=request,c='default',f='conta_a_receber'),[]],
                              ['A Pagar',False,URL(r=request,c='default',f='conta_a_pagar'),[]],
                              ['Pagar Conta',False,URL(r=request,c='default',f='pagar_conta'),[]],
                              ['Receber Conta',False,URL(r=request,c='default',f='receber_conta'),[]],
                              ['Categorias',False,URL(r=request,c='default',f='categoria_entrada_saida'),[]],
                              ['Tipos de Documentos',False,URL(r=request,c='default',f='tipo_documento'),[]],
                             ]
                            ])
  response.menu.append(['Almoxarifado',False,None,
                             [
                              ['Itens',False,URL(r=request,c='default',f='item_almoxarifado'),[]],
                              ['Movimento',False,URL(r=request,c='default',f='movimento_almoxarifado'),[]],
                             ]
                            ])
  response.menu.append(['Estoque',False,None,
                             [
                              ['Produtos',False,URL(r=request,c='default',f='produto'),[]],
                              ['Movimento',False,URL(r=request,c='default',f='movimento_estoque'),[]],
                              ['Unidades',False,URL(r=request,c='default',f='unidade'),[]],
                             ]])
  response.menu.append(['Pessoal',False,None,
                             [
                              ['Funcionários',False,URL(r=request,c='default',f='funcionario'),[]],
                             ]
                            ])
