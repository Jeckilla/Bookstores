import sqlalchemy
from sqlalchemy.orm import sessionmaker

from config import login, password, host, port, db_name

from models import create_tables, Publisher, Book, Sale, Stock, Shop

dict_of_conf = {'login': login, 'password': password, 'host': host, 'port': port, 'database': db_name}
DSN = f'postgresql://{dict_of_conf["login"]}:{dict_of_conf["password"]}@{dict_of_conf["host"]}:{dict_of_conf["port"]}/{dict_of_conf["database"]}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Pushkin')
publisher2 = Publisher(name='Lermontov')
publisher3 = Publisher(name='Tolstoy')

session.add_all([publisher1, publisher2, publisher3])
session.commit()

print('Publishers ids')
print(publisher1.id)
print(publisher2.id)
print(publisher3.id)

book1 = Book(title='The Queen of spades', id_publisher=1)
book2 = Book(title='The captain`s daughter', id_publisher=1)
book3 = Book(title='The Hero of our time', id_publisher=2)
book6 = Book(title='Mcyri', id_publisher=2)
book4 = Book(title='The Sunday', id_publisher=3)
book5 = Book(title='The War and Peace', id_publisher=3)
session.add_all([book1, book2, book3, book4, book5, book6])
session.commit()

print('Books ids')
print(book1.id_book)
print(book2.id_book)
print(book3.id_book)
print(book4.id_book)
print(book5.id_book)
print(book6.id_book)

shop1 = Shop(name='AkademBook')
shop2 = Shop(name='FictionBook')
shop3 = Shop(name='ClassicBook')
session.add_all([shop1, shop2, shop3])
session.commit()

stock1 = Stock(id_book=1, id_shop=1, count=200)
stock2 = Stock(id_book=2, id_shop=1, count=3200)
stock3 = Stock(id_book=5, id_shop=1, count=300)
stock4 = Stock(id_book=3, id_shop=2, count=700)
stock5 = Stock(id_book=4, id_shop=3, count=1300)
stock6 = Stock(id_book=6, id_shop=2, count=200)
session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])
session.commit()

sale1 = Sale(price=300, date_sale='2023-04-12', id_stock=1, count=10)
sale2 = Sale(price=350, date_sale='2023-04-15', id_stock=1, count=12)
sale3 = Sale(price=250, date_sale='2023-05-25', id_stock=2, count=5)
sale4 = Sale(price=450, date_sale='2023-05-01', id_stock=3, count=21)
sale5 = Sale(price=400, date_sale='2023-05-05', id_stock=5, count=11)
sale6 = Sale(price=400, date_sale='2023-05-14', id_stock=5, count=25)
sale7 = Sale(price=400, date_sale='2023-05-14', id_stock=6, count=15)
sale8 = Sale(price=200, date_sale='2023-05-03', id_stock=4, count=10)
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8])
session.commit()



def buy_books_of_publisher():
    publisher = input("Введите фамилию издателя/автора: ") #запрашиваю только имя, потому что поиск так обычно происходит
    for q in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Publisher, Publisher.id == Book.id_publisher)\
        .join(Stock, Book.id_book == Stock.id_book)\
        .join(Shop, Stock.id_shop == Shop.id_shop)\
        .join(Sale, Stock.id_stock == Sale.id_stock)\
        .filter(Publisher.name == publisher).all():

        title, name, price, date_sale = q
        print(f'{title}, {name}, {price}, {date_sale}')

buy_books_of_publisher()


session.close()
