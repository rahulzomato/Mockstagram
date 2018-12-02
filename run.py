import click
from configs import settings as Settings
from mockstagram_webapp.src import app as mswebapp
from gevent.pywsgi import WSGIServer



@click.group()
def cli():
    pass

@cli.command('webapp', help='run mockstagram webapp')
@click.option('--port', default=Settings.WEBAPP_SERVICE_PORT)
@click.option('--debug', default=Settings.DEBUG)
@click.option('--with_gevent', default=False)
def mockstagram_webapp(port, debug, with_gevent):
	click.echo('starting webapp on {0} with debug {1}'.format(port, debug))
	if with_gevent:
		http_server = WSGIServer(('0.0.0.0', port), mswebapp)
		http_server.serve_forever()
	else:
		mswebapp.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == '__main__':
    cli()