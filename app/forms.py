from flask_wtf import Form
from wtforms import PasswordField,validators,StringField,IntegerField,FloatField
from wtforms.validators import DataRequired,Required

class LoginForm(Form):
    name=StringField('name',validators=[DataRequired()])
    password=PasswordField('password',[validators.DataRequired()])

class SearchForm(Form):
    bookinfo=StringField('bookname',validators=[DataRequired()])

class Book_add(Form):
    id=StringField('id',validators=[DataRequired()])
    name = StringField('name')
    style_num = StringField('style_num',validators=[DataRequired()])
    author = StringField('author',validators=[DataRequired()])
    count = StringField('count',validators=[DataRequired()])
    available_count = StringField('available_count',validators=[DataRequired()])
    price = StringField('price')
    press = StringField('press', validators=[DataRequired()])
    publish_date = StringField('publish_date', validators=[DataRequired()])
    summary=StringField('summary', validators=[DataRequired()])

class Book_delete(Form):
    id = StringField('id', validators=[DataRequired()])

class Book_alter_select(Form):
    id=StringField('id',validators=[DataRequired()])

class Book_alter(Form):
    id=StringField('id')
    name = StringField('name',validators=[DataRequired()])
    style_num = StringField('style_num',validators=[DataRequired()])
    author = StringField('author',validators=[DataRequired()])
    count = StringField('count',validators=[DataRequired()])
    available_count = StringField('available_count',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    press=StringField('press',validators=[DataRequired()])
    publish_date=StringField('publish_date',validators=[DataRequired()])
    summary = StringField('summary', validators=[DataRequired()])

class Reader_add(Form):
    no=StringField('no',validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
    kind = StringField('kind', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    grade=StringField('grade', validators=[DataRequired()])
    department=StringField('department', validators=[DataRequired()])

class Reader_delete(Form):
    no = StringField('no', validators=[DataRequired()])

class Reader_alter_select(Form):
    no=StringField('readerno',validators=[DataRequired()])

class Reader_select(Form):
    no=StringField('readerno',validators=[DataRequired()])