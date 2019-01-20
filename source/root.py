"""Root."""
import gzip
import functools
from cStringIO import StringIO as IO
from werkzeug.routing import BaseConverter
from flask import after_this_request, request
from generate_blog_articles import generate


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


class GlobalValue(object):
    def __getattr__(self, item):
        return app_global.config[item]


app_global = None
global_value = GlobalValue()


def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                    response.status_code >= 300 or
                    'Content-Encoding' in response.headers):
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func

class AppDelegate():
    __slot__ = {
            'app'
            'global_work_path'
            }
    def __init__(self, app=None):
        global app_global
        app_global = app

        self.app = app
        self.app.config.from_object('config')
        self.app.config.from_pyfile('./instance/config.py')
        self.app.config.from_envvar('APP_CONFIG_FILE')
        self.app.url_map.converters['regex'] = RegexConverter

        # generate article list
        generate()

    def register(self):
        """
        blueprint
        """
        from inter import main
        self.app.register_blueprint(main)

        """
        normal route
        """

        @self.app.route('/')
        @gzipped
        def main():
            return self.app.send_static_file('index.html')

        @self.app.route('/<path:path>')
        @gzipped
        def static_file(path):
            return self.app.send_static_file(path)

        @self.app.route('/static/js/<path>')
        @gzipped
        def jsFile(path):
            return self.app.send_static_file('static/js/'+path)

        @self.app.route('/static/css/<path>')
        @gzipped
        def cssFile(path):
            return self.app.send_static_file('static/css/'+path)

        @self.app.route('/static/media/<path>')
        @gzipped
        def mediaFile(path):
            return self.app.send_static_file('static/media/'+path)



