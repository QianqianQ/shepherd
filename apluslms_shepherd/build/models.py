import enum

from apluslms_shepherd.extensions import db


class States(enum.Enum):
    PUBLISH = 1
    RUNNING = 2
    FINISHED = 3
    FAILED = 4


class Action(enum.Enum):
    CLONE = 1
    BUILD = 2


class Build(db.Model):
    course_key = db.Column(db.String(50), primary_key=True)
    instance_key = db.Column(db.String(50), primary_key=True)
    start_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(States))
    action = db.Column(db.Enum(Action))


class BuildLog(db.Model):
    task_id = db.Column(db.String(50), primary_key=True)
    course_key = db.Column(db.String(50))
    instance_key = db.Column(db.String(50))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(States))
    action = db.Column(db.Enum(Action))
    log_text = db.Column(db.Text)
