import sqlalchemy

from .db_session import SqlAlchemyBase


class AnswerQuestion(SqlAlchemyBase):
    __tablename__ = 'answer'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    answer = sqlalchemy.Column(sqlalchemy.String)

    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('question.id'))
    question = sqlalchemy.orm.relationship('Question')