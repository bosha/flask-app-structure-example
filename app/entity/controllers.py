from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from .models import Entity, db
from .forms import EntityCreateForm
from app.utils.db import sqlalchemy_orm_to_dict
from app.comment.forms import CommentAddForm
from app.comment.models import Comment

module = Blueprint('entity', __name__)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET'])
@module.route('/page/<int:page>/', methods=['GET'])
def index(page=1):
    entities = None
    try:
        entities = Entity.query.paginate(page, 1, True)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was uncaught database query', 'danger')
        abort(500)
    return render_template('entity/index.html', object_list=entities)


@module.route('/<int:id>/view/', methods=['GET'])
def view(id):
    entity = None
    cmt_form = CommentAddForm(request.form)
    try:
        entity = db.session.\
            query(Entity).\
            filter(Entity.id == id).\
            options(joinedload(Entity.comments)).\
            first()
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return render_template('entity/view.html', object=entity, form=cmt_form)


@module.route('/create/', methods=['GET', 'POST'])
def create():
    form = EntityCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            entity = Entity(**form.data)
            db.session.add(entity)
            db.session.flush()
            id = entity.id
            db.session.commit()
            flash('The entity was successfully added!', 'success')
            return redirect(url_for('entity.view', id=id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database', exc_info=e)
        db.session.rollback()
        flash('There was error while querying database', 'error')
    return render_template('entity/create.html', form=form)


@module.route('/<int:id>/update/', methods=['GET', 'POST'])
def update(id):
    form = EntityCreateForm(request.form)
    entity = Entity.query.get_or_404(id)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            for key, val in form.data.items():
                if hasattr(entity, key):
                    setattr(entity, key, val)
            db.session.commit()
            flash('Entity successful updated!', 'success')
            return redirect(url_for('entity.view', id=id))
        else:
            form = EntityCreateForm(**sqlalchemy_orm_to_dict(entity))
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error('Uncaught exception while '
                  'querying database at entity.update', exc_info=e)
        flash('Uncaught error while querying database', 'danger')
        abort(500)
    return render_template('entity/update.html', form=form, id=id)


@module.route('/view/<int:id>/remove/', methods=['GET', 'POST'])
def remove(id):
    entity = None
    try:
        if request.method == 'POST':
            entity = Entity.query.filter_by(id=id).first_or_404()
            Comment.query.filter(Comment.entity_id == entity.id).delete()
            db.session.delete(entity)
            db.session.commit()
            flash('Entity was successful removed!', 'success')
            return redirect(url_for('entity.index'))
        else:
            entity = Entity.query.get_or_404(id)
    except SQLAlchemyError as e:
        db.session.rollback()
        log_error('Uncaught exception '
                  'while querying database at entity.remove', exc_info=e)
        flash('Uncaught exception while querying database', 'danger')
        abort(500)
    return render_template('entity/delete.html', object=entity)
