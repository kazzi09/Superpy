import csv, json, os
from datetime import date, datetime
import matplotlib.pyplot as plt

class Stock:
    def __init__(self, path: str, field_names: list):
        self.field_names = field_names
        self.path = path
        
    def initialize_csv(self):
        with open(self.path, mode='w+') as stock:
            writer = csv.DictWriter(stock, fieldnames=self.field_names)
            writer.writeheader()

            stock.close()
            
    def add_product_to_stock(self, product_name: str, buy_date: str, buy_price: float, expiration_date: str):
        with open(self.path, mode='a') as stock:
            writer = csv.DictWriter(stock, fieldnames=self.field_names)
            new_id = open('./data/stock_id.txt', 'r').read()

            writer.writerow({
                'id': new_id, 
                'product_name': product_name, 
                'buy_date': buy_date, 
                'buy_price': buy_price, 
                'expiration_date': expiration_date
            })

            stock.close()

            open('./data/stock_id.txt', 'w').write(str(int(new_id) + 1))

            print(f'Added: id: {new_id}, product_name: {product_name}, buy_date: {buy_date}, buy_price: {buy_price}, expiration_date: {expiration_date}')

    def read_stock(self):
         with open(self.path) as stock:
            reader = csv.DictReader(stock)

            for row in reader:
                print(row)

            stock.close()     

    def check_if_item_is_in_stock(self, product_name: str):
        with open(self.path) as stock:
            reader = csv.DictReader(stock)

            for row in reader:
                if row['product_name'] == product_name:
                    stock.close()
                    return True
                
            stock.close()
            return False

    def check_if_item_is_in_stock_and_not_expired(self, product_name: str):
        currentday = datetime.strptime(open('./data/currentday.txt', 'r').read(), '%Y-%m-%d')

        with open(self.path) as stock:
            reader = csv.DictReader(stock)

            for row in reader:
                if row['product_name'] == product_name:
                    expirationdate = datetime.strptime(row['expiration_date'], '%Y-%m-%d')

                    if expirationdate > currentday:
                        return 'stock_not_expired'
                    else:
                        return 'stock_expired'

        return 'not_in_stock'        

    def remove_product_from_stock_and_return_product(self, product_name: str):
        product: dict
        product_is_sold = False

        with open(self.path, 'r') as inp, open('./data/new.csv', 'w+') as out:
            reader = csv.DictReader(inp)

            writer = csv.DictWriter(out, fieldnames=self.field_names)
            writer.writeheader()

            for row in reader:
                if row['product_name'] != product_name:
                    writer.writerow(row)
                else:
                    if product_is_sold:
                        writer.writerow(row)
                    else:
                        product = row
                        product_is_sold = True
                   
        os.remove(self.path)
        os.rename('./data/new.csv', self.path)

        return product

    def clear_expired_stock(self):
        currentday = datetime.strptime(open('./data/currentday.txt', 'r').read(), '%Y-%m-%d')

        with open(self.path, 'r') as inp, open('./data/new.csv', 'w+') as out:
            reader = csv.DictReader(inp)

            writer = csv.DictWriter(out, fieldnames=self.field_names)
            writer.writeheader()

            for row in reader:
                expirationdate = datetime.strptime(row['expiration_date'], '%Y-%m-%d')

                if expirationdate > currentday:
                    writer.writerow(row)
                else:
                    print(f'Product: {row["product_name"]} with id: {row["id"]} has expired and is removed.')

        os.remove(self.path)
        os.rename('./data/new.csv', self.path)

    def export_stock_as_json(self):
        data = {}

        with open(self.path, 'r') as stock:
            reader = csv.DictReader(stock)

            for rows in reader:
                key = rows['id']
                data[key] = rows

        with open('data/stock_export.json', 'w+') as json_file:
            json_file.write(json.dumps(data, indent=4))

        print('Data export finished to data/stock_export.json')

    def show_graph(self):
        date_data = []
        graph_data = {}

        with open(self.path) as stock:
            reader = csv.DictReader(stock)

            for rows in reader:
                date_data.append(rows['buy_date'])

            date_data = list(set(date_data))

            stock.close()

        for date in date_data:
            total_price: float = 0
                
            with open(self.path) as stock:
                reader = csv.DictReader(stock)

                for rows in reader:
                    if date == rows['buy_date']:
                        total_price = total_price + float(rows['buy_price'])

            graph_data[date] = round(total_price, 2) 

        graph_data = dict(sorted(graph_data.items()))

        plt.bar(graph_data.keys(), graph_data.values())

        plt.title('SuperPy Stock Data')
        plt.xlabel('bought dates')
        plt.ylabel('total bought price per day')

        plt.show()