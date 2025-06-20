import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class ThemeQuestions(SqlAlchemyBase):
    __tablename__ = 'theme_questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('training_class.id'))
    training_class = relationship('TrainingClass')
