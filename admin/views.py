"""
Author: Josh and Shaikha
Description: This module defines a Flask blueprint for an admin feature.
The 'admin' blueprint includes routes and views for managing administrative tasks.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from models import User
from app import requires_roles


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin/admin.html')


# view all registered users
@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
    current_users = User.query.filter_by(role='user').all()
    return render_template('admin/admin.html', name="PLACEHOLDER FOR FIRSTNAME", current_users=current_users)


@admin_blueprint.route('/logs', methods=['POST'])
@login_required
@requires_roles('admin')
def logs():
    with open("blog.log", "r") as f:
        content = f.read().splitlines()[-20:]

    return render_template('admin/admin.html', logs=content)

