import urllib.request, ast, csv, json

class Area:

	def __init__(self, zipcode, total):
		self.zipcode = zipcode
		self.total = total

	def add_info(self, lat, lng):
		self.lat = lat
		self.lng = lng

	def add_demos(self, queries):
		self.demos = []
		for item in queries:
			self.demos.append(item)

class ZipInfo:

	def __init__(self, key):
		self.key = key

	def get(self, query, file_type='json'):
		url = 'https://maps.googleapis.com/maps/api/geocode/%s?address=%s&key=%s' % (file_type, query, self.key)
		req = urllib.request.Request(url)
		response = urllib.request.urlopen(req)
		return response.read()

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
	api_key_c = (d['census'])
	api_key_g = (d['google'])

c = Census(api_key_c)
z = ZipInfo(api_key_g)

query_for = [
	'DP05_0001E',	# total population
	'DP05_0017E',	# median age
	'DP05_0032PE',	# race:white (%)
	'DP03_0062E',	# median household income
	'DP02_0064PE',	# bachelors degree (%)
	'DP02_0065PE'	# graduate degree (%)
	]

for order in orders:
	info = z.get(order.zipcode)
	results = ast.literal_eval(info.decode('utf8'))
	lat = results['results'][0]['geometry']['location']['lat']
	lng = results['results'][0]['geometry']['location']['lng']
	order.add_info(lat, lng)
	info = c.get(query_for, ['for=zip+code+tabulation+area:'+order.zipcode])
	try:
		results = ast.literal_eval(info.decode('utf8'))
	except:
		for x in range(0, len(query_for)):
			demos.append('null')
		order.add_demos(demos)
		continue
	else:
		demos = []
		for x in range(0, len(query_for)):
			demos.append(results[1][x])
		order.add_demos(demos)

with open('orders_demos.csv', 'w') as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow(['Zipcode','Profit','Lat','Lng','Population','Median-Age','Race-White','Median-Household-Income','Bachelors-Degree','Graduate-Degree'])
	for order in orders:
		writer.writerow([str(order.zipcode), str(order.total), str(order.lat), str(order.lng), str(order.demos[0]), str(order.demos[1]), str(order.demos[2]), str(order.demos[3]), str(order.demos[4]), str(order.demos[5])])
