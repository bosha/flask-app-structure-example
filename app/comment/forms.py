from flask.ext.wtf import Form
from wtforms import (
    StringField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Email,
)

class CommentAddForm(Form):
    name = StringField(
        'Name',
        [
            DataRequired(message="This field is required")
        ],
        description="Your name"
    )
    email = StringField(
        'E-Mail',
        [
            Email()
        ],
        description="Содержимое записи",
    )
    content = TextAreaField(
        'Content',
        [
            DataRequired(message="This field is required")
        ],
        description="Content of the comment"
    )
    entity_id = HiddenField()
