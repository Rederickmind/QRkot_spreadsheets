from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_model import AbstractModel


class Donation(AbstractModel):
    """Модель для пожертвований."""
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))