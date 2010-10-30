import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from toast.lib.base import BaseController, render

log = logging.getLogger(__name__)

class CommandController(BaseController):
    def add_line(self):
        log.debug(request.params['line'])

        redirect(url(controller='view'))
