from flask import render_template

class AppDelegate():
    __slot__ = {
        'app'
    }
    def __init__(self, app=None):
        self.app = app

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
            return render_template('index.html')


