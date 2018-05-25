from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

ACCESS = [
    (1, 'user'), 
    (2, 'admin'),
    ]
    
ROLES =  [
    (0, 'annotator'), 
    (1, 'validator')
    ]

#Project forms
class ProjectForm(FlaskForm):
    """
    Form for admin to add or edit a project
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

    ## TODO: Restructure createdb ...

##User Forms
class UserAssignForm(FlaskForm):
    """
    Form for admin to assign projects and roles to users
    """
    project = QuerySelectField(query_factory=lambda: Project.query.all(),
                                  get_label="name")
    access_level = SelectField('Level', choices=ACCESS)
    role = SelectField('Role', choices=ROLES)
    submit = SubmitField('Submit')