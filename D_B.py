import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

db = 'postgresql://postgres:postgres@localhost:5432/database'
engine = create_engine(db)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship("Publisher", backref="books")

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('books.id'))
    id_shop = Column(Integer, ForeignKey('shops.id'))
    count = Column(Integer)
    book = relationship("Book", backref="stocks")
    shop = relationship("Shop", backref="stocks")
    
class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date_sale = Column(Date)
    id_stock = Column(Integer, ForeignKey('stocks.id'))
    count = Column(Integer)
    stock = relationship("Stock", backref="sales")

Base.metadata.create_all(engine)

def get_shops(publisher_id_or_name):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale
    ).select_from(
        Stock
    ).join(
        Book
    ).join(
        Publisher
    ).join(
        Sale
    ).join(
        Shop
    )

    if publisher_id_or_name.isdigit():
        publisher_query = query.filter(Publisher.id == int(publisher_id_or_name))
    else:
        publisher_query = query.filter(Publisher.name == publisher_id_or_name)

    results = publisher_query.all()
    for result in results:
        title, shop_name, price, date_sale = result
        print(f"{title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    publisher_info = input("Enter the publisher ID or name: ")
    get_shops(publisher_info)
    session.close()
    engine.dispose()  
