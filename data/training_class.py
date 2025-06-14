import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class TrainingClass(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'training_class'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
