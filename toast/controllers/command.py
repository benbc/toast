import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from toast.lib.base import BaseController, render
from toast.app.commands import *

log = logging.getLogger(__name__)

class CommandController(BaseController):
    def add_book(self):
        command = AddBookCommand(request.params['name'], request.params['author'])
        log.debug(command)
        config['toast.application'].send(command)
        redirect(url(controller='view'))

    def add_recipe(self):
        book = int(request.params['book'])
        command = AddRecipeCommand(book, request.params['title'])
        log.debug(command)
        config['toast.application'].send(command)
        redirect(url(controller='view', action='book', id=book))
