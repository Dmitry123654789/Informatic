import os

from flask import render_template, redirect, request
from flask_login import login_user, logout_user
from requests import post, session
from werkzeug.exceptions import NotFound

from api.resourse_login import post_login
from data.answer_questions import AnswerQuestion
from data.db_session import create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions
from data.training_class import TrainingClass
from data.users import User
from form.theme_form import ThemeForm
from form.user_form import UserForm
from tools import app, login_manager
from tools.parse_docx_file import create_new_theme


def chech_class(class_name):
    with create_session() as session:
        train_class = session.query(TrainingClass).filter(TrainingClass.name == class_name).first()
    if not train_class:
        raise NotFound()
    return train_class


def get_answer_and_questions(theme):
    with create_session() as session:
        # ["название теста", ("вопрос", ["фото"], ["ответы"])]
        questions = session.query(Question).filter(Question.theme_id == theme.id)
        lst_questions = [theme.name]
        for question in questions:
            que_que = question.question.splitlines()
            que = [que_que[0], que_que[1:]]
            answ = session.query(AnswerQuestion).filter(AnswerQuestion.question_id == question.id).all()
            que += [[x.answer for x in answ]]
            lst_questions.append(que)
    return lst_questions


def delete_theme(theme, train_class):
    with create_session() as session:
        questions = session.query(Question).filter(Question.theme_id == theme.id)
        for question in questions:
            img_srces = question.question.splitlines()[1:]
            for img_src in img_srces:
                full_img_src = 'tools/' + img_src
                if os.path.exists(full_img_src):
                    os.remove(full_img_src)

            answers = session.query(AnswerQuestion).filter(AnswerQuestion.question_id == question.id).all()
            for answer in answers:
                session.delete(answer)

            session.delete(question)

        session.delete(theme)
        session.commit()


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/class/<class_name>')
def class_page(class_name):
    with create_session() as session:
        train_class = chech_class(class_name)
        themes = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id).all()
    return render_template('class_page.html', title=f'Ответы {class_name} класс', themes=themes, class_name=class_name)


@app.route('/class/<class_name>/tests/<test_id>', methods=["GET", "POST"])
def show_test(class_name, test_id):
    with create_session() as session:
        train_class = chech_class(class_name)
        theme = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id,
                                                     ThemeQuestions.id == test_id).first()
        if not theme:
            raise NotFound()

        # Был отправлен запрос на удаление темы
    if request.method == 'POST':
        delete_theme(theme, class_name)
        return redirect(f'/class/{class_name}')

    lst_questions = get_answer_and_questions(theme)
    return render_template('show_test.html', title=theme.name, questions=lst_questions, class_name=class_name)


@app.route('/class/<class_name>/tests/all_tests')
def show_all_test(class_name):
    all_lst_questions = []
    with create_session() as session:
        train_class = chech_class(class_name)
        themes = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id)

    for theme in themes:
        lst_questions = get_answer_and_questions(theme)
        all_lst_questions.append(lst_questions)

    return render_template('show_all_test.html', title=f'Все ответы на {class_name} класс',
                           all_lst_questions=all_lst_questions, class_name=class_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        login_post = post_login(**{'email': form.email.data, 'password': form.password.data})
        if login_post.status_code == 200:
            user = User(**login_post.json['user'])
            login_user(user, remember=True)
            return redirect('/')
        elif login_post.status_code == 401:
            form.password.errors = ['Неверный пароль']
            return redirect('/login')
        elif login_post.status_code == 404:
            form.email.errors = ['Пользователь не найден']
            return redirect('/login')
    return render_template('login.html', form=form, title='Войти')


@app.route('/admin/new_theme', methods=['GET', 'POST'])
def admin_classes():
    form = ThemeForm()
    if request.method == 'POST':
        file = form.theme
        train_class = form.train_class.data
        answ = create_new_theme(file, train_class)
        return render_template('admin/add_theme.html', train_class=train_class, success=True,
                               title='Новая тема добавлена')
    return render_template('admin/add_theme.html', form=form, title='Создание новой темы')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    user = sess.get(User, user_id)
    return user
