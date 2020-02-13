# Recogito2 Gazetteer Package: GeoNames-All

Code to generate a gazetteer package from the [full GeoNames download](http://download.geonames.org/export/dump/readme.txt). The gazetter file format is compliant with the [Linked Places specification](https://github.com/LinkedPasts/linked-places).

This repository contains two Python scripts:

- `download.py` downloads all country ZIP files to the `./downloads` folder (this can take a while)
- `convert.py` generates the dump file `./output/geonames_all.lpf.jsonl` in [JSONL](http://jsonlines.org/) format

## TODO

- Add continents and non-country features
- Merge natural earth polygon shapes
- World continent borders from the [UCLA Geoportal](http://gis.ucla.edu/geodata/dataset/continent_ln)