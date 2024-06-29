from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(Text)
    language = Column(Text)
    sent = Column(Integer, default=0)
    accepted = Column(Integer, default=0)


class Review(Base):
    __tablename__ = 'review'
    document_id = Column(Text, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_msg_id = Column(Integer)
    admin_msg_id = Column(Integer)


class Reviewed(Base):
    __tablename__ = 'reviewed'
    document_id = Column(Text, ForeignKey('review.document_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_msg_id = Column(Integer)
    reviewed_msg_id = Column(Integer)
    accepted = Column(Boolean)
    feedback = Column(Text)
