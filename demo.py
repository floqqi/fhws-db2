from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@192.168.99.100:3306/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
db = SQLAlchemy(app)
session = db.session


class Studiengang(db.Model):
    __tablename__ = 'studiengaenge'

    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.Unicode(255),
        nullable=False,
        unique=True
    )


class Student(db.Model):
    __tablename__ = 'studenten'

    id = db.Column(
        db.Integer(),
        primary_key=True
    )
    name = db.Column(
        db.Unicode(255),
        nullable=False
    )
    exmatrikuliert_am = db.Column(
        db.Date()
    )
    studiengang_id = db.Column(
        db.Integer(),
        db.ForeignKey('studiengaenge.id'),
        nullable=False
    )
    studiengang = db.relationship(
        Studiengang,
        lazy='joined'
    )

    @hybrid_property
    def ist_eingeschrieben(self):
        return self.exmatrikuliert_am is None

    @ist_eingeschrieben.expression
    def ist_eingeschrieben(cls):
        return cls.exmatrikuliert_am == None


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    manager.run(
        default_command='shell'
    )
