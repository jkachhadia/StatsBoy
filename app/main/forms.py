from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import Required,Length,Email,Regexp
from ..models import Role,User
from flask.ext.pagedown.fields import PageDownField


class EditProfileForm(Form):
    name=StringField('Real Name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')

class EditProfileAdminForm(Form):
    email=StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('Username',validators=[Required(),Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must only have letters, numbers, dots or underscores')])
    confirmed=BooleanField('Confirmed')
    role=SelectField('Role', coerce=int)
    name=StringField('Real Name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')

    def __init__(self,user, *args, **kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name)
                              for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(username=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class PostForm(Form):
    body=PageDownField("Whats on your mind?",validators=[Required()])
    submit=SubmitField('Submit')

class CommentForm(Form):
    body=StringField('',validators=[Required()])
    submit=SubmitField('Submit')

class MoodForm(Form):
    mood=StringField("How's your mood?",validators=[Required()])
    submit=SubmitField('shoot your mood')
