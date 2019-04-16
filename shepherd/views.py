from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


@login_required
@main_bp.route('/', methods=['GET'])
def main_page():
    return render_template('main.html', user=current_user)