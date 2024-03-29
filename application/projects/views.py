from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db, permission_required
from application.projects.models import Project
from application.projects.forms import CreateProjectForm, UpdateProjectForm
from application.permissions.models import Permission
from application.stages.forms import CreateStageForm
from application.permissions.forms import AddUserToProjectForm

@app.route("/projects", methods=["GET"])
@login_required
def projects_index():
    return render_template("projects/list.html", projects = current_user.get_projects())

@app.route("/projects/create/")
@login_required
def projects_create_form():
    return render_template("projects/create.html", form = CreateProjectForm())

@app.route("/projects/create/", methods=["POST"])
@login_required
def projects_create():
    form = CreateProjectForm(request.form)

    if not form.validate():
        return render_template("projects/create.html", form = form)
    
    p = Project(form.name.data)
    db.session().add(p)
    db.session().commit()

    perm = Permission(p.id, current_user.get_id(), True)
    db.session().add(perm)
    db.session().commit()
    
    return redirect(url_for("projects_index"))

@app.route("/projects/<project_id>/update", methods=["GET"])
@login_required
@permission_required(admin=True)
def projects_update_form(project_id):
    p = Project.query.get(project_id)
    return render_template("projects/update.html", project=p,
                           project_form = UpdateProjectForm(),
                           stage_form = CreateStageForm(),
                           add_user_to_project_form = AddUserToProjectForm(project_id))

@app.route("/projects/<project_id>/update", methods=["POST"])
@login_required
@permission_required(admin=True)
def projects_update(project_id):
    form = UpdateProjectForm(request.form)

    p = Project.query.get(project_id)
    
    if not form.validate():
        return render_template("/projects/update.html", project=p,
                               project_form = form,
                               stage_form = CreateStageForm(),
                               add_user_to_project_form = AddUserToProjectForm(project_id))
    
    p.name = form.name.data

    db.session().commit()

    return redirect(url_for("projects_update_form", project_id = project_id))

@app.route("/projects/<project_id>/delete", methods=["GET"])
@login_required
@permission_required(admin=True)
def projects_delete_form(project_id):
    p = Project.query.get(project_id)
    return render_template("/projects/delete.html", project=p)

@app.route("/projects/<project_id>/delete", methods=["POST"])
@login_required
@permission_required(admin=True)
def projects_delete(project_id):
    p = Project.query.get(project_id)
    if p is not None:
        db.session().delete(p)
        db.session().commit()
    return redirect(url_for("projects_index"))
