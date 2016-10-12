from werkzeug.routing import BaseConverter
import env_global

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

class AppDelegate():
    __slot__ = {
        'app'
        'global_work_path'
    }
    def __init__(self, app=None):

        self.app = app
        self.app.config.from_object('config')
        self.app.config.from_envvar('APP_CONFIG_FILE')
        env_global.WORK_PATH = app.config['WORK_PATH']
        self.app.url_map.converters['regex'] = RegexConverter


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
        def main():
            return self.app.send_static_file('index.html')

        @self.app.route('/<path:path>')
        def static_file(path):
            return self.app.send_static_file(path)


