#!/usr/bin/env python

import argparse
import json
import requests
import os

def format_payload(plate):
    payload = {
        "filters": {
            "op":"in",
            "content": {
                "field":"files.file_name",
                "value": [
                    "%s*.CEL" % (plate)
                ]
            }
        },
        "format":"JSON",
        "fields":"file_id,file_name,cases.demographic.gender,cases.demographic.race,cases.samples.sample_type",
        "size":"50000"
    }
    return payload

def post_request(payload):
    endpoint = 'https://api.gdc.cancer.gov/v0/legacy/files'
    headers = {"Content-Type": "application/json"}
    response = requests.post(endpoint, data=json.dumps(payload),headers=headers)
    with open(os.path.join(args.workdir,"response.json"),"w") as r:
        json.dump(response.json(),r)
    return response

def format_ids(response):
    hits = response.json()['data']['hits']
    ids = list()
    for hit in hits:
        ids.append(hit['file_id'])
 
    ids = {"ids": ids}
    return ids

def download(ids,token,plate):
    endpoint = 'https://api.gdc.cancer.gov/v0/legacy/data'
    headers = {'X-Auth-Token': '%s' % (token),
        "Content-Type": "application/json"}
    response = requests.post(endpoint, data=json.dumps(ids), headers=headers,stream=True)

    handle = open(os.path.join(args.workdir,plate + "_gdc_cels.tar.gz"),"wb")
    for chunk in response.iter_content(chunk_size=1024):
        handle.write(chunk)
    handle.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("plate")
    parser.add_argument("token")
    parser.add_argument("--workdir", required=False, default="./")

    args = parser.parse_args()

    token_file = open(args.token,"r")
    token = token_file.read().rstrip()

    if not os.path.exists(args.workdir):
        os.makedirs(args.workdir)
    payload = format_payload(args.plate)
    response = post_request(payload)
    ids = format_ids(response)
    download(ids, token, args.plate)
