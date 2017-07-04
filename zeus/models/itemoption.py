from datetime import datetime

from zeus.config import db
from zeus.db.types import GUID


class ItemOption(db.Model):
    id = db.Column(GUID, primary_key=True, default=GUID.default_value)
    item_id = db.Column(GUID, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    __tablename__ = 'itemoption'
    __table_args__ = (
        db.UniqueConstraint('item_id', 'name', name='unq_itemoption_name'),
    )