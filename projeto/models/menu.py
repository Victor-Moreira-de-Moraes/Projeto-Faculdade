# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu += [
    (T('Home'), False, URL('default', 'index')),
    (T('Nova Transação'), False, URL('default', 'nova_transacao')),
    (T('Ver Transações'), False, URL('default', 'ver_transacao'))
]
