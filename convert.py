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
    names = set(map(lambda str: str.strip(), self.fields[3].split(',')))
    names.add(self.fields[0])

    feature = {
      '@id': f'http://sws.geonames.org/{self.fields[0]}',
      'type': 'Feature',
      'properties': {
        'title': self.fields[1],
        'ccodes': [ self.fields[8] ],
      },
      'names': list(map(lambda str: {
        'toponym': str
      }, names)),
      'geometry': {
        'type': 'Point',
        'coordinates': [
          self.fields[5], self.fields[4]
        ]
      }
    }

    return json.dumps(feature)

def convert_zip(ccode):
  with open(OUTFILE, 'a') as outfile:
    with zipfile.ZipFile(f'./downloads/{ccode}.zip', 'r') as archive:
      with archive.open(f'{ccode}.txt') as f:
        reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
        for row in reader:
          feature = Feature(row)
          outfile.write(f'{feature.to_json()}\n')

def gzip_outfile():
  with open(OUTFILE, 'rb') as infile, gzip.open(f'{OUTFILE}.gz', 'wb') as outfile:
    outfile.writelines(infile)

# Delete outfile (if exists)
try:
  os.remove(OUTFILE)
except OSError:
  pass

# List all Zip files in the downloads folder...
zipfiles = [f for f in glob.glob('./downloads/*.zip')]
ccodes = list(map(lambda f: f[f.rfind('/') + 1 : -4], zipfiles))
ccodes.sort()

# ...convert...
for ccode in ccodes:
  print(f'Converting file {ccode}.zip')
  convert_zip(ccode)

# ...and gzip 
gzip_outfile()

