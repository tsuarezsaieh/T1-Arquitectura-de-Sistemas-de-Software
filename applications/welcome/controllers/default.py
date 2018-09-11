# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    
    form = SQLFORM(db.mensajes)
    
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form, rows = db(db.mensajes).select())

def error():
    return dict()
