import flask
app = flask.Flask(
                __name__,
                static_url_path='', 
                static_folder='../studio_app/static/',
                template_folder='../studio_app/templates/'
                )
