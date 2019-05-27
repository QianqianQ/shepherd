import enum

from sqlalchemy_mptt.mixins import BaseNestedSets

from apluslms_shepherd.extensions import db

# db.metadata.clear()

gm_table = db.Table('gm_table', db.Model.metadata,
                    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                    )

gp_table = db.Table('gp_table', db.Model.metadata,
                    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                    db.Column('permission_id', db.Integer, db.ForeignKey('group_permission.id'))
                    )


class CRUD():
    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()


class Group(db.Model, BaseNestedSets, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    members = db.relationship("User", secondary=gm_table,
                              backref=db.backref('groups', lazy='dynamic'))
    permissions = db.relationship("GroupPermission", secondary=gp_table,
                                  backref=db.backref('groups', lazy='dynamic'))

    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        if self.parent is None:
            return "Root: <Group (id={0}, name={1}, parent=None)>".format(self.id, self.name)
        else:
            return "<Group (id={0}, name={1}, parent={2})>".format(self.id, self.name,
                                                                   self.parent.name)


PERM_TYPE = {'groups': 'manage groups', 'courses': 'manage courses'}
PERMISSION_LIST = list(perm_tuple for perm_tuple in PERM_TYPE.items())


class PermType(enum.Enum):
    groups = 1
    courses = 2


class GroupPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(PermType))
