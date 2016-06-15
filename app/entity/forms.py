from flask.ext.wtf import Form
from wtforms import (
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired

class EntityCreateForm(Form):
    name = StringField(
        'Name',
        [
            DataRequired(message="This field is required")
        ],
        description="Name of the entity"
    )
    content = TextAreaField(
        'Content',
        [],
        description="Content of the entity",
    )
