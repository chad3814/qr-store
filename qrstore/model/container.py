from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Text, ARRAY

from qrstore.model import DeclarativeBase, metadata, DBSession

class Container(DeclarativeBase):
    __tablename__ = 'container'

    container_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    title = Column(Text)
    uuid = Column(Text, unique=True)
    items = Column(ARRAY(Text))