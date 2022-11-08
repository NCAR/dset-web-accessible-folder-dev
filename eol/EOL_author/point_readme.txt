
EOL datasets with data from a site will have a bounding box of a single point.
This will throw an error when first harvested by CKAN.
Subsequent harvests this will no long throw an error.
The point data is used correctly by CKAN, so disregard these error msgs.

