def sqlalchemy_orm_to_dict(model):
    """
    Converts sqlalchemy model to dictionary
    :param model: declarative sqlalchemy model
    :return: Sqlalchemy model as dictionary
    :rtype: dict
    :raise RuntimeError: if passed object not a sqlalchemy model
    """
    if not hasattr(model, '__table__') or not hasattr(model.__table__, 'columns'):
        raise RuntimeError(
            "{} not JSON serializable. Probably, not sqlalchemy model?".format(model.__name__)
        )

    def columns():
        return [c.name for c in model.__table__.columns]

    return dict([(c, getattr(model, c)) for c in columns()])
