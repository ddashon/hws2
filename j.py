from flask import Flask

app = Flask(__name__)

@app.route('/1/')
def index():
    return '<html><head><p>log in, please</p></head></html>'

from flask import render_template
@app.route('/1/')
@app.route('/1/<name>')
def log(name=None):
    return render_template('a.html', name=name)


from flask import request
@app.route('/1/')
def login():
    if request.args['password'] == '123':
        return 'Name: ' + request.args['login']

if __name__ == '__main__':
    app.run(debug=True)
