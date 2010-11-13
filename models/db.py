# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################
#from gluon.tools import PluginManager
#plugins = PluginManager
#plugins.plugin_jqgrid.theme = 'ui-lightness' 

request.env.http_accept_language='pt-br' 

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    #db = DAL('mysql://yamac872_princip:pm4ch1n3@localhost/yamac872_atelie')

## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='yawehyireh'

# definir tabela de usuÃ¡rio customizada
auth_table = db.define_table(
  auth.settings.table_user_name,
  Field('first_name', length=128, default='',label='Nome'),
  Field('last_name', length=128, default='',label='Sobrenome'),
  Field('email', length=128, default='', unique=True,label='Email'),
  Field('password', 'password', length=256,
   readable=False, label='Senha'),
   Field('registration_key', length=128, default= '',
   writable=False, readable=False))

auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
auth_table.password.requires = CRYPT()
auth_table.email.requires = [
   IS_EMAIL(error_message=auth.messages.invalid_email),
   IS_NOT_IN_DB(db, auth_table.email)]
auth.settings.table_user = auth_table

auth.define_tables()                         # creates all needed tables
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc



# crud.settings.auth=auth                      # enforces authorization on crud
#mail=Mail()                                  # mailer
#mail.settings.server='smtp.gmail.com:587'    # your SMTP server
#mail.settings.server='127.0.0.1:587'
#mail.settings.sender='admin@ya-machine.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
#mail.settings.login=None
#auth.settings.mailer=mail                    # for user email verification
#auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
#auth.messages.verify_email = 'Clique no link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s para verificarmos seu email.'
#auth.settings.reset_password_requires_verification = True
#auth.messages.reset_password = 'Clique no link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s para refazer sua senha.'
## more options discussed in gluon/tools.py
#########################################################################

response.title = 'Principal'
response.subtitle = ' '

# funções auxiliares
def rep_sim_nao(value):
    if value:
        return 'Sim'
    else:
        return 'Não'
    
def is_master():
  if auth.is_logged_in():
    return auth.user.id == 1
  else:
    return False

def moeda(valor):
    return 'R$ %0.2f' % valor


db.define_table('parceiro',
                Field('razao_social','string',required=True),
                Field('nome','string'),
                Field('cnpj','string'),
                Field('cpf','string'),
                Field('endereco','string'),
                Field('numero','string'),
                Field('uf','string'),
                Field('cidade','string'),
                Field('e_cliente','boolean',default=False),
                Field('e_fornecedor','boolean',default=False),
                Field('fundacao','integer'))
db.parceiro.id.represent = lambda id: SPAN(A('%i editar'%id,_href=URL(r=request,c="default",f="editar_parceiro",args=id)))

db.define_table('funcionario',
                Field('usuario',db.auth_user),
                Field('nome','string'),
                Field('cpf','string'),
                Field('endereco','string'),
                Field('numero','string'),
                Field('uf','string'),
                Field('cidade','string'),
                Field('salario_atual','decimal(10,2)'),
                Field('vencimento_salario','integer'),
                Field('cargo','string'))
db.funcionario.usuario.requires = IS_NULL_OR(IS_IN_DB(db,'auth_user.id','%(first_name)s'))
db.funcionario.usuario.represent = lambda value: db.auth_user[value].first_name
db.funcionario.vencimento_salario.requires = IS_INT_IN_RANGE(1,31)
db.funcionario.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_funcionario",args=id))) 


db.define_table('contato',
                Field('nome','string',required=True),
                Field('cargo','string'),
                Field('celular','string',required=True),
                Field('email','string'),
                Field('endereco','string',label='Endereço'),
                Field('numero','string'),
                Field('cidade','string'),
                Field('uf','string'),
                Field('empresa',db.parceiro))
db.contato.nome.requires = IS_NOT_EMPTY()
db.contato.email.requires = IS_NULL_OR(IS_EMAIL())
db.contato.empresa.requires = IS_NULL_OR(IS_IN_DB(db,'parceiro.id','%(razao_social)s'))
db.contato.empresa.represent = lambda value: ('',db.parceiro[value].razao_social)[value]
db.contato.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_contato",args=id)))


db.define_table('grupo',
                Field('nome','string',required=True),
                Field('observacao','text',label='Observação'))
db.grupo.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_grupo",args=id)))

