import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Questions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)

    theme_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('theme_questions.id'))
    theme = sqlalchemy.orm.relationship('ThemeQuestions')