import datetime
import import_csv as impcsv
import os
import auth
import db
import script_doi_extract as DOI_SEARCH
from flask import Flask, render_template, jsonify, request
from flask import request
import pandas as pd


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
        return render_template('import_data.html', app=app)

    @app.route('/import-data', methods=['POST'])
    def import_data():
        # Récupérer le fichier CSV envoyé via le formulaire
        file_csv = request.files['file']

        # Recupérer le type sélectionné dans le formulaire
        type_data = request.form['select-type']

        # Vérifier que le fichier est bien un CSV
        if not file_csv.filename.endswith('.csv'):
            return 'Le fichier n\'est pas un CSV !'

        res = impcsv.traitement_CSV_IMPORT(type_data, file_csv.stream)
        return res

    @app.route('/pub')
    def publications_page():
        return render_template(
            'publications.html',
            app=app,
            publications=db.get_publication(),
            total_rand=db.get_total_pub_essais_obs(),
            total_obs=db.get_total_pub_essais_rand(),
            total_pub=db.get_total_pub()
        )

    # Request GET
    @app.route('/chart-nb-phase')
    def get_nb_phase():
        return jsonify(db.get_phase_by_nb())

    @app.route('/doi-get-data')
    def doi_res():
        # Récupérer les données de l'API CrossRef
        param = str(request.args.get('q'))
        result = DOI_SEARCH.get_doi(param)
        return jsonify(result)

    @app.route('/stats_pub')
    def stats_pub():
        toto_art = db.get_total_articles()
        toto_preprint = db.get_total_preprints()
        return render_template(
            'stat_publications.html',
            app=app,
            toto_art=toto_art,
            toto_preprint=toto_preprint,
            get_top_concept=db.get_top_concepts_by_publication_count()
        )

    @app.route('/stats_clt')
    def stats_clt():
        return render_template('stat_clinical_trial.html', app=app)

    ## STATISTIQUES ESSAIS CLINIQUES
    @app.route('/statcltgender')
    def get_stat_clt_gender():
        return jsonify(db.get_gender_stats())

    # Les fonctions doivent être déclarées avant ce bloc
    db.init_app(app)
    app.register_blueprint(auth.bp)
    return app
