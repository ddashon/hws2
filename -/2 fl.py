import 1
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def form():
    temperature=1.weather()
    if request.args:
        return render_template('result.html')
    return render_template('form.html', temperature=temperature)


@app.route('/itog')
def itog():
    word = request.args['word']
    translation = 1.alltext(word)
    return render_template('itog.html', translation=translation)


@app.route('/itog2')
def second():
    with open('translated.txt', 'r', encoding='UTF-8') as file:
        translated = file.read()
    return render_template('second.html', translated = translated)


if __name__ == '__main__':
    app.run(debug=True)
