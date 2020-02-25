import csv
import glob
import gzip
import io
import json
import os
import zipfile
import config as cfg

OUTFILE = f'./output/{cfg.outfile}.lpf.jsonl'

class Feature:

  def __init__(self, csv):
    self.fields = csv

  def to_json(self):

    def parse_num(str):
      s = str.strip()
      return int(s) if s else None

    names = set(map(lambda str: str.strip(), self.fields[3].split(',')))
    names.add(self.fields[1])

    # Remove empty strings (in case the 'alternate names' column was empty!)
    names = list(filter(None, names))

    admin_codes = map(lambda idx: self.fields[idx], range(10, 13))
    admin_codes = list(filter(lambda c: c.strip(), admin_codes))

    feature = {
      '@id': f'http://sws.geonames.org/{self.fields[0]}',
      'type': 'Feature',
      'properties': {
        'title': self.fields[1],
        'ccodes': [ self.fields[8] ],
        'admin_codes': admin_codes,
        'feature_class': self.fields[6],
        'feature_code': self.fields[7],
        'population': parse_num(self.fields[14]), 
        'elevation': parse_num(self.fields[15])
      },
      'names': list(map(lambda str: {
        'toponym': str
      }, names)),
      'geometry': {
        'type': 'Point',
        'coordinates': [
          float(self.fields[5]), float(self.fields[4])
        ]
      }
    }

    return json.dumps(feature)

class Concordances:

  #  link concordances from the alternateNamesV2.zip file
  def __init__(self):
    print('Building concordance table (may take a while)')
    self.concordances = {}

    with zipfile.ZipFile('./downloads/alternateNamesV2.zip', 'r') as archive:
      with archive.open('alternateNamesV2.txt') as f:
        reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')

        for row in reader:
          if row[2] == 'link' or row[2] == 'wkdt':
            gn_id = row[1]
            if gn_id in self.concordances:
              self.concordances[gn_id].append(row[2])
            else:
              self.concordances[gn_id] = [ row[2] ]

        print(f'Collected {len(self.concordances)} concordance links')

  # Checks if there is a concordance for the given GeoNames ID
  def includes(self, gn_id):
    return self.concordances[gn_id] if gn_id in self.concordances else None

def convert_zip(ccode, maybe_concordances):
  with open(OUTFILE, 'a') as outfile:
    with zipfile.ZipFile(f'./downloads/{ccode}.zip', 'r') as archive:
      with archive.open(f'{ccode}.txt') as f:
        reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')

        ctr = 0
        for row in reader:
          if (not maybe_concordances or maybe_concordances.includes(row[0])):
            feature = Feature(row)
            outfile.write(f'{feature.to_json()}\n')
            ctr += 1

        return ctr

def gzip_outfile():
  with open(OUTFILE, 'rb') as infile, gzip.open(f'{OUTFILE}.gz', 'wb') as outfile:
    outfile.writelines(infile)

# Delete outfile (if exists)
try:
  os.remove(OUTFILE)
except OSError:
  pass

maybe_concordances = Concordances() if cfg.require_concordance else None

# List all Zip files in the downloads folder...
zipfiles = [f for f in glob.glob('./downloads/*.zip')]
ccodes = list(map(lambda f: f[f.rfind('/') + 1 : -4], zipfiles))

# Filter according to settings
if len(cfg.countries) > 0:
  ccodes = list(filter(lambda ccode: ccode in cfg.countries, ccodes))

ccodes.sort()

# ...convert...
ctr = 0
for ccode in ccodes:
  print(f'Converting file {ccode}.zip')
  ctr += convert_zip(ccode, maybe_concordances)

print(f'Converted {ctr} records')

# ...and gzip 
print('GZipping...')
gzip_outfile()
print('Done.')

