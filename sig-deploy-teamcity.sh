#!/bin/bash
echo -e "This scripts downloads the latest zip url of a release zip to https://portal.sig.eu\n"

# get the current date
date_yymmdd=$(date +%Y%m%d)

zip_name=deltares_overstroomik_backend_${date_yymmdd}.zip

echo "filling ${zip_name}"


# add the whole directory
zip -r ${zip_name} .

echo -e "\nNow upload ${zip_name} to https://portal.sig.eu in separate build step\n"
