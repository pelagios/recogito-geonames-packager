import csv
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

with zipfile.ZipFile('./downloads/AT.zip', 'r') as archive:
  with archive.open('AT.txt') as f:
    reader = csv.reader(io.TextIOWrapper(f), delimiter='\t')
    for row in reader:
      feature = Feature(row)
      print(feature.to_json())
