# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- index page ----
def index():
    response.flash = T("Hello!!!")
    return dict(message=T('Welcome!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


@auth.requires_login()
def nova_transacao():
    form = SQLFORM(Transacao)
    if form.process().accepted:
        session.flash = 'Nova transação feita com sucesso! %s' % form.vars.titulo
        redirect(URL('nova_transacao'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def ver_transacao():
    grid = SQLFORM.grid(db.transacao.auth_user_id == auth.user_id,
                        fields=[db.transacao.data_transacao, db.transacao.tipo, db.transacao.tipo_conta,
                                db.transacao.nome_transacao, db.transacao.resumo, db.transacao.valor])
    return dict(grid=grid)


@auth.requires_login()
def editar_transacao():
    form = SQLFORM(Transacao, request.args(0, cast=int),  showid=False)
    if form.process().accepted:
        session.flash = 'Transação atualizado: %s' % form.vars.nome_transacao
        redirect(URL('ver_transacao'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def apagar_transacao():
    db(Transacao.id==request.args(0, cast=int)).delete()
    session.flash = 'Transação apagada!'
    redirect(URL('ver_transacao'))
