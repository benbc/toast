import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from toast.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ViewController(BaseController):
    def index(self):
        database = config['toast.database']
        c.books = database.books()
        c.authors = database.authors()
        return render('/index.jinja')
