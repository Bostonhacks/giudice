import os

from flask import Flask, jsonify, render_template
from giudice.projects import process_csv, assign_tables_to_judges


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Login page & home page
    @app.route('/')
    def login():
        return "Login"

    # JSON response for projects endpoint
    @app.route('/projects')
    def projects():
        projects = process_csv()
        return jsonify(projects)

    @app.route('/judging')
    def judging():
        assignments = assign_tables_to_judges()
        return render_template('judge-home.html', assignments=assignments)

    @app.route('/judging/scoring')
    def scoring():
        assignments = assign_tables_to_judges()
        return render_template('judge-judging.html', assignments=assignments)

    return app