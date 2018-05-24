from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import ProjectForm
from .. import db
from ..models import *


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


##Projects Views
@admin.route('/projects', methods=['GET', 'POST'])
@login_required  #call list function from projects
def list_projects():
    """
    List all projects
    """
    check_admin()

    projects = Project.query.all()

    return render_template('admin/projects/projects.html',
                           projects=projects, title="Projects")


@admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Add a project to the database
    """
    check_admin()

    add_project = True

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                                description=form.description.data)
        try:
            # add project to the database
            db.session.add(project)
            db.session.commit()
            flash('You have successfully added a new project.')
        except:
            # in case project name already exists
            flash('Error: project name already exists.')

        # redirect to projects page
        return redirect(url_for('admin.list_projects'))

@admin.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project
    """
    check_admin()

    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the sproject.')

        # redirect to the projects page
        return redirect(url_for('admin.list_projects'))

    form.description.data = project.description
    form.name.data = project.name
    return render_template('admin/projects/project.html', action="Edit",
                           add_project=add_project, form=form,
                           project=project, title="Edit Project")


@admin.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """
    Delete a project from the database
    """
    check_admin()

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    # redirect to the projects page
    return redirect(url_for('admin.list_projects'))

    return render_template(title="Delete Project")


##User Views
""" @admin.route('/users')
def list_user():
    check_admin()
    users = User.query.all()
    return render_template('admin/users/users.html',
                        users=users, title="Users") 
                        """


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a project and a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a project or role
    if user.is_super:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.project_id = form.project.data
        user.access_level = form.access_level.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a project and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')

