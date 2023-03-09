# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context, abort
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from qrstore import model
from qrstore.controllers.secure import SecureController
from qrstore.model import DBSession

from qrstore.utils.git_sha import GitSha
from qrstore.lib.base import BaseController
from qrstore.controllers.error import ErrorController
from qrstore.model.container import Container

from uuid import uuid4
import qrcode
import io

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the qr-store application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "QR-Store"
        tmpl_context.git_sha = GitSha()[0:6]

    @expose('qrstore.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    @expose('qrstore.templates.container')
    def container(self, uuid):
        cont = DBSession.query(Container).filter_by(uuid=uuid).one()
        return dict(container=cont)
    @expose(content_type='image/png')
    def qrcode(self, uuid):
        # from sqlalchemy.exc import InvalidRequestError
        # try:
        #     cont = DBSession.query(Container).filter_by(uuid=uuid).one()
        # except InvalidRequestError:
        #     raise abort(404)
        bytes_arr = io.BytesIO()
        qrcode.make('http://127.0.0.1:8080/container/' + uuid).get_image().save(bytes_arr, format='PNG')     
        return bytes_arr.getvalue()

    @expose('qrstore.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
