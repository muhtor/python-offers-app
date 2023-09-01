import requests
from sqlalchemy import create_engine, Table, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к базе данных SQLite
DATABASE_URL = "sqlite:///products.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение модели данных с помощью ORM
Base = declarative_base()


class Offer(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    merchant = Column(String)
    ram = Column(String)
    rom = Column(String)
    image_url = Column(String)


Base.metadata.create_all(bind=engine)  # Создание таблицы в базе данных (если её ещё нет)

Session = sessionmaker(bind=engine)
session = Session()


# Сохранение данных в базу данных
def create_offer_db(db_session, offer_data):
    attributes = {attr["name"].lower(): attr["value"] for attr in offer_data.get("attributes", [])}

    offer = Offer(
        id=offer_data["id"],
        name=offer_data["name"],
        brand=offer_data["brand"],
        category=offer_data["category"],
        merchant=offer_data["merchant"],
        ram=attributes.get("ram"),
        rom=attributes.get("rom"),
        image_url=offer_data["image"]["url"]
    )

    db_session.add(offer)
    db_session.commit()


# Получение данных с адреса
url = "https://www.kattabozor.uz/hh/test/api/v1/offers"
response = requests.get(url)
data = response.json()

if data:
    for item in data['offers']:
        with SessionLocal() as session:
            create_offer_db(session, item)
