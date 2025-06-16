from flask import Flask, render_template

from data.answer_questions import AnswerQuestion
from data.db_session import global_init, create_session
from data.questions import Question
from data.theme_questions import ThemeQuestions
from data.training_class import TrainingClass

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/class/<class_name>')
def class_page(class_name):
    with create_session() as session:
        train_class = session.query(TrainingClass).filter(TrainingClass.name == class_name).first()
        print(train_class.id)
        themes = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id).all()
    return render_template('class_page.html', title=f'Ответы {class_name} класс', themes=themes, class_name=class_name)


@app.route('/class/<class_name>/tests/<test_id>')
def show_test(class_name, test_id):
    with create_session() as session:
        train_class = session.query(TrainingClass).filter(TrainingClass.name == class_name).first()
        theme = session.query(ThemeQuestions).filter(ThemeQuestions.class_id == train_class.id, ThemeQuestions.id == test_id).first()
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
        train_class = session.query(TrainingClass).filter(TrainingClass.name == class_name).first()
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

    return render_template('show_all_test.html', title=f'Все ответы на {class_name} класс', all_lst_questions=all_lst_questions, class_name=class_name)


if __name__ == '__main__':
    global_init('db/informatic_questions.db')
    app.run()
