import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id_book = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'Book {self.id_book}: ({self.title}, {self.id_publisher})'


class Shop(Base):
    __tablename__ = 'shop'

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):
        return f'Shop {self.id_shop}: {self.name}'


class Stock(Base):
    __tablename__ = 'stock'

    id_stock = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id_book'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id_shop'))
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __str__(self):
        return f'Stock {self.id_stock}: book {self.id_book},shop {self.id_shop},count = {self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id_sale = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id_stock'))
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'Sale {self.id_sale}, prise = {self.price}, date_sale = {self.date_sale}, count = {self.count}'



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
