from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URI = f"postgresql://matt@localhost/spelling_bee"
print(SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_pre_ping=True,
)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)