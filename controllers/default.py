# -*- coding: utf-8 -*- 

largura_grid = '700'

def index():
    if auth.is_logged_in():
        message = auth.has_membership(auth.id_group('usuario'))
        return dict(message=message)
    else:
        return dict(message='Benvindo!')

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if len(request.args) > 0:
        if request.args[0] == 'profile':
            response.subtitle = 'Editar perfil de %s' % auth.user.first_name
        elif request.args[0] == 'change_password':
            response.subtitle = 'Trocar Senha'
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    #session.forget()
    return service()

def data():
    return dict(form=crud())
    
@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def parceiro():
    response.subtitle = 'Parceiro'
    form = crud.create(db.parceiro)
    grid = plugin_jqgrid(db.parceiro,width=largura_grid)  
    return dict(form=form,grid=grid)

def editar_parceiro():
    response.subtitle = 'Editar Parceiro'
    response.view = 'simple_form.html'
    form = crud.update(db.parceiro,request.args(0),next=URL(r=request,c='default',f='parceiro')) 
    return dict(title='Editar Parceiro',form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def contato():
    response.subtitle = 'Contato'
    response.view = 'todos_novo.html'
    form = crud.create(db.contato)
    grid = plugin_jqgrid(db.contato,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_contato():
    response.subtitle = 'Editar Contato'
    response.view = 'simple_form.html'
    form = crud.update(db.contato,request.args(0),next=URL(r=request,c='default',f='contato')) 
    return dict(title='Editar Contato',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def grupo():
    response.subtitle = 'Grupo'
    response.view = 'todos_novo.html'
    form = crud.create(db.grupo)
    grid = plugin_jqgrid(db.grupo,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_grupo():
    response.subtitle = 'Editar Grupo'
    response.view = 'simple_form.html'
    form = crud.update(db.grupo,request.args(0),next=URL(r=request,c='default',f='grupo')) 
    return dict(title='Editar Grupo',form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def participacao():
    response.subtitle = 'Participação'
    response.view = 'todos_novo.html'
    form = crud.create(db.participacao)
    grid = plugin_jqgrid(db.participacao,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def editar_participacao():
    response.subtitle = 'Editar Participação'
    response.view = 'simple_form.html'
    form = crud.update(db.participacao,request.args(0),next=URL(r=request,c='default',f='participacao')) 
    return dict(title='Editar Agrupamento',form=form)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def log():
    response.subtitle = 'Log'
    response.view = 'todos_novo.html'
    form = crud.create(db.log)
    grid = plugin_jqgrid(db.log,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def usuario():
    response.subtitle = 'Usuários'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_user)
    grid = plugin_jqgrid(db.auth_user,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def auth_group():
    response.subtitle = 'Grupos'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_group)
    grid = plugin_jqgrid(db.auth_group,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def auth_membership():
    response.subtitle = 'Papéis'
    response.view = 'todos_novo.html'
    form = crud.create(db.auth_membership)
    grid = plugin_jqgrid(db.auth_membership,width=largura_grid)  
    return dict(form=form,grid=grid) 

#
# Fluxo de Caixa

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def movimento_caixa():
    response.subtitle = 'Entrada/Saída do Caixa'
    response.view = 'todos_novo.html'
    form = crud.create(db.caixa)
    grid = plugin_jqgrid(db.caixa,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento():
    response.subtitle = 'Editar Entrada/Saída'
    response.view = 'simple_form.html'
    form = crud.update(db.caixa,request.args(0),next=URL(r=request,c='default',f='entrada')) 
    return dict(form=form)


def transferencia():
    response.subtitle = 'Transferência entre Contas'
    form = SQLFORM.factory(Field('montante','decimal',requires=IS_NOT_EMPTY()),
                           Field('conta_origem',db.conta,requires=IS_IN_DB(db,'conta.id','%(nome)s')),
                           Field('conta_destino',db.conta,requires=IS_IN_DB(db,'conta.id','%(nome)s')),
                           Field('obs','string')
                           )
    if form.accepts(request.vars,session):
        db.caixa.insert(conta=request.vars.conta_destino,
                          valor=request.vars.montante,
                          movimento='Entrada',
                          documento='Trans: %s' % request.vars.obs)
        db.caixa.insert(conta=request.vars.conta_origem,
                        valor=request.vars.montante,
                        movimento='Saída',
                        documento='Trans: %s' % request.vars.obs)
        response.flash = 'Transferência efetuada com sucesso.'
    elif form.errors:
        response.flash = 'Há erros no formulário.'
    response.view = 'simple_form.html'
    return dict(form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def conta():
    response.subtitle = 'Conta (plano de contas)'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta)
    grid = plugin_jqgrid(db.conta,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta():
    response.subtitle = 'Editar Conta'
    response.view = 'simple_form.html'
    form = crud.update(db.banco,request.args(0),next=URL(r=request,c='default',f='conta')) 
    return dict(title='Editar Conta',form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def categoria_entrada_saida():
    response.subtitle = 'Categoria de Entrada e Saída'
    response.view = 'todos_novo.html'
    form = crud.create(db.categoria_entrada_saida)
    grid = plugin_jqgrid(db.categoria_entrada_saida,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_categoria_entrada_saida():
    response.subtitle = 'Editar Categoria de Entradas e Saídas'
    response.view = 'simple_form.html'
    form = crud.update(db.categoria_entrada_saida,request.args(0),next=URL(r=request,c='default',f='categoria_entrada_saida')) 
    return dict(title='Editar Categorias de Entrada e Saída',form=form)

def tipo_documento():
    response.subtitle = 'Tipo Documento'
    response.view = 'todos_novo.html'
    form = crud.create(db.tipo_documento)
    grid = plugin_jqgrid(db.tipo_documento,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_tipo_documento():
    response.subtitle = 'Editar Tipo de Documento'
    response.view = 'simple_form.html'
    form = crud.update(db.tipo_documento,request.args(0),next=URL(r=request,c='default',f='tipo_documento')) 
    return dict(title='Editar Tipo de Documento',form=form)

def conta_a_pagar():
    response.subtitle = 'Conta a Pagar'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta_a_pagar)
    grid = plugin_jqgrid(db.conta_a_pagar,width=largura_grid)
    db.conta_a_pagar.paga.writable=False  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta_a_pagar():
    response.subtitle = 'Editar Conta a Pagar'
    response.view = 'simple_form.html'
    form = crud.update(db.conta_a_pagar,request.args(0),next=URL(r=request,c='default',f='conta_a_pagar')) 
    return dict(title='Editar Conta a Pagar',form=form)

def conta_a_receber():
    response.subtitle = 'Conta a Receber'
    response.view = 'todos_novo.html'
    form = crud.create(db.conta_a_receber)
    grid = plugin_jqgrid(db.conta_a_receber,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_conta_a_receber():
    response.subtitle = 'Editar Conta a Receber'
    response.view = 'simple_form.html'
    form = crud.update(db.conta_a_receber,request.args(0),next=URL(r=request,c='default',f='conta_a_receber')) 
    return dict(title='Editar Conta a Receber',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def pagar_conta():
    response.subtitle = 'Pagar Conta (baixa)'
    if request.args:
        conta = crud.read(db.conta_a_pagar,request.args[0])
        form = SQLFORM.factory(
                               Field('valor_pago','decimal',default=db.conta_a_pagar[request.args[0]].valor),
                               Field('data_pagamento','date',default=request.now),
                               Field('pagar_com',db.conta,requires=IS_IN_DB(db,'conta.id','%(nome)s')))
        if form.accepts(request.vars,session):
            db(db.conta_a_pagar.id==request.args[0]).update(paga=True,
                                                            data_pagamento=request.vars.data_pagamento,
                                                            valor=request.valor)
            db.caixa.insert(conta=request.vars.pagar_com,
                            documento=db.conta_a_pagar[request.args[0]].id,
                            valor=request.vars.valor_pago,
                            movimento='Saída',
                            data=request.vars.data_pagamento)
            session.flash = 'A conta foi paga!'
            return redirect(URL(r=request,args=[]))
        elif form.errors:
            response.flash = 'Há erros no formulário.'
            
    else:
        conta = 'Selecione um conta para pagar:'
        form = ''
    grid = plugin_jqgrid(db.conta_a_pagar,'paga',False)
    return dict(conta=conta,form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def receber_conta():
    response.subtitle = 'Receber Conta (baixa)'
    if request.args:
        conta = crud.read(db.conta_a_receber,request.args[0])
        form = SQLFORM.factory(
                               Field('valor_recebido','decimal',default=db.conta_a_receber[request.args[0]].valor),
                               Field('data_recebimento','date',default=request.now),
                               Field('receber_em',db.conta,requires=IS_IN_DB(db,'conta.id','%(nome)s')))
        if form.accepts(request.vars,session):
            db(db.conta_a_receber.id==request.args[0]).update(recebida=True,
                                                              data_recebimento=request.vars.data_recebimento,
                                                              valor=request.vars.valor)
            db.caixa.insert(conta=request.vars.receber_em,
                            documento=db.conta_a_receber[request.args[0]].id,
                            valor=request.vars.valor_recebido,
                            data=request.vars.data_recebimento)
            session.flash = 'Conta recebida!'
            return redirect(URL(r=request,args=[])) 
        elif form.errors:
            response.flash = 'Há erros no formulário.'
    else:
        conta = 'Selecione um conta para receber:'
        form = ''
    grid = plugin_jqgrid(db.conta_a_receber,'recebida',False)
    return dict(conta=conta,form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def banco():
    response.subtitle = 'Banco'
    response.view = 'todos_novo.html'
    form = crud.create(db.banco)
    grid = plugin_jqgrid(db.banco,width=largura_grid)  
    return dict(form=form,grid=grid)

def editar_banco():
    response.subtitle = 'Editar Banco'
    response.view = 'simple_form.html'
    form = crud.update(db.banco,request.args(0),next=URL(r=request,c='default',f='banco')) 
    return dict(title='Editar Banco',form=form)


@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def item_almoxarifado():
    response.subtitle = 'Item do Almoxarifado'
    response.view = 'todos_novo.html'
    form = crud.create(db.item_almoxarifado)
    grid = plugin_jqgrid(db.item_almoxarifado,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_item_almoxarifado():
    response.subtitle = 'Editar Item do Almoxarifado'
    response.view = 'simple_form.html'
    form = crud.update(db.item_almoxarifado,request.args(0),next=URL(r=request,c='default',f='item_almoxarifado')) 
    return dict(title='Editar Item do Almoxarifado',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def movimento_almoxarifado():
    response.subtitle = 'Movimento do Almoxarifado'
    response.view = 'todos_novo.html'
    form = crud.create(db.movimento_almoxarifado)
    grid = plugin_jqgrid(db.movimento_almoxarifado,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento_almoxarifado():
    response.subtitle = 'Editar Movimento do Almoxarifado'
    response.view = 'simple_form.html'
    form = crud.update(db.movimento_almoxarifado,request.args(0),next=URL(r=request,c='default',f='movimento_almoxarifado')) 
    return dict(title='Editar Almoxarifado',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def produto():
    response.subtitle = 'Produto'
    response.view = 'todos_novo.html'
    response.subtitle = 'Produto'
    form = crud.create(db.produto)
    grid = plugin_jqgrid(db.produto,width=largura_grid,col_width=200)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_produto():
    response.subtitle = 'Editar Produto'
    id = request.args(0)
    form = crud.update(db.produto,id,next=URL(r=request,c='default',f='produto'))
    entradas = db((db.movimento_estoque.produto==id) &
                      (db.movimento_estoque.movimento=='Entrada') ).select(db.movimento_estoque.quantidade.sum())
    entradas_soma = 0
    if entradas[0]._extra[db.movimento_estoque.quantidade.sum()]:
        entradas_soma = entradas[0]._extra[db.movimento_estoque.quantidade.sum()]
    saidas = db((db.movimento_estoque.produto==id) &
                      (db.movimento_estoque.movimento=='Saída') ).select(db.movimento_estoque.quantidade.sum())
    saidas_soma = 0
    if saidas[0]._extra[db.movimento_estoque.quantidade.sum()]:
        saidas_soma = saidas[0]._extra[db.movimento_estoque.quantidade.sum()]
    total_estoque = entradas_soma - saidas_soma 
    return dict(title='Editar Produto',form=form,total_estoque=total_estoque)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def movimento_estoque():
    response.subtitle = 'Movimento de Estoque'
    response.view = 'todos_novo.html'
    form = crud.create(db.movimento_estoque)
    grid = plugin_jqgrid(db.movimento_estoque,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_movimento_estoque():
    response.subtitle = 'Editar Movimento de Estoque'
    response.view = 'simple_form.html'
    form = crud.update(db.movimento_estoque,request.args(0),next=URL(r=request,c='default',f='movimento_estoque')) 
    return dict(title='Editar Estoque',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )

def unidade():
    response.subtitle = 'Unidade'
    response.view = 'todos_novo.html'
    form = crud.create(db.unidade)
    grid = plugin_jqgrid(db.unidade,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_unidade():
    response.subtitle = 'Editar Unidade'
    response.view = 'simple_form.html'
    form = crud.update(db.unidade,request.args(0),next=URL(r=request,c='default',f='unidade')) 
    return dict(title='Editar Unidade',form=form)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or 
               auth.has_membership(auth.id_group('operador')) or
               is_master()
               )
def funcionario():
    response.subtitle = 'Fucionário'
    response.view = 'todos_novo.html'
    form = crud.create(db.funcionario)
    grid = plugin_jqgrid(db.funcionario,width=largura_grid)  
    return dict(form=form,grid=grid)

@auth.requires(auth.has_membership(auth.id_group('usuario')) or
               is_master()
               )
def editar_funcionario():
    response.subtitle = 'Editar Funcionário'
    response.view = 'simple_form.html'
    form = crud.update(db.funcionario,request.args(0),next=URL(r=request,c='default',f='funcionario')) 
    return dict(title='Editar Funcionário',form=form)


# relatórios

def rel_fluxo_caixa():
    
    response.subtitle = 'Relatório Fluxo de Caixa'
    form = SQLFORM.factory(Field('data_ini','date',label='Data inicial',
                                 requires=IS_DATE(format='%d/%m/%y', error_message='use o formato 31/12/1981')),
                           Field('data_fim','date',label='Data final', 
                                 requires=IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')))
    if form.accepts(request.vars,session):
        import time
        data_ini = time.strptime(request.vars.data_ini,'%d/%m/%Y' )
        data_fim = time.strptime(request.vars.data_fim,'%d/%m/%Y' )
        fluxo = db((db.caixa.data>=data_ini) &
                   (db.caixa.data<=data_fim)).select()
        return dict(form=form, fluxo=fluxo)
    else:
        return dict(form=form,fluxo='Informe as datas limites')

def saldo():
    response.subtitle = 'Saldos'
    contas = db(db.conta.id>0).select()
    saldos = []
    for conta in contas:
            entradas = db((db.caixa.conta==conta.id) and (db.caixa.movimento=='Entrada')).select(db.caixa.valor.sum())
            if entradas[0]._extra[db.caixa.valor.sum()]:
                entradas_soma = entradas[0]._extra[db.caixa.valor.sum()]
            else:
                entradas_soma = 0
            saidas = db((db.caixa.conta==conta.id) and (db.caixa.movimento=='Saída')).select(db.caixa.valor.sum())
            if saidas[0]._extra[db.caixa.valor.sum()]:
                saidas_soma = saidas[0]._extra[db.caixa.valor.sum()]
            else:
                saidas_soma = 0
            saldos.append([conta.nome,entradas_soma - saidas_soma])
    return dict(saldos=saldos)