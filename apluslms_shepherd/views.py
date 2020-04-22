from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user, login_user
from flask_principal import identity_changed, Identity

from apluslms_shepherd.build.models import Build
from apluslms_shepherd.courses.models import CourseInstance
from apluslms_shepherd.auth.models import User
from apluslms_shepherd.extensions import db
from apluslms_shepherd import config

main_bp = Blueprint('main', __name__)


class FrontendBuild(object):
    def __init__(self, course_id, number, course_key, instance_key, step, state):
        self.course_id = course_id
        self.instance_key = instance_key
        self.course_key = course_key
        self.number = number
        self.current_state = None if state is None else state.name
        self.current_step = None if step is None else step.name


@main_bp.route('/', methods=['GET'])
# @login_required
def main_page():
    print("course clone dir: ", config.DevelopmentConfig.COURSE_REPO_BASEPATH)
    user = User.query.filter_by(id='1').first()
    if user is None:
        user = User(id='1',
                    email="test1@aalto.fi",
                    display_name="Teacher",
                    sorting_name="Smith",
                    full_name="TEACHER SMITH",
                    roles="Teacher")
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
    login_user(user)
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))

    instances = CourseInstance.query.all()
    sorted_build_entries = Build.query.order_by(Build.number.desc())
    newest_builds = [
        FrontendBuild(course_id=instance.id,
                      instance_key=instance.instance_key,
                      course_key=instance.course_key,
                      number=0 if len(sorted_build_entries.filter_by(course_id=instance.id).all()) is 0
                      else sorted_build_entries.filter_by(course_id=instance.id).first().number,
                      state=None if len(sorted_build_entries.filter_by(course_id=instance.id).all()) is 0
                      else sorted_build_entries.filter_by(course_id=instance.id).first().state,
                      step=None if len(sorted_build_entries.filter_by(course_id=instance.id).all()) is 0
                      else sorted_build_entries.filter_by(course_id=instance.id).first().step
                      )
        for instance in instances
    ]
    return render_template('main.html', user=current_user, instances=newest_builds)
