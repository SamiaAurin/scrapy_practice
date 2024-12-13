from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    image_path = Column(String)

# Database connection
DATABASE_URL = "postgresql://username:password@ecommerce_scraper-db-1:5432/ecommerce_data"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session() #creates a new session object that is used for querying or adding data to the database.
