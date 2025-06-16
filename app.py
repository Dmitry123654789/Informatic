from flask import Flask, render_template, redirect, request
from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from flask_restful import Api
from requests import post

from api.resourse_login import LoginResource
from data.answer_questions import AnswerQuestion
from data.db_session import global_init, create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions
from data.training_class import TrainingClass
from werkzeug.exceptions import NotFound

from data.users import User
from form.user_form import UserForm

app = Flask(__name__)




# api пользователей
api = Api(app)
api.add_resource(LoginResource, '/api/login')

app.config['SECRET_KEY'] = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)

def chech_class(class_name):
    with create_session() as session:
        train_class = session.query(TrainingClass).filter(TrainingClass.name == class_name).first()
    if not train_class:
        raise NotFound()
    return train_class


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/class/<class_name>')
def class_page(class_name):
    with create_session() as session:
        train_class = chech_class(class_name)
        themes = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id).all()
    return render_template('class_page.html', title=f'Ответы {class_name} класс', themes=themes, class_name=class_name)


@app.route('/class/<class_name>/tests/<test_id>')
def show_test(class_name, test_id):
    with create_session() as session:
        train_class = chech_class(class_name)
        theme = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id,
                                                     ThemeQuestions.id == test_id).first()
        if not theme:
            raise NotFound()
        questions = session.query(Question).filter(Question.theme_id == theme.id)

    # ["название теста", ("вопрос", ["фото"], ["ответы"])]
    lst_questions = [theme.name]
    for question in questions:
        que_que = question.question.splitlines()
        que = [que_que[0], que_que[1:]]
        with create_session() as session:
            answ = session.query(AnswerQuestion).filter(AnswerQuestion.question_id == question.id).all()
        que += [[x.answer for x in answ]]
        lst_questions.append(que)

    return render_template('show_test.html', title=theme.name, questions=lst_questions, class_name=class_name)


@app.route('/class/<class_name>/tests/all_tests')
def show_all_test(class_name):
    all_lst_questions = []
    with create_session() as session:
        train_class = chech_class(class_name)
        themes = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id)

        for theme in themes:
            # ["название теста", ("вопрос", ["фото"], ["ответы"])]
            questions = session.query(Question).filter(Question.theme_id == theme.id)
            lst_questions = [theme.name]
            for question in questions:
                que_que = question.question.splitlines()
                que = [que_que[0], que_que[1:]]
                answ = session.query(AnswerQuestion).filter(AnswerQuestion.question_id == question.id).all()
                que += [[x.answer for x in answ]]
                lst_questions.append(que)

            all_lst_questions.append(lst_questions)

    return render_template('show_all_test.html', title=f'Все ответы на {class_name} класс',
                           all_lst_questions=all_lst_questions, class_name=class_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        login_post = post(f'http://localhost:5000/api/login',
                          json={'email': form.email.data, 'password': form.password.data})
        if login_post.status_code == 200:
            user = User(**login_post.json()['user'])
            login_user(user, remember=True)
            return redirect('/')
        elif login_post.status_code == 401:
            form.password.errors = ['Неверный пароль']
            return redirect('/login')
        elif login_post.status_code == 404:
            form.email.errors = ['Пользователь не найден']
            return redirect('/login')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    sess = create_session()
    user = sess.get(User, user_id)
    return user

if __name__ == '__main__':
    global_init('db/informatic_questions.db')
    app.run()
