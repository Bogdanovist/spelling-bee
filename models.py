from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from db.base_class import Base 

class Word(Base):
    #id = Column(Integer, primary_key=True)
    word = Column(String(100), primary_key=True)
    level = Column(Integer, nullable=False)

class Question(Base):
    id = Column(Integer, primary_key=True)
    word_id = Column(String, ForeignKey("word.word"), nullable=False)
    result = Column(String(10), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())