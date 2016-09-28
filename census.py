import urllib.request
import ast
import csv

class Area:
    def __init__(self, zipcode, total):
        self.zipcode = zipcode
        self.total = total
    def add_demos(self, queries):
    	self.demos = []
    	for item in queries:
    		self.demos.append(item)
	def add_info(self, queries):
		self.info = []
    	for item in queries:
    		self.info.append(item)

class Census:
    def __init__(self, key):
        self.key = key

    def get(self, fields, geo, year=2014, dataset='acs5'):
        fields = [','.join(fields)]
        base_url = 'http://api.census.gov/data/%s/%s/profile?get=' % (str(year), dataset)
        query = fields
        for item in geo:
            query.append(item)
        add_url = '&'.join(query)
        key_url = '&key=' + self.key
        url = base_url + add_url + key_url
        print(url, '\n')
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return response.read()

f = open('orders.csv')
csv_f = csv.reader(f)

orders = []

for row in csv_f:
	if row[30] == 'US' and row[28] == 'MA':
		code = row[29].split('-')[0]
		amount = float(row[12])
		added = False
		for order in orders:
			if order.zipcode == code:
				order.total += amount
				added = True
		if added == False:
			orders.append(Area(code, amount))


for order in orders:
	print(order.zipcode, order.total)

api_key = "" # read from file

c = Census(api_key)

query_for = [	'DP05_0001E',	# total population
				'DP05_0017E',	# median age
				'DP05_0032PE',	# race:white (%)
				'DP03_0062E', 	# median household income
				'DP02_0064PE', 	# bachelors degree (%)
				'DP02_0065PE'	# graduate degree (%)
			]

for order in orders:
	zipcode = c.get(query_for, ['for=zip+code+tabulation+area:'+order.zipcode])
	results = ast.literal_eval(zipcode.decode('utf8'))
	order.add_demos([results[1][0], results[1][1], results[1][2], results[1][3], results[1][4]])
	print('ZIPCODE:', order.zipcode)
	print('----------')
	print('Population:', order.demos[0])
	print('Median Age:', order.demos[1])
	print('Race (white):', order.demos[2], '%')
	print('Median Household Income: $' + order.demos[3])
	print('Bachelors Degree:', order.demos[4], '%')


f2 = "orders_demos.csv"

with open(f2, "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow(['Zipcode','Profit','Population','Age','Race','Bachelors','Graduate'])
	for order in orders:
		writer.writerow([str(order.zipcode), str(order.total), str(order.demos[0]), str(order.demos[1]), str(order.demos[2]), str(order.demos[3]), str(order.demos[4])])
