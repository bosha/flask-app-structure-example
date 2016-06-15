from slugify import slugify
from sqlalchemy import event

from app.database import db

class Entity(db.Model):
    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False, unique=True)
    slug = db.Column(db.String(1000))
    content = db.Column(db.String(5000))

    comments = db.relationship('Comment', backref='entity')

    def __str__(self):
        return self.name


@event.listens_for(Entity, 'before_insert')
def event_before_insert(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    target.slug = slugify(target.name)


@event.listens_for(Entity, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
