import urllib.request

url = 'http://download.geonames.org/export/dump/countryInfo.txt'
response = urllib.request.urlopen(url)

lines = response.read().decode('utf-8').split('\n')

# Strip empty lines and comments
without_comments = list(filter(lambda l: not l.startswith('#') and l, lines))

# Country codes are in the first column of the TSV
ccodes = list(map(lambda l: l.split('\t')[0], without_comments))

for cc in ccodes:
  print(f'Downloading {cc}.zip')
  urllib.request.urlretrieve(f'http://download.geonames.org/export/dump/{cc}.zip', f'./downloads/{cc}.zip')

