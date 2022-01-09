import pandas as pd
from pymed import PubMed
from flask import Flask, render_template, redirect
from flask.helpers import url_for
from flask_session import Session
from flask import *
import os
import subprocess
import time
import signal
import re
from test import GetAllFiles
import secrets


app = Flask(__name__)

sesh = Session()


driver_files = os.listdir('files/Driver')

gene_files = os.listdir('files/Genes')

gene_drug_files = os.listdir(r'networks/Gene-Drug')

prot_prot_files = os.listdir(r'networks/Protein-Protein')


def make_token():
    return secrets.token_urlsafe(4)


@app.route('/')
def index():
    return redirect(url_for('landing'))


@app.route('/landing')
def landing():
    return render_template('new.index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/browser')
def browser():
    return render_template('browser.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/downloads')
def downloads():
    return render_template(
        'downloads.html',
        driverFiles=driver_files,
        geneFiles=gene_files,
        heading=['Driver genes for cancer type', 'Genes for cancer type'])


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/sample_cyto.js')
def new():
    with open('static/js/ample_cyto.js') as f:
        response = app.response_class(response=f.readlines(),
                                      status=200,
                                      mimetype='text/html')
    return response


@app.route('/networks/<path:jsName>', methods=['GET', 'POST'])
def network_viz(jsName):
    #jsName = jsName.replace("/", "\\")
    with open(f'networks/{jsName}.js') as f:
        response = app.response_class(response=f.readlines(),
                                      status=200,
                                      mimetype='application/json')
    return response


@app.route('/data/<path:filename>')
def download(filename):
    """check which files are requested based on anchor tag in html"""
    if not 'driver' in filename:
        app.config['UPLOAD_FOLDER'] = 'files/Genes'
        dir = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        print(dir)
        return send_from_directory(dir, path=filename)
    if 'driver' in filename:
        app.config['UPLOAD_FOLDER'] = 'files/Driver'
        dir = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        print(dir)
        return send_from_directory(dir, path=filename)


@app.route('/canceromics/download/<path:filename>')
def download_canceromics_data(filename):
    #filename = filename.replace("/", "\\")
    return send_file(fr'{filename}')


@app.route('/testing/<path:csv_name>', methods=['GET', 'POST'])
def test(csv_name):
    with open(f'{csv_name}') as f:
        response = app.response_class(response=f.readlines(),
                                      status=200,
                                      mimetype='application/csv')
    return response


# autoplotter routing and process management ------------- START


@app.route('/autoplotter')
def get_autoplotter():
    return render_template('autoplotter.html')


# @app.route('/autoplotter_view/<path:csv_name>')
# def view_autoplotter(csv_name):
#     return render_template('autoplotter_view.html', csv_name)


@app.route('/eda/killall', methods=['GET'])
def kill_processes():
    try:
        os.kill((apltr_process.pid), signal.SIGTERM)
        return redirect(url_for('landing'))
    except NameError:
        pass


def kill_and_launch(filename: str):
    global apltr_process
    try:
        os.kill((apltr_process.pid), signal.SIGTERM)
        print('script killed')
        print('script execution initiated')
        apltr_process = subprocess.Popen(
            ['python', r'autoplotter_app.py', filename],
            shell=False,
        )
        time.sleep(5)
        return 'http://127.0.0.1:5100/'
    except NameError:
        apltr_process = subprocess.Popen(
            ['python', r'autoplotter_app.py', filename],
            shell=False,
        )
        time.sleep(5)
        return 'http://127.0.0.1:5100/'


@app.route('/eda/ext-webapp/<path:filename>', methods=['GET'])
def autoplotter(filename):
    redirection = kill_and_launch(filename)
    return redirect(redirection)

    # return render_template('test.html', csv = filename)


# autoplotter routing and process management ------------- END

# Text mining routing and process management ------------- START


def create_csv(query: str):
    pubmed = PubMed(tool="test", email="a@a.com")
    search_term = query
    search = search_term.split()
    for i in search:
        results = pubmed.query(i, max_results=10)
        articleList = []
        articleInfo = []

        for article in results:
            # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
            # We need to convert it to dictionary with available function
            articleDict = article.toDict()
            articleList.append(articleDict)

        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        for article in articleList:
            # Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
            pubmedId = article['pubmed_id'].partition('\n')[0]
            # Append article info to dictionary
            articleInfo.append({
                u'Pubmed_id': pubmedId,
                u'Title': article['title'],
                u'Abstract': article['abstract'],
                u'Publication_date': article['publication_date'],
                u'doi': article['doi'],
                u'Authors': article['authors']
            })

    # Generate Pandas DataFrame from list of dictionaries
    articlesPD = pd.DataFrame.from_dict(articleInfo)

    csv_name = f'{search_term}_results.csv'

    export_csv = articlesPD.to_csv(fr'pubmed\{csv_name}',
                                   index=None,
                                   header=True)

    try:
        for file in os.listdir("pubmed_text_mining"):
            os.remove(file)
    except:
        pass

    from data_extraction import DataExtraction

    DataExtraction.run(rf'{csv_name}')

    return csv_name


