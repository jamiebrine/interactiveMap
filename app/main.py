import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/landing')
def go():
    return render_template('app/base.html')