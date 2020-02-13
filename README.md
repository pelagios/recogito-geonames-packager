# Recogito2 Gazetteer Package: GeoNames-All

Code to generate a gazetteer package from the [full GeoNames download](http://download.geonames.org/export/dump/readme.txt). The gazetter file format is compliant with the [Linked Places specification](https://github.com/LinkedPasts/linked-places).

This repository contains two Python scripts:

- `download.py` downloads all country ZIP files to the `./downloads` folder (this can take a while)
- `convert.py` generates the dump file `./output/geonames_all.lpf.jsonl` in [JSONL](http://jsonlines.org/) format

## Configuring the Build

The build can be configured to contain a specific country (or list of countries only) __TODO__

## Note to Recogito Maintainers

The full gazetteer package is a fairly large dataset. We recommend importing it first into a new & empty Recogito instance.
Incremental updates are fine, but updating an existing instance with the full dump is __not recommended__ on a production
instance. (Instead, create a clone of the instance, make the update there, and then switch indices.)

## TODO

- Add continents and non-country features
- Merge natural earth polygon shapes
- World continent borders from the [UCLA Geoportal](http://gis.ucla.edu/geodata/dataset/continent_ln)