from flask import request
from flask import render_template, jsonify
from app import flask_app


app = flask_app.get_app()
app_routes = [
    { 'path': '/', 'name': 'index'},
    { 'path': '/help', 'name': 'Help'},
    { 'path': '/status', 'name': 'Counters'},
    { 'path': '/status/details', 'name': 'Detailed Counters'}
]


# ###### Custom Routes
@app.route('/')
@app.route('/index')
def index():
    msg = "Hello, World!"
    #data = utils.parse_request(request, fmt='raw') or ''
    return (msg)


@app.route('/help')
def routes_map():
    msg = { "routes": []}
    url_root = request.url_root[:-1]
    for r in app_routes:
        r['url'] = "{}{}".format(url_root, r['path'])
        msg['routes'].append(r)

    #return ("{} {}\n".format(request.url_root))
    return jsonify(msg), 200


@app.route('/status')
def status():
    msg = {}
    msg['version'] = flask_app.get_version()
    msg['pool'] = flask_app.pool.metrics_list()
    msg['this'] = str(repr(request))

    return jsonify(msg), 200


@app.route('/status/details')
def status_details():
    msg = {}
    msg['version'] = flask_app.get_version()
    msg['pool'] = flask_app.pool.metrics_list_detailed()
    msg['this'] = str(repr(request))

    return jsonify(msg), 200


@app.route('/run')
def run_jobs():
    flask_app.pool.run(func=flask_app.tasks.run_sleep15, alias='task1')
    flask_app.pool.run(func=flask_app.tasks.run_sleep30,
                       a1="aaa", a2=123, alias='task2')
    return 'Two jobs was launched in background!'


# ###### Error handle routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('code_404.html')


# ###### Internal framework funcs
@app.before_request
def metrics_before():
    print("Req Before. TODO register req metrics: {}". format(repr(request)))
    return


@app.after_request
def metrics_after(response):
    print("Req After. TODO register resp metrics: {}". format(repr(response)))
    return response
