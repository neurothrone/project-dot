from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import bp_user
from ..forms import EditProjectForm, NewProjectForm
from app.controllers.profile import ProfileController
from app.controllers.project import ProjectController
from app.schemas.complex import ProjectOutWithProfile
from app.schemas.project import ProjectIn, ProjectOut, ProjectUpdate


@bp_user.get("/projects/new")
@login_required
def new_project():
    return render_template("user/projects/new_project.html",
                           form=NewProjectForm())


@bp_user.post("/projects/new")
@login_required
def new_project_post():
    form = NewProjectForm()
    if form.validate_on_submit():
        project: ProjectOut = ProjectController.create(ProjectIn(
            title=form.title.data,
            description=form.description.data,
            demo_link=form.demo_link.data,
            source_link=form.source_link.data
        ))
        ProfileController.add_existing_project_to_user(project.id, current_user.id)
        flash("Project created successfully.", category="success")
        return redirect(url_for("open.view_project", project_id=project.id))
    return render_template("user/projects/new_project.html", form=form)


@bp_user.get("/projects/<int:project_id>/edit")
@login_required
def edit_project(project_id: int):
    if not (project := ProjectController.get_by_id(project_id)):
        flash("There is no project by that id.", category="error")
        return redirect(url_for("open.view_profile", username=current_user.username))

    # TODO: 'app.schemas.project.ProjectOut object' has no attribute 'owner'
    # if current_user.profile.id != project.owner.id:
    #     flash("You can not edit a project that is not your own.", category="error")
    #     return redirect(url_for("main.index"))

    return render_template("user/projects/edit_project.html",
                           form=EditProjectForm(obj=project),
                           project=project)


@bp_user.post("/projects/<int:project_id>/edit")
@login_required
def edit_project_post(project_id: int):
    form = EditProjectForm()
    if form.validate_on_submit():
        data = form.data
        del data["csrf_token"]
        del data["submit"]
        project_update = ProjectUpdate(**data)
        project: ProjectOut = ProjectController.update_model(project_id, project_update)
        flash(message="Changes to project saved.", category="success")
        return redirect(url_for("open.view_project", project_id=project.id))
    else:
        flash(message="Changes to project not saved.", category="error")

    return render_template("user/projects/edit_project.html",
                           form=form)


@bp_user.get("/projects/<int:project_id>/delete")
@login_required
def delete_project(project_id: int):
    project: ProjectOutWithProfile = ProjectController.get_by_id(project_id)

    if not project:
        flash("There is no project by that id.", category="error")
        return redirect(url_for("open.view_profile", username=current_user.username))

    if current_user.profile.id != project.owner.id:
        flash("You can not delete a project that is not your own.", category="error")
    else:
        ProjectController.delete(project.id)
        flash("Project deleted.", category="success")
    return redirect(url_for("open.view_profile", username=current_user.username))
