from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><p>Hello, world!</p></body></html>'


@app.route('/time/<int:shift>')
def time_page(shift):
    h = datetime.datetime.today().hour
    h += shift
    return 'Time in your country:' + str(h)

@app.route('/user/<user>')
def user_index(user):
    return 'This is the page of' + user

if __name__ == '__main__':
    app.run(debug=True)
