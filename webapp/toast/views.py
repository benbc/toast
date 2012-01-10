from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import logging
from toast.app.commands import AddBookCommand, AddRecipeCommand

log = logging.getLogger(__name__)

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    database = request.registry.settings['toast.database']
    return {'books': database.books(), 'authors': database.authors()}

@view_config(route_name='book', renderer='templates/book.jinja2')
def book(request):
    database = request.registry.settings['toast.database']
    id = request.matchdict['id']
    book = database.book(int(id))
    return {'book': book}

@view_config(route_name='add_book')
def add_book(request):
    command = AddBookCommand(request.params['name'], request.params['author'])
    log.debug(command)
    application = request.registry.settings['toast.application']
    application.send(command)
    return HTTPFound(request.route_path('index'))

@view_config(route_name='add_recipe')
def add_recipe(request):
    book = int(request.params['book'])
    command = AddRecipeCommand(book, request.params['title'])
    log.debug(command)
    application = request.registry.settings['toast.application']
    application.send(command)
    return HTTPFound(request.route_path('book', id=book))
