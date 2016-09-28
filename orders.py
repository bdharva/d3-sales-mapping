import urllib.request, ast, csv, json

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
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		return response.read()

orders = []

with open('orders.csv', newline='') as csvfile:
	csv_f = csv.reader(csvfile)
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

with open('api_keys.json') as json_data:
	d = json.load(json_data)
	api_key = (d['google'])

z = ZipInfo(api_key)

for order in orders:
	info = z.get(order.zipcode)
	results = ast.literal_eval(info.decode('utf8'))
	lat = results['results'][0]['geometry']['location']['lat']
	lng = results['results'][0]['geometry']['location']['lng']
	order.add_info(lat, lng)

f = "orders_zips.csv"

with open(f, "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow(['Zipcode','Profit','Lat','Lng'])
	for order in orders:
		writer.writerow([str(order.zipcode), str(order.total), str(order.lat), str(order.lng)])