# chamado de agrupamento na interface 
db.define_table('participacao',
                Field('contato',db.contato),
                Field('grupo',db.grupo))
db.participacao.grupo.requires = IS_IN_DB(db,'grupo.id','%(nome)s')
db.participacao.grupo.represent = lambda value: db.grupo[value].nome         
db.participacao.contato.requires = IS_IN_DB(db,'contato.id','%(nome)s')
db.participacao.contato.represent = lambda value: db.contato[value].nome 
db.participacao.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_participacao",args=id)))

db.define_table('log',
               Field('acao','string'),
               Field('data','datetime'),
               Field('usuario',db.auth_user))
db.log.usuario.requires = IS_IN_DB(db,'user.id','%(first_name)')

#
# Fluxo de Caixa
#

# Conta
db.define_table('banco',
                Field('nome','string',required=True),
                Field('agencia','string',label='Agência'),
                Field('cidade','string'),
                Field('uf','string')
                )
db.banco.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_banco",args=id)))

db.define_table('conta',
                Field('nome','string',required=True),
                Field('numero','string'),
                Field('banco',db.banco),
                Field('obs','text'),
                )
db.conta.nome.requires = IS_NOT_EMPTY()
db.conta.banco.requires = IS_IN_DB(db,'banco.id','%(nome)s')
db.conta.banco.represent = lambda value: db.banco[value].nome 
db.conta.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_conta",args=id)))


# Tipo de documento: boleto, cheque, espécie, etc.
db.define_table('tipo_documento',
                Field('nome','string'),
                )
db.tipo_documento.requires = IS_NOT_EMPTY()
db.tipo_documento.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_tipo_documento",args=id)))

# Categorias de despesas ou 
db.define_table('categoria_entrada_saida',
                Field('nome','string',required=True),
                Field('entrada_saida','string',label='Entrada/Saída')
                )            
db.categoria_entrada_saida.nome.requires = IS_NOT_EMPTY()
db.categoria_entrada_saida.entrada_saida.requires = IS_IN_SET(['Entrada','Saída'])
db.categoria_entrada_saida.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_categoria_entrada_saida",args=id)))

db.define_table('conta_a_pagar',
                Field('fornecedor',db.parceiro),
                Field('valor','double',default=0),
                Field('vencimento','date'),
                Field('tipo_documento',db.tipo_documento,label='Tipo Doc.'),
                Field('data_pagamento','date',label='Data do Pagamento',writable=False,readable=False),
                Field('paga','boolean',default=False,writable=False),
                Field('categoria',db.categoria_entrada_saida),
                Field('descricao','text',label='Descrição'),
                )
db.conta_a_pagar.fornecedor.requires = IS_IN_DB(db(db.parceiro.e_fornecedor=='True'),'parceiro.id','%(razao_social)s')
db.conta_a_pagar.fornecedor.represent = lambda value: db.parceiro[value].razao_social
db.conta_a_pagar.valor.requires = IS_NOT_EMPTY()
db.conta_a_pagar.tipo_documento.requires = IS_IN_DB(db,'tipo_documento.id','%(nome)s')
db.conta_a_pagar.tipo_documento.represent = lambda value: db.tipo_documento[value].nome
db.conta_a_pagar.paga.represent = rep_sim_nao
db.conta_a_pagar.categoria.requires = IS_IN_DB(db(db.categoria_entrada_saida.entrada_saida=='Saída'),'categoria_entrada_saida.id','%(nome)s')
db.conta_a_pagar.categoria.represent = lambda value: db.categoria_entrada_saida[value].nome 
db.conta_a_pagar.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_conta_a_pagar",args=id)),
                                                A(' pagar',_href=URL(r=request,c="default",f="pagar_conta",args=id))) 

db.define_table('conta_a_receber',
                Field('cliente',db.parceiro),
                Field('valor','double',default=0),
                Field('vencimento','date'),
                Field('tipo_documento',db.tipo_documento,label='Tipo Doc.'),
                Field('data_recebimento','date',label='Data do Recebimento',readable=False,writable=False),
                Field('recebida','boolean',default=False,writable=False),
                Field('categoria',db.categoria_entrada_saida),
                Field('descricao','text',label='Descrição'),
                )
