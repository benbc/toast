from pyramid.config import Configurator
from toast.app.application import build_application

def main(global_config, **settings):
    application, database = build_application()
    settings['toast.application'] = application
    settings['toast.database'] = database

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static')
    config.add_route('index', '/')
    config.add_route('book', '/book/{id}')
    config.add_route('add_book', '/add_book')
    config.add_route('add_recipe', '/add_recipe')
    config.scan()

    return config.make_wsgi_app()
