from sqlalchemy import event
from sqlalchemy.sql import func, select

from zeus.config import db
from zeus.db.mixins import RepositoryBoundMixin, StandardAttributes
from zeus.db.types import GUID, JSONEncodedDict
from zeus.db.utils import model_repr
from zeus.utils import timezone


class ChangeRequest(RepositoryBoundMixin, StandardAttributes, db.Model):
    number = db.Column(db.Integer, nullable=False)
    parent_revision_sha = db.Column(db.String(40), nullable=False)
    message = db.Column(db.String, nullable=False)
    author_id = db.Column(GUID, db.ForeignKey('author.id'), index=True)
    provider = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String(64), nullable=True)
    url = db.Column(db.String, nullable=True)
    data = db.Column(JSONEncodedDict, nullable=True)
    date_updated = db.Column(db.TIMESTAMP(
        timezone=True), nullable=True, onupdate=timezone.now)

    parent_revision = db.relationship(
        'Revision', foreign_keys='[ChangeRequest.repository_id, ChangeRequest.parent_revision_sha]', viewonly=True
    )
    author = db.relationship('Author')

    __tablename__ = 'change_request'
    __table_args__ = (
        db.ForeignKeyConstraint(
            ('repository_id',
             'parent_revision_sha'), ('revision.repository_id', 'revision.sha')
        ),
        db.Index('idx_cr_repo_sha', 'repository_id', 'parent_revision_sha'),
        db.UniqueConstraint('repository_id', 'number', name='unq_cr_number'),
        db.UniqueConstraint('repository_id', 'provider',
                            'external_id', name='unq_cr_provider')
    )
    __repr__ = model_repr('repository_id', 'parent_revision_sha')

    @property
    def subject(self):
        return self.message.splitlines()[0]


@event.listens_for(ChangeRequest.repository_id, 'set', retval=False)
def set_number(target, value, oldvalue, initiator):
    if value is not None and target.number is None:
        target.number = select([func.next_item_value(value)])
    return value
