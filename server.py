import traceback

from flask import Flask, request, render_template
from model import guess_programming_language, load_model


app = Flask(__name__)


DEFAULT_MODEL_DIR = "my_model_cpu/"
classiffer = load_model(DEFAULT_MODEL_DIR)

@app.route('/check')
def ping():
    return 'everything is OK'


@app.route('/', methods=['GET', 'POST'])
def guess():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            code = request.form['code']
            if not code or len(code) <= 20:
                return render_template('index.html', error='Please type more than 20 characters!')
            language, score = guess_programming_language(classiffer, code)
            return render_template('index.html', language=language, score=score, code=code)
        except:
            traceback.print_exc()
            return render_template('index.html', error='Unknown error has occurred, please try again!')


if __name__ == '__main__':
    app.run(port=5001, debug=False)

