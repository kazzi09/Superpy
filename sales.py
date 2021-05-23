import csv, json
from datetime import date, datetime
import matplotlib.pyplot as plt

class Sales_Keeper():
    def __init__(self, path: str, field_names: list):
        self.path = path
        self.field_names = field_names

    def initialize_csv(self):
        with open(self.path, mode='w+') as stock:
            writer = csv.DictWriter(stock, fieldnames=self.field_names)
            writer.writeheader()

            stock.close()

    def sell_product(self, bought_id: int, product_name: str, sell_date: str, sell_price: float, original_price: float):
        with open(self.path, mode='a') as sales:
            writer = csv.DictWriter(sales, fieldnames=self.field_names)
            new_id = open('./data/sales_id.txt', 'r').read()

            writer.writerow({
                'id': new_id, 
                'bought_id': bought_id,
                'product_name': product_name,
                'sell_date': sell_date, 
                'sell_price': sell_price, 
                'original_price': original_price
            })

            sales.close()

            open('./data/sales_id.txt', 'w').write(str(int(new_id) + 1))

            print(f'Sold: id: {new_id}, bought_id: {bought_id}, sell_date: {sell_date}, sell_price: {sell_price}')

    def read_sales(self):
         with open(self.path) as sales:
            reader = csv.DictReader(sales)

            for row in reader:
                print(row)

            sales.close() 

    def report_revenue_or_profit(self, day: str, report_profit = False):
        revenue: float = 0
        sales_cost: float = 0

        with open(self.path) as sales:
            reader = csv.DictReader(sales)
            
            if day == 'today':
                day = open('./data/currentday.txt', 'r').read()

            try:
                givenday = datetime.strptime(day, '%Y-%m-%d')
                givenday = givenday.strftime('%Y-%m-%d')

                for row in reader:
                    if row['sell_date'] == givenday:
                        revenue = revenue + float(row['sell_price'])
                        sales_cost = sales_cost + float(row['original_price'])

            except ValueError as e:
                print(f'{e}. No valid date given.')

            if report_profit:
                profit = revenue - sales_cost
                print(f'The profit for {day} was: €{round(profit, 2)}')
            else:
                 print(f'The revenue for {day} was: €{round(revenue, 2)}')
           
            sales.close()   

    def export_sales_as_json(self):
        data = {}

        with open(self.path, 'r') as sales:
            reader = csv.DictReader(sales)

            for rows in reader:
                key = rows['id']
                data[key] = rows

        with open('data/sales_export.json', 'w+') as json_file:
            json_file.write(json.dumps(data, indent=4))

        print('Data export finished to data/sales_export.json')

    def show_graph(self):
        date_data = []
        graph_data = {}

        with open(self.path) as sales:
            reader = csv.DictReader(sales)

            for rows in reader:
                date_data.append(rows['sell_date'])

            date_data = list(set(date_data))

            sales.close()

        for date in date_data:
            total_price: float = 0
                
            with open(self.path) as sales:
                reader = csv.DictReader(sales)

                for rows in reader:
                    if date == rows['sell_date']:
                        total_price = total_price + float(rows['sell_price'])

            graph_data[date] = round(total_price, 2) 

        graph_data = dict(sorted(graph_data.items()))

        plt.bar(graph_data.keys(), graph_data.values())

        plt.title('SuperPy Sales Data')
        plt.xlabel('sold dates')
        plt.ylabel('total revenue per day')

        plt.show()