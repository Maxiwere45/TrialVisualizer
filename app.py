import datetime
import os
import db
import auth
import script_doi_extract as DOI_SEARCH
from flask import Flask, render_template, jsonify, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    app.config['MONGO_URI'] = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'
    app.config['MONGO_DBNAME'] = 'infos'

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

    # a simple page that says hello
    @app.route('/')
    def index():
        trials = db.get_trial()
        heure_actuelle = datetime.datetime.now().time()
        return render_template(
            'home.html',
            app=app,
            tnow=heure_actuelle.strftime("%H:%M"),
            trials=trials,
            publications=db.get_publication()
        )

    @app.route('/clt')
    def clinical_trial_page():
        trials = db.get_trial()
        return render_template(
            'clinicaltrials.html',
            app=app,
            trials=trials
        )

    @app.route('/doi-search')
    def doi_search():
        return render_template(
            'doi-search.html',
            app=app
        )

    @app.route('/pub')
    def publications_page():
        publications = db.get_publication()
        return render_template(
            'publications.html',
            app=app,
            publications=publications
        )

    # Request GET
    @app.route('/chart-nb-phase')
    def ma_liste():
        return jsonify(db.get_phase())

    @app.route('/doi-get-data')
    def doi_res():
        # Récupérer les données de l'API CrossRef
        param = str(request.args.get('q'))
        result = DOI_SEARCH.get_doi(param)
        return jsonify(result)

    db.init_app(app)
    app.register_blueprint(auth.bp)

    return app
