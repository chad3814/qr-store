# -*- coding: utf-8 -*-
"""Setup the qr-store application"""
from __future__ import print_function, unicode_literals
import transaction
from qrstore import model


def bootstrap(command, conf, vars):
    """Place any commands to setup qrstore here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'chad3814'
        u.display_name = 'Chad Walker'
        u.email_address = 'chad@cwalker.dev'
        u.password = 'password'

        model.DBSession.add(u)
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
