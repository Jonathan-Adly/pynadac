import requests
import json

import argparse

# create a parser object
parser = argparse.ArgumentParser(
    description="This program takes an NDC list as input and return the latest NADAC_per_unit price for each"
)


# add argument
parser.add_argument(
    "ndc",
    nargs="*",
    metavar="NDC",
    type=str,
    help="All the NDC given seperated by a space will be processed",
)

# parse the arguments from standard input
args = parser.parse_args()

# check if add argument has any input data.
# If it has, then do the request and add the NADAC price to result list
if len(args.ndc) != 0:

    url = "https://data.medicaid.gov/api/1/datastore/query/dfa2ab14-06c2-457a-9e36-5cb6d80f8d93/0/"
    payload = {
        "keys": "true",
        "offset": "0",
        "properties": [
            "ndc_description",
            "ndc",
            "nadac_per_unit",
            "pricing_unit",
            "as_of_date",
        ],
        "conditions": [
            {
                "property": "ndc",
                "value": args.ndc,
                "operator": "in",
            }
        ],
        "sorts": [
            {"property": "as_of_date", "order": "desc"},
            {"property": "ndc_description", "order": "desc"},
        ],
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, json=payload, headers=headers).content
    results = json.loads(response)["results"]
    seen = []
    new_list = []

    for item in results:
        if not item["ndc_description"] in seen:
            new_list.append(item)
            seen.append(item["ndc_description"])

    print(new_list)


else:
    print("You didn't enter an NDC")
