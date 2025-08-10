from . import users_blueprint
from flask import flash, render_template

@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('users/403.html'), 403

@users_blueprint.route("/about", methods=['GET'])
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template("users/about.html", company_name="Puneeth Y S")