db.conta_a_receber.cliente.requires = IS_IN_DB(db(db.parceiro.e_cliente==True),'parceiro.id','%(razao_social)s')
db.conta_a_receber.cliente.represent = lambda value: db.parceiro[value].razao_social
db.conta_a_receber.valor.requires = IS_NOT_EMPTY()
db.conta_a_receber.tipo_documento.requires = IS_IN_DB(db,'tipo_documento.id','%(nome)s')
db.conta_a_receber.tipo_documento.represent = lambda value: db.tipo_documento[value].nome
db.conta_a_receber.recebida.represent = rep_sim_nao
db.conta_a_receber.categoria.requires = IS_IN_DB(db(db.categoria_entrada_saida.entrada_saida=='Entrada'),'categoria_entrada_saida.id','%(nome)s')
db.conta_a_receber.categoria.represent = lambda value: db.categoria_entrada_saida[value].nome
db.conta_a_receber.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_conta_a_receber",args=id)),
                                                  A(' receber',_href=URL(r=request,c="default",f="pagar_conta",args=id)))

db.define_table('caixa',
                Field('conta',db.conta),
                Field('data','date',label='Data Venc.'),
                Field('documento','string',label='Número Doc.',default=0),
                Field('movimento','string',),
                Field('valor','double',default=0),
                )
db.caixa.conta.requires = IS_IN_DB(db,'conta.id','%(nome)s')
db.caixa.conta.represent = lambda value: db.conta[value].nome
db.caixa.data.requires = IS_DATE(format='%d/%m/%Y', error_message='use o formato 31/12/1981')
db.caixa.movimento.requires = IS_IN_SET(['Entrada','Saída'])
db.caixa.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_saida",args=id)))

db.define_table('unidade',
                Field('sigla','string',required=True),
                Field('descricao','string'))
db.unidade.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_unidade",args=id)))

db.define_table('item_almoxarifado',
                Field('descricao',label='Descriação',required=True),
                Field('unidade',db.unidade)
                )
db.item_almoxarifado.unidade.requires = IS_IN_DB(db,'unidade.id','%(sigla)s')
db.item_almoxarifado.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_item_almoxarifado",args=id)))

db.define_table('movimento_almoxarifado',
                Field('item',db.item_almoxarifado),
                Field('quantidade','integer'),
                Field('movimento','string'),
                Field('data','date',default=request.now,writable=False),
                Field('marca','string')
                )
db.movimento_almoxarifado.item.requires = IS_IN_DB(db,'item_almoxarifado.id','%(descricao)s')
db.movimento_almoxarifado.item.represent = lambda value: db.item_almoxarifado[value].descricao 
db.movimento_almoxarifado.movimento.requires = IS_IN_SET(['Entrada','Saída'])
db.movimento_almoxarifado.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_almoxarifado",args=id)))

db.define_table('produto',
                Field('descricao','string'),
                Field('unidade',db.unidade),
                Field('descontinuado','boolean',default=False),
                Field('fornecedor',db.parceiro)
                )
db.produto.unidade.requires = IS_IN_DB(db,'unidade.id','%(sigla)s')
db.produto.descontinuado.represent = rep_sim_nao
db.produto.fornecedor.requires = IS_IN_DB(db(db.parceiro.e_fornecedor==True),'parceiro.id','%(razao_social)s')
db.produto.fornecedor.represent = lambda value: db.parceiro[value].razao_social 
db.produto.id.represent = lambda id: SPAN(A('%i editar'%id,_href=URL(r=request,c="default",f="editar_produto",args=id)))


db.define_table('movimento_estoque',
                Field('produto',db.produto),
                Field('quantidade','integer'),
                Field('data','date',default=request.now,writable=False),
                Field('movimento','string'),
                Field('preco','decimal(10,2)',label='Preço unitário',default=0),
                Field('marca','string'))
#class TotalVirtual:
#        def valor_total(self):
#            return self.movimento_estoque.quantidade*self.movimento_estoque.preco
#db.movimento_estoque.virtualfields.append(TotalVirtual())
db.movimento_estoque.produto.requires = IS_IN_DB(db(db.produto.descontinuado==False),
                                                 'produto.id','%(descricao)s')
db.movimento_estoque.movimento.requires = IS_IN_SET(['Entrada','Saída'])
db.movimento_estoque.id.represent = lambda id: SPAN(A('editar',_href=URL(r=request,c="default",f="editar_movimento_estoque",args=id)))


