from flask import (
    Blueprint,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError

from app.database import db
from .models import Comment
from .forms import CommentAddForm


module = Blueprint('comment', __name__, url_prefix='/comment')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/add/', methods=['POST'])
def add():
    form = CommentAddForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            comment = Comment(**form.data)
            db.session.add(comment)
            db.session.commit()
            flash('Comment was successful added!', 'success')
            return redirect(url_for('entity.view', id=comment.entity_id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('Uncaught exception while querying database', 'danger')
        abort(500)

