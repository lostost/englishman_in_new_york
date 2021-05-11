import json

from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from pdf_translate import convert_pdf_to_txt
from pdf_translate_google_api import go_translate
import data
import random
import re
import word_processing
import os
import collections

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
UPLOAD_FOLDER = '/static/pdf_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
goals = data.goals
teachers = data.teachers
for id in teachers:
    teachers[id]['url'] = id
    teachers[id]['id'] = id


class MyForm(FlaskForm):
    # name = StringField('name')
    file = FileField()


def tokenization(text):
    text = re.split('[^a-zа-яё]+', text, flags=re.IGNORECASE)
    return text


@app.template_filter('teacher_name')
def teacher_name(teacher):
    return teacher.values()


def text_analysis(words):
    words_dict = {}
    for word in words:
        if word in words_dict:
            words_dict[words] += 1
        else:
            words_dict[words] = 1

    sorted_words_dict = sorted(words_dict, key=words_dict.get)
    return sorted_words_dict


@app.template_filter('filter_teachers_random')
def my_random(random_teachers, quantity=0):
    keys = list(random_teachers)
    random.shuffle(keys)
    if quantity == 0:
        quantity = len(keys)
    elif quantity > len(keys):
        quantity = len(keys)
    keys = keys[:quantity]
    result = {}

    for id in keys:
        result[id] = random_teachers[id]

    return result


@app.context_processor
def inject_goals():
    image_default = 'https://telegraf.design/wp-content/uploads/2018/02/SamNielson_Characterdimension_Bit-1.jpg'

    return dict(goals=goals, image_default=image_default)


# @app.route('/')
@app.route('/show')
def show():
    messages = request.args['messages']
    messages = session['messages']
    # print(json.loads(messages))
    file_name = str(json.loads(messages)['path'])
    raw = convert_pdf_to_txt(file_name)
    # print(raw)
    words = word_processing.main(raw)
    translate_words = go_translate('. '.join(words), 'ru').split('. ')
    # print('words = ', words)
    # print('translate = ', translate_words)
    # print('len words ', len(words))
    # print('len translate ', len(translate_words))
    words_dict = {}
    for i, word in enumerate(words):
        words_dict[word] = translate_words[i]
    # tokenization_text = tokenization(translated_raw)
    # result_words = text_analysis(' '.join(word_processing.main(raw)))
    print("file_name.split('/')[1]", '/'.join(file_name.split('/')[1:]))
    return render_template('index.html', file_name='/'.join(file_name.split('/')[1:]), words_dict=words_dict)


@app.route('/tutor', methods=['GET'])
def get_tutors():
    teachers_count = request.args.get('teachers_count')
    if teachers_count == 'all':
        quantity = 0
    else:
        quantity = 6
    return render_template('tutor.html', teachers=teachers, quantity=quantity, goals=goals)


@app.route('/')
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join('static/pdf_files', filename))
        messages = json.dumps({"path": os.path.join('static/pdf_files', filename)})
        session['messages'] = messages
        return redirect(url_for('.show', messages=messages))
    return render_template('submit.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
