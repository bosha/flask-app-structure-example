from sqlalchemy import event

from app.database import db

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    content = db.Column(db.Text())

    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))

    def __str__(self):
        return self.name


@event.listens_for(Comment, 'after_delete')
def event_after_delete(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    pass
