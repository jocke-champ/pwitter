from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TweetForm(FlaskForm):
    tweet = StringField('Tweet', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')