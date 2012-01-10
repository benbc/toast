from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
