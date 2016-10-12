from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

class AppDelegate():
    __slot__ = {
        'app'
    }
    def __init__(self, app=None):
        self.app = app
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


