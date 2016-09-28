import urllib.request
import ast
import csv
import json

class Area:

	def __init__(self, zipcode, total):
		self.zipcode = zipcode
		self.total = total

	def add_info(self, lat, lng):
		self.lat = lat
		self.lng = lng

class ZipInfo:

	def __init__(self, key):
		self.key = key

	def get(self, query, file_type='json'):
		url = 'https://maps.googleapis.com/maps/api/geocode/%s?address=%s&key=%s' % (file_type, query, self.key)
		print(url, '\n')
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		return response.read()

orders = []

f = open('orders.csv')
csv_f = csv.reader(f)

for row in csv_f:
	if row[30] == 'US':
		code = row[29].split('-')[0]
		amount = float(row[12])
		added = False
		for order in orders:
			if order.zipcode == code:
				order.total += amount
				added = True
		if added == False:
			orders.append(Area(code, amount))

f.close()

api_key = "" # read from file

z = ZipInfo(api_key)

for order in orders:
	info = z.get(order.zipcode)
	results = ast.literal_eval(info.decode('utf8'))
	#print(json.dumps(results, sort_keys=True, indent=4))
	lat = results['results'][0]['geometry']['location']['lat']
	lng = results['results'][0]['geometry']['location']['lng']
	order.add_info(lat, lng)

f = "orders_zips.csv"

with open(f, "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow(['Zipcode','Profit','Lat','Lng'])
	for order in orders:
		writer.writerow([str(order.zipcode), str(order.total), str(order.lat), str(order.lng)])

f.close()
