import backend.WikiGraph as wg
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, flash
from flask_caching import Cache
import time
import os

WORKING_DIR = os.environ['WIKIRACE_WORKING_DIR']
ALLTITLESPATH = os.environ['WIKIRACE_ALLTITLESPATH']
GRAPHPATH = os.environ['WIKIRACE_GRAPHPATH']
WIKIPEDIA_URL = "https://de.wikipedia.org/wiki/"
# Set cache timeout to infinity
CACHE_TIMEOUT = None

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
bootstrap = Bootstrap5(app)
cache.init_app(app)

WG = None


def setupGraph(workingDir, allTitlesPath, graphPath):
    global WG
    WG = wg.WikiGraph(workingDir, allTitlesPath, "", graphPath)
    WG.loadGraphNK()
    WG.loadAllHeadingNS0Pretty()

setupGraph(WORKING_DIR, ALLTITLESPATH, GRAPHPATH)

@app.route('/')
@cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def index():
    source = request.args.get('source', "")
    target = request.args.get('target', "")
    path = []
    parametersValid = False
    duration = 0
    
    if source and target:
        parametersValid = True
        sourceValid = verifyArticle(source)
        targetValid = verifyArticle(target)

        if not sourceValid:
            flash("Start article name is not valid", "warning")
            parametersValid = False

        if not targetValid:
            flash("Target article name is not valid", "warning")
            parametersValid = False

        if parametersValid:
            start_time = time.time()
            simplePath = getPath(source,target)
            end_time = time.time()
            path = addLinks(simplePath)            
            duration = round(end_time - start_time, 2)

    return render_template('index.html', sourceValue=source, targetValue=target, searchPerformed=parametersValid, numberOfLinks=max(len(path)-1, 0), path=path, duration=duration)

def getPath(source, target):
    global WG
    return WG.findPathName(source,target)

def verifyArticle(articleName):
    global WG
    return WG.pNameIsValid(articleName)

def addLinks(artikleList):
    enrichedList = []
    for a in artikleList:
        enrichedList.append((a, WIKIPEDIA_URL + a.replace(" ", "_")))
    return enrichedList