@app.route('/textmining')
def get_textmining():
    return render_template('text_mining.html')


@app.route('/textmining/result')
def text_mining_result():
    query = request.args.get('query')
    result = create_csv(query)
    return render_template('test.html',
                           csv_name=result,
                           extraction=os.listdir("pubmed_text_mining"))


@app.route('/textmining/show/<path:filename>')
def show_result(filename):
    with open(fr'pubmed\{filename}', encoding='utf-8') as f:
        response = app.response_class(response=f.readlines(),
                                      status=200,
                                      mimetype='application/csv')
    return response


@app.route('/textmining/download/<path:filename>')
def download_textmining_result(filename):
    app.config['UPLOAD_FOLDER'] = 'pubmed'
    dir = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(dir, path=filename)


@app.route('/dataextraction/download/<path:filename>')
def download_data_extraction_result(filename):
    app.config['UPLOAD_FOLDER'] = 'pubmed_text_mining'
    dir = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(dir, path=filename)


@app.route('/canceromics/<path:filename>')
def load_files(filename):
    parent = f'canceromics/{filename}'
    FileDispatch = GetAllFiles()
    FileTree = FileDispatch.getFiles(f'canceromics/{filename}')
    return jsonify(FileTree)


# @app.route('/cytoscape/network/<path:folder>')
# def render_network(folder):
#     """render index.html from different cytoscape files """
#     app.config['NETWORK'] = rf"networks\Gene-Drug\{folder}"
#     return app.send_static_file(rf"{app.config['NETWORK']}\index.html")
#     # return send_file(rf"networks\Gene-Drug\{folder}\index.html")


@app.route('/cytoscape/network/<path:file>')
def render_network(file):
    """render index.html from different cytoscape files """
    app.config['NETWORK'] = 'networks/Gene-Drug'
    dir = os.path.join(current_app.root_path, app.config['NETWORK'])
    return send_from_directory(dir, path=file)


@app.route('/cytoscape/network/prot-prot/<path:file>')
def render_network_prot(file):
    """render index.html from different cytoscape files """
    app.config['NETWORK'] = 'networks\\Protein-Protein'
    dir = os.path.join(current_app.root_path, app.config['NETWORK'])
    return send_from_directory(dir, path=file)


@app.route('/plotly')
def show_plot():
    import pubmed_ml.plotly_test as pt
    from kmeans_fdist import PlotDispatch
    plots = PlotDispatch(
        r'E:\MIT\OncoOmics_portal\pubmed\medicinal database_results.csv')

    elbow = plots.plot_elbow()
    pca = plots.clustering_and_pca()
    text = plots.impl_word_cloud()
    wrdcld = plots.get_wordcloud(text)
    # freqdist = plots.frequency_dist()

    # return render_template('plots.html', elbow=elbow, clustering=pca, freq=freqdist, wrd=wrdcld)
    return render_template('plots.html',
                           elbow=elbow,
                           clustering=pca,
                           wrd=wrdcld)


@app.route('/ML')
def ML():
    return render_template('ML.html')


@app.route('/ML/run', methods=['GET', 'POST'])
def upload_file():
    app.config['UPLOAD_FOLDER'] = r'ML'

    if request.method == 'POST':
        print('running file upload')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        session['file'] = file.filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        target_col = request.form['radio-part']

        # from ML.papermill_implementation import run_classification, run_regression

        if request.form['radio-method'] == 'R':
            # run_regression(session.get('file'), target_col)
            return render_template('Regression_output.html')
        elif request.form['radio-method'] == 'C':
            # run_classification(session.get('file'), target_col)
            return render_template('Classification_output.html')
        else:
            return render_template('ML.html', error='Please check input and resubmit')
    else:
        return render_template('ML.html', error='Something went wrong')


@app.route('/docking')
def docking():
    return render_template('docking_upload.html')


@app.route('/pdbs/<filename>')
def get_pdb(filename):
    return send_file(rf'docking/{filename}')


@app.route('/ligand/<filename>')
def get_ligand(filename):
    return send_file(rf'docking/{filename}')


