import csv
import glob
import io
import json
import zipfile

class Feature:

  def __init__(self, csv):
    self.fields = csv

  def to_json(self):
    feature = {
      '@id': f'http://sws.geonames.org/{self.fields[0]}',
      'type': 'Feature',
      'properties': {
        'title': self.fields[1],
        'ccodes': [ self.fields[8] ],
      },
      'names': [
        { 'toponym': self.fields[1] }
      ],
      'geometry': {
        'type': 'Point',
        'coordinates': [
          self.fields[5], self.fields[4]
        ]
      }
    }

    # TODO alternateNames fields[3]

    return json.dumps(feature)

def convert_zip(ccode):
  with open('./output/geonames_all.lpf.jsonl', 'a') as outfile:
    with zipfile.ZipFile(f'./downloads/{ccode}.zip', 'r') as archive:
      with archive.open(f'{ccode}.txt') as f:
        reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
        for row in reader:
          feature = Feature(row)
          outfile.write(f'{feature.to_json()}\n')

# TODO delete outfile

zipfiles = [f for f in glob.glob('./downloads/*.zip')]
for f in zipfiles:
  ccode = f[f.rfind('/') + 1 : -4]  

  print(f'Converting file {f}')
  convert_zip(ccode)

