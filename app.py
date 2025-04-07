from typing import final

from flask import Flask, render_template
import os
from docx import Document

app = Flask(__name__)
my_dir = os.path.dirname(__file__)
NAMES_TESTS = sorted(os.listdir(os.path.join(my_dir, 'tests_9')))


@app.route('/')
def index():
    return render_template('index.html', names=NAMES_TESTS)


@app.route('/tests/<test_id>')
def show_test(test_id):
    doc = Document(os.path.join(my_dir, f'tests_9/{NAMES_TESTS[int(test_id) - 1]}'))
    new_lst = []
    for x in [x.text for x in doc.paragraphs]:
        new_lst += [y.strip() for y in x.split('\n')]
    return render_template('show_test.html', strings=new_lst)


@app.route('/all_tests')
def show_all_test():
    final_lst = []
    for name in NAMES_TESTS:
        doc = Document(os.path.join(my_dir, f'tests_9/{name}'))
        new_lst = []
        for x in [x.text for x in doc.paragraphs]:
            new_lst += [y.strip() for y in x.split('\n')]
        final_lst.append('')
        final_lst.append('')
        final_lst += new_lst

    return render_template('show_test.html', strings=final_lst)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
