from flask import render_template , request, session, url_for, redirect, flash, current_app
from pydantic import BaseModel, field_validator, ValidationError
from . import stocks_blueprint
from project.db import get_db_session
from project.models import Stock
import click

class StockModel(BaseModel):
    """Class for parsing new stock data from a form."""
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('Stock symbol must be 1-5 characters')
        return value.upper()


@stocks_blueprint.route("/", methods=['GET'])
def index():
    return render_template("stocks/index.html")

@stocks_blueprint.route('/add_stock', methods=["GET", "POST"])
def add_stock():
    if request.method == "POST":

        for key, value in request.form.items():\
            print(f"{key}: {value}")
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            
            # Save the form data to the database
            with get_db_session() as session:
                new_stock = Stock(stock_data.stock_symbol,
                                stock_data.number_of_shares,
                                stock_data.purchase_price)
                session.add(new_stock)
                session.commit()
            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')
            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)
    return render_template("stocks/add_stock.html")


@stocks_blueprint.route('/stocks/')
def list_stocks():
    with get_db_session() as session:
        stocks = session.query(Stock).order_by(Stock.id).all()
    return render_template('stocks/stocks.html', stocks=stocks)


@stocks_blueprint.cli.command('create_default_set')
def create_default_set():
    """Create three new stocks and add them to the database"""
    stock1 = Stock('HD', '25', '247.29')
    stock2 = Stock('TWTR', '230', '31.89')
    stock3 = Stock('DIS', '65', '118.77')
    with get_db_session() as session:
        session.add(stock1)
        session.add(stock2)
        session.add(stock3)
        session.commit()

@stocks_blueprint.cli.command('create')
@click.argument('symbol')
@click.argument('number_of_shares')
@click.argument('purchase_price')
def create(symbol, number_of_shares, purchase_price):
    """Create a new stock and add it to the database"""
    stock = Stock(symbol, number_of_shares, purchase_price)
    with get_db_session() as session:
        session.add(stock)
        session.commit()
    