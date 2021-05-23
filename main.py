# Imports
import argparse, json, numpy 
from datetime import date, datetime, timedelta
from stock import Stock
from sales import Sales

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.
def init_stock():
    return Stock(
        path='./data/stock.csv', 
        field_names=['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
    )

def init_sales():
    return Sales(
        path='./data/sold.csv',
        field_names=['id', 'bought_id', 'product_name', 'sell_date', 'sell_price', 'original_price']
    )

def init_cli():
    parser = argparse.ArgumentParser(prog="SuperPy", description=" ")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser('init', help="Initialize SuperPy")
    reinit_parser = subparsers.add_parser('reinit', help="Re Initialize SuperPy")

    buy_parser = subparsers.add_parser('buy', help="Add product to stock")
    buy_parser.add_argument('-n', '--productname', help="Product Name", required=True)
    buy_parser.add_argument('-p', '--buyprice', help="Price", required=True)
    buy_parser.add_argument('-e', '--expirationdate', help="Expiration Date in YYYY-MM-DD", required=True)

    stock_parser = subparsers.add_parser('stock', help="Show products currently in stock")

    sales_parser = subparsers.add_parser('sales', help="Show products sold")

    time_parser = subparsers.add_parser('advancetime', help="Advance time by given days")
    time_parser.add_argument('-d', '--days', help="How many days to advance", default='1')

    testdata_parser = subparsers.add_parser('testdata', help="Fill with test data")

    sell_parser = subparsers.add_parser('sell', help="Sell an item from stock")
    sell_parser.add_argument('-n', '--productname', help='Product Name', required=True)
    sell_parser.add_argument('-p', '--price', help="Sold at price", required=True)

    revenue_parser = subparsers.add_parser('revenue', help="Get revenue for today or yesterday")
    revenue_parser.add_argument('-d', '--day', help="Which day, YYYY-MM-DD", default="today")

    profit_parser = subparsers.add_parser('profit', help="Get revenue for today or yesterday")
    profit_parser.add_argument('-d', '--day', help="Which day, YYYY-MM-DD", default="today")

    clear_stock_parser = subparsers.add_parser('clearstock', help="Remove expired products from stock")

    import_json_parser = subparsers.add_parser('importjson', help="Import old stock from Json file")
    import_json_parser.add_argument('-p', '--path', help="Path to Json file", required=True)

    export_json_parser = subparsers.add_parser('exportjson', help="Export stock or sales data to Json")
    export_json_parser.add_argument('-t', '--type', help="Stock or Sales", required=True)

    graph_parser = subparsers.add_parser('showgraph', help="Show a graph with the desired data")
    graph_parser.add_argument('-t', '--type', help="Stock or Sales", required=True)

    return parser.parse_args()

def reinitialize(stock: Stock, sales: Sales):
    stock.initialize_csv()
    sales.initialize_csv()

    open('./data/stock_id.txt', 'w+').write(str(1))
    open('./data/sales_id.txt', 'w+').write(str(1))

    print('Stock Bot and Sales Bot are reinitialized!')

def add_item_to_stock(product_name, buy_price, expiration_date, stock: Stock):
    try:
        product_name = str(product_name)
    except ValueError as e:
         print(f'{e}. Given name is not a valid string.')
         return

    buy_date = open('./data/currentday.txt', 'r').read()

    try:
        buy_price = float(buy_price)
    except ValueError as e:
        print(f'{e}. Given price is not a number.')
        return
    
    try:
        expiration_date = date.fromisoformat(expiration_date)
    except ValueError as e:
        print(f'{e}. No valid date given.')
        return

    stock.add_product_to_stock(product_name, buy_date, buy_price, expiration_date)

def advance_time(days: int):
    currentday = open('./data/currentday.txt', 'r').read()

    print('Advanced date from: ', currentday)

    currentday = datetime.strptime(open('./data/currentday.txt', 'r').read(), '%Y-%m-%d')
    currentday = currentday + timedelta(days=int(days))
    currentday = currentday.strftime('%Y-%m-%d')

    print('To: ', currentday)

    open('./data/currentday.txt', 'w').write(currentday)

def fill_test_data(stock: Stock, sales: Sales):
    add_item_to_stock('Apples', 4.5, '2021-05-01', stock)
    add_item_to_stock('Oranges', 2.7, '2021-04-29', stock)
    add_item_to_stock('Beer', 8.9, '2022-05-02', stock)
    add_item_to_stock('Tea', 1.2, '2021-12-05', stock)
    add_item_to_stock('Coffee', 2.9, '2021-07-05', stock)

    sell_item('Bacardi', 9.0, stock, sales)
    sell_item('Beer', 12.0, stock, sales)

    advance_time(1)

    add_item_to_stock('Peper', 2.0, '2020-12-05', stock)
    add_item_to_stock('Mint', 1.5, '2020-07-05', stock)
    add_item_to_stock('Strawbeery', 4.0, '2021-07-05', stock)

    sell_item('Strawbeery', 15.0, stock, sales)

def sell_item(product_name: str, sell_price: float, stock: Stock, sales: Sales):
    product_check = stock.check_if_item_is_in_stock_and_not_expired(product_name)

    if product_check == 'not_in_stock':
        print('Item is not in stock.')
        return

    if product_check == 'stock_expired':
        print('Item in stock but expired. It is recommended to clear the stock of expired items.')
        return

    sold_product = stock.remove_product_from_stock_and_return_product(product_name)

    try:
        sell_price = float(sell_price)
    except ValueError as e:
        print(f'{e}. Given price is not a number.')
        return

    sell_date = open('./data/currentday.txt', 'r').read()

    sales.sell_product(sold_product['id'], sold_product['product_name'], sell_date, sell_price, sold_product['buy_price'])

def import_json_file(path: str, stock: Stock):
    with open(path) as json_file:
        data = json.load(json_file)

        stock_data = data['stock']

        for item in stock_data:
            try:
                product_name = str(item['product_name'])
            except ValueError as e:
                print(f'Error, given data is invalid.')
                print(f'{e}. Given name is not a valid string.')
                return

            try:
                buy_date = date.fromisoformat(item['buy_date'])
            except ValueError as e:
                print(f'Error, given data is invalid.')
                print(f'{e}. No valid date given.')
                return

            try:
                buy_price = float(item['buy_price'])
            except ValueError as e:
                print(f'Error, given data is invalid.')
                print(f'{e}. Given price is not a number.')
                return

            try:
                expiration_date = date.fromisoformat(item['expiration_date'])
            except ValueError as e:
                print(f'Error, given data is invalid.')
                print(f'{e}. No valid date given.')
                return

            stock.add_product_to_stock(product_name, buy_date, buy_price, expiration_date)

        print('')
        print(f'Succesfully imported data from {path}.')

def export_json_file(export_type: str, stock: Stock, sales: Sales):
    export_type = export_type.lower()

    if export_type == 'stock':
        stock.export_stock_as_json()
    elif export_type == 'sales':
        sales.export_sales_as_json()
    else:
        print('Type Error in given type.')   

def export_sales_as_graph(graph_type: str, stock: Stock, sales: Sales):
    graph_type = graph_type.lower()

    if graph_type == 'stock':
        stock.show_graph()
    elif graph_type == 'sales':
        sales.show_graph()
    else:
        print('Type Error in given type.')     

def main():
    stock = init_stock()
    sales = init_sales()

    args = init_cli()
    
    print('')

    if (args.command == 'init' or args.command == 'reinit'):
        reinitialize(stock, sales)

    if (args.command == 'buy'):
        add_item_to_stock(args.productname, args.buyprice, args.expirationdate, stock)

    if (args.command == 'stock'):
        stock.read_stock()

    if (args.command == 'sales'):
        sales.read_sales()

    if (args.command == 'advancetime'):
        advance_time(args.days)

    if (args.command == 'testdata'):
        fill_test_data(stock, sales)

    if (args.command == 'sell'):
        sell_item(args.productname, args.price, stock, sales)

    if (args.command == 'revenue'):
        sales.report_revenue_or_profit(args.day)

    if (args.command == 'profit'):
        sales.report_revenue_or_profit(args.day, True)

    if (args.command == 'clearstock'):
        stock.clear_expired_stock()

    if (args.command == "importjson"):
        import_json_file(args.path, stock)

    if (args.command == 'exportjson'):
        export_json_file(args.type, stock, sales)

    if (args.command == 'showgraph'):
        export_sales_as_graph(args.type, stock, sales)

    print('')

if __name__ == '__main__':
    main()