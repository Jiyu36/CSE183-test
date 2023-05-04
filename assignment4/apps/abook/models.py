"""
This file defines the database models
"""
import datetime

from pydal.validators import *

from .common import Field, auth, db


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

db.define_table(
    'contact',
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email, requires=IS_NOT_EMPTY(), writeable = False, readable = False)
)

db.define_table(
    'phone',
    Field('contact_id', 'reference contact'),
    Field('phone_number'),
    Field('phone_name'),
)

db.contact.id.readable = db.contact.id.writable = False
db.phone.contact_id.readable = db.phone.contact_id.writable = False


db.commit()
