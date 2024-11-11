from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL
from typing import Optional

class PhotoForm(FlaskForm):
    title: StringField = StringField('Title', validators=[DataRequired()])
    description: Optional[TextAreaField] = TextAreaField('Description')
    image_url: StringField = StringField('Image URL', validators=[DataRequired(), URL()])
    submit: SubmitField = SubmitField('Add Photo')

