import os
import requests
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup (SQLAlchemy)
Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    image_path = Column(String)

# Create a database engine
DATABASE_URL = "postgresql://username:password@ecommerce_scraper-db-1:5432/ecommerce_data"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Create the table if it doesn't exist
Session = sessionmaker(bind=engine)
session = Session()  # Creates a session to interact with the database

class EcommercePipeline:
    def process_item(self, item, spider):
        # Extract product details
        title = item['title']
        price = item['price']
        image_url = item['image_url']

        # Download image and save it locally
        image_path = self.download_image(image_url)

        # Save product data to the database
        self.save_to_database(title, price, image_path)

        return item

    def download_image(self, image_url):
        # Create an "images" directory if it doesn't exist
        image_dir = "images"
        os.makedirs(image_dir, exist_ok=True)

        # Extract image name from URL
        image_name = os.path.basename(image_url)
        image_path = os.path.join(image_dir, image_name)

        # Download and save the image
        if not os.path.exists(image_path):
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(response.content)
            else:
                raise DropItem(f"Failed to download image from {image_url}")

        return image_path

    def save_to_database(self, title, price, image_path):
        # Create a Property object and save it to the database
        property = Property(title=title, price=float(price), image_path=image_path)
        try:
            session.add(property)
            session.commit()  # Commit the transaction
        except Exception as e:
            session.rollback()  # Rollback the transaction in case of an error
            raise DropItem(f"Failed to save item {title} to database: {e}")
