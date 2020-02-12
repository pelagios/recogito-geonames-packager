# recogito2-places-geonames-all

Code to generate a gazetteer file from all of GeoNames.

## What this does

1. Pulls the list of country codes from <http://download.geonames.org/export/dump/countryInfo.txt>
2. Downloads the dump for each country into the `downloads` folder (warning: this will take a while)
3. Goes through the CSV for every country and...
   - creates a Linked Places JSON record for each row
   - appends the record to the result [JSONL](http://jsonlines.org/) file
