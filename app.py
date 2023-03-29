import datetime
import os
import auth
import db
import script_doi_extract as DOI_SEARCH
from flask import Flask, render_template, jsonify, request


def create_app(test_config=None):
    # create and configure the app
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
        heure_actuelle = datetime.datetime.now().time()
        return render_template(
            'home.html',
            app=app,
            tnow=heure_actuelle.strftime("%H:%M")
        )

    @app.route('/clt')
    def clinical_trial_page():
        trials = db.get_trial()
        women = db.get_total_esais_fem()
        men = db.get_total_esais_male()
        allg = db.get_total_essais()
        return render_template(
            'clinicaltrials.html',
            app=app,
            trials=trials,
            women=women,
            men=men,
            allg=allg
        )

    @app.route('/doi-search')
    def doi_search():
        return render_template(
            'doi-search.html',
            app=app
        )

    @app.route('/import')
    def import_page():
        return 0  # render_template('import_data.html', app=app)

    @app.route('/pub')
    def publications_page():
        toto_obs = db.get_total_pub_essais_rand()
        toto_rand = db.get_total_pub_essais_obs()
        publications = db.get_publication()
        return render_template(
            'publications.html',
            app=app,
            publications=publications,
            total_rand=toto_rand,
            total_obs=toto_obs
        )

    # Request GET
    @app.route('/chart-nb-phase')
    def ma_liste():
        return jsonify(db.get_phase_by_nb())

    @app.route('/doi-get-data')
    def doi_res():
        # Récupérer les données de l'API CrossRef
        param = str(request.args.get('q'))
        result = DOI_SEARCH.get_doi(param)
        return jsonify(result)

    @app.route('/stats')
    def stats():
        tnow = datetime.datetime.now().time()
        return render_template('statistics.html', app=app, tnow=tnow.strftime("%H:%M"))


    # Les fonctions doivent être déclarées avant ce bloc #
    db.init_app(app)
    app.register_blueprint(auth.bp)
    return app