@app.route('/dockingFileUpload', methods=['GET', 'POST'])
def upload_docking_files():
    app.config['DOCKING_UPLOAD'] = 'docking'

    prot_file = request.files['proteinFile']
    lig_file = request.files['ligandFile']

    session['_id'] = '2'

    if prot_file.filename.endswith('.pdbqt') and lig_file.filename.endswith('.pdbqt') or lig_file.filename.endswith('.sdf'):

        lig_filename = session.get('_id') + '@' + lig_file.filename
        prot_filename = session.get('_id') + '@' + prot_file.filename

        prot_file.save(os.path.join(
            app.config['DOCKING_UPLOAD'], prot_filename))

        lig_file.save(os.path.join(
            app.config['DOCKING_UPLOAD'], lig_filename))

        return render_template('docking.html', lig_filename=lig_filename, prot_filename=prot_filename)

    else:
        return render_template('new.docking.html', error='Could not upload files. check file type.'
                               )


@app.route('/getCenters/<filename>')
def get_center(filename):
    pdb_file = open(
        rf'docking/{filename}').readlines()
    pdb = {'Record name': [],
           'Atom number': [],
           'Atom name': [],
           'AltLoc': [],
           'ResName': [],
           'ChainID': [],
           'ResSeq': [],
           'AChar': [],
           'X': [],
           'Y': [],
           'Z': [],
           'Occupancy': [],
           'Temperature factor': [],
           'Segment identifier': [],
           'Element symbol': [],
           'Charge': []
           }
    for line in pdb_file:
        if re.match('^ATOM', line):
            pdb['Record name'].append(line[0:5])
            pdb['Atom number'].append(line[5:11])
            pdb['Atom name'].append(line[12:16])
            pdb['AltLoc'].append(line[16])
            pdb['ResName'].append(line[17:20])
            pdb['ChainID'].append(line[21])
            pdb['ResSeq'].append(line[22:26])
            pdb['AChar'].append(line[26])
            pdb['X'].append(line[30:38])
            pdb['Y'].append(line[38:46])
            pdb['Z'].append(line[46:54])
            pdb['Occupancy'].append(line[54:60])
            pdb['Temperature factor'].append(line[60:66])
            pdb['Segment identifier'].append(line[72:76])
            pdb['Element symbol'].append(line[76:78])
            pdb['Charge'].append(line[78:80])
    pdb_df = pd.DataFrame(pdb,
                          columns=['Record name', 'Atom number', 'Atom name', 'AltLoc', 'ResName', 'ChainID', 'ResSeq', 'X', 'Y',
                                   'Z', 'Occupancy', 'Temperature factor', 'Segment identifier', 'Element symbol', 'Charge']).set_index('Atom number')
    pdb_df[['X', 'Y', 'Z', ]] = pdb_df[['X', 'Y', 'Z', ]].apply(pd.to_numeric)
    pdb_df['ResSeq'] = pdb_df['ResSeq'].apply(pd.to_numeric)
    x_size = pdb_df.X.max() - pdb_df.X.min()
    y_size = pdb_df.Y.max() - pdb_df.Y.min()
    z_size = pdb_df.Z.max() - pdb_df.Z.min()

    return jsonify(
        [pdb_df.X.max() - x_size / 2,
         pdb_df.Y.max() - y_size / 2,
         pdb_df.Z.max() - z_size / 2
         ])


@app.route('/runVina', methods=['GET', 'POST'])
def run_vina():
    from vina_implementation import RunVina
    receptor = request.args.get('receptor')
    ligand = request.args.get('ligand')
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    print(f'value of z - {z}')
    exh = request.args.get('e')
    sx = request.args.get('w')
    sy = request.args.get('h')
    sz = request.args.get('d')
    output_file = ligand.split('.')[0] + 'output.pdbqt'
    result = RunVina(receptor, ligand, x, y, z, exh, sx, sy, sz, output_file)
    result = result.run_process()
    return render_template('docking_result.html', result=result[0].decode(), error=result[1].decode(), output=output_file)


@app.route('/sendVinaOutput/<filename>')
def send_output(filename):
    dir = os.path.join(current_app.root_path, r'docking')
    return send_from_directory(dir, filename)


@app.route('/cheminformatics')
def cheminfo():
    dir = os.path.join(current_app.root_path, r'Cheminformatics/outputs')
    outputs = os.listdir(dir)
    return render_template('cheminfo_descriptor.html', outputs=outputs)


@app.route('/cheminfo_outputs/<file>')
def cheminfo_outputs(file):
    dir = os.path.join(current_app.root_path, r'Cheminformatics/outputs')
    return send_from_directory(dir, file)


@app.route('/cheminformatics/rdkit')
def render_chem_out():
    return render_template('Chemoinformatics_RDKit_SMILES_Molecule.html')


if __name__ == '__main__':

    app.secret_key = 'aljhsjehkjkawjnenlalc'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    sesh.init_app(app)
    app.run(host='0.0.0.0', port=8080)
