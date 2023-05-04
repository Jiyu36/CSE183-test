import uuid

from py4web import URL, Field, abort, action, redirect, request
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .common import T, auth, cache, db, session, signed_url, Field, logger, authenticated, unauthenticated, flash
from .models import get_user_email
from yatl.helpers import A
from pydal.validators import *

url_signer = URLSigner(session)

# The auth.user below forces login.
@action("index")
@action.uses("index.html", auth.user)
def index():

    #mainly from the assignment ReadMe

    rows = db(db.contact.user_email == get_user_email()).select().as_list()
    print(rows)

    for row in rows:
        #print(row)
        row["phone_number"] = ""
        s = db(db.phone.contact_id == row['id']).select()

        for r in s:
            if(row["phone_number"] != ""):
                row["phone_number"] = row["phone_number"] + ", "

            row["phone_number"] = row["phone_number"] + r['phone_number'] + " (" + r['phone_name']+") "
    #rows = db(db.contact.user_email == get_user_email()).select()

    return dict(rows = rows)

@action('add_contact', method = ["GET", "POST"])
@action.uses('add_contact.html', auth.user)
def add():

    form = Form(db.contact, 
    csrf_session=session, 
    formstyle=FormStyleBulma)       ##from rebbish2 code

    if form.accepted:
        redirect(URL("index"))

    return dict(
        add_form = form
    )


@action('edit_contact/<contact_id:int>', method=["GET", "POST"])
@action.uses('edit_contact.html', auth.user)
def edit(contact_id = None):

    assert contact_id is not None
    id = db.contact[contact_id]
    if id is None:
        redirect(URL("index"))

    form = Form(db.contact, 
    record = id, 
    deletable = False,
    csrf_session = session, 
    formstyle = FormStyleBulma)

    if form.accepted:
        redirect(URL("index"))
    
    return dict(
        edit_form = form
    )

@action('delete/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user)
def delete(contact_id = None):

    assert contact_id is not None
    #path_p = db.contact[contact_id]
    #path_p.delete_record()

    #well, delete medol may works easier and better?
    db(db.contact.id == contact_id).delete()
    redirect(URL("index"))



@action('add_phone/<contact_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses('add_phone.html', auth.user, session)
def addphone(contact_id = None):
    assert contact_id is not None

    form = Form([Field('phone'), Field('kind')], csrf_session=session,
                formstyle=FormStyleBulma)
    if form.accepted:
        db.phone.insert(
            contact_id = contact_id,
            phone_number = form.vars["phone"],
            phone_name = form.vars["kind"]
        )
        redirect(URL('edit_phones', contact_id))
        #redirect(URL("index"))   add phone page should be a child of edit phone

    user = db(
        (db.contact.user_Email == get_user_email()) & (db.contact.id == contact_id) 
    ).select().first()
    
    name = user.first_name + " " + user.last_name

    return dict(form = form, name = name)


@action('edit_phone/<contact_id:int>/<phone_id:int>', method=['GET', 'POST'])
@action.uses('edit_phone.html', auth.user)
def edit_phone(contact_id = None, phone_id = None):

    assert contact_id is not None
    assert phone_id is not None

    

    form = Form([Field('phone'), Field('kind')],
        record=dict(phone = p.phone.phone_number, kind = p.phone.phone_name),
        deletable=False,
        csrf_session=session,
        formstyle=FormStyleBulma
    )
    
    #phones = db(db.phone.customer_id==customer.id).select()

    if(form.accepted):

        db(db['phone'].id == phone_id).update(
            phone_number = form.vars['phone'],
            phone_name = form.vars['kind']
        )
        redirect(URL('edit_phone', contact_id))
    
    p=db(
        (db.phone.id == phone_id) & (db.phone.contact_id == contact_id)
    ).select().first()

    name = p.contact.first_Name + " " + p.contact.last_Name
    #print(name)

    return dict(form = form, name = name)

    #rows = db(db.phone.contact_id == contact_id).select()
    #return dict(rows=rows, contact_id=contact_id, url_signer=url_signer)


