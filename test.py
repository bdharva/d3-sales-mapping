import urllib.request
import ast


class Census:
    def __init__(self, key):
        self.key = key

    def get(self, fields, geo, year=2010, dataset='sf1'):
        fields = [','.join(fields)]
        base_url = 'http://api.census.gov/data/%s/%s?key=%s&get=' % (str(year), dataset, self.key)
        query = fields
        for item in geo:
            query.append(item)
        add_url = '&'.join(query)
        url = base_url + add_url
        print(url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return response.read()

c = Census('25ba8ce4107f486306b9373c337489d563c2a189')
state = c.get(['P0010001'], ['for=state:25'])
# url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&for=state:25
county = c.get(['P0010001'], ['in=state:25', 'for=county:*'])
# url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&in=state:25&for=county:*
city = c.get(['P0010001'], ['in=state:25', 'for=place:*'])
# url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&in=state:25&for=place:*

# Cast result to list type
state_result = ast.literal_eval(state.decode('utf8'))
county_result = ast.literal_eval(county.decode('utf8'))
city_result = ast.literal_eval(city.decode('utf8'))

def count_pop_county():
    count = 0
    for item in county_result[1:]:
        count += int(item[0])
    return count

def count_pop_city():
    count = 0
    for item in city_result[1:]:
        count += int(item[0])
    return count

print(state)
# b'[["P0010001","state"],\n["6547629","25"]]'

print('Total state population:', state_result[1][0])
# Total state population: 6547629

print('Population in all counties', count_pop_county())
# Population in all counties 6547629

print('Population in all cities', count_pop_city())
# Population in all cities 4615402