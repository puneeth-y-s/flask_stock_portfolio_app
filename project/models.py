from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Stock(Base):
    """
    Class that represents a purchased stock in a portfolio.

    The following attributes of a stock are stored in this table:
        stock symbol (type: string)
        number of shares (type: integer)
        purchase price (type: integer)

    Note: Due to a limitation in the data types supported by SQLite, the
          purchase price is stored as an integer:
              $24.10 -> 2410
              $100.00 -> 10000
              $87.65 -> 8765
    """

    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String)
    number_of_shares = Column(Integer)
    purchase_price = Column(Integer)

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100:.2f}'
    

class User(Base):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)

    REMEMBER: Never store the plaintext password in a database!
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hashed = Column(String(128))

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)
    
    def __repr__(self):
        return f'<User: {self.email}>'