import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from toast.lib.base import BaseController, render
from toast.app.commands import AddLineCommand

log = logging.getLogger(__name__)

class CommandController(BaseController):
    def add_line(self):
        command = AddLineCommand(request.params['line'])
        log.debug(command)
        redirect(url(controller='view'))
