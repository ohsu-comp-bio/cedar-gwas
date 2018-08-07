from __future__ import print_function

import argparse
import json
import os
import requests


def fetch_mapping():
    payload = {
        "filters":{
            "op": "and",
            "content": [
                {
                    "op":"in",
                    "content": {
                        "field": "experimental_strategy",
                        "value": [
                            "Genotyping array"
                        ]
                    }
                },
                {
                    "op": "in",
                    "content": {
                        "field": "platform",
                        "value": [
                            "Affymetrix SNP Array 6.0"
                        ]
                    }
                },
                {
                    "op": "in",
                    "content": {
                        "field": "data_format",
                        "value": [
                            "CEL"
                        ]
                    }
                },
                {
                    "op": "in",
                    "content": {
                        "field": "cases.project.program.name",
                        "value": [
                            "TCGA"
                        ]
                    }
                }
            ]
        },
        "format": "JSON",
        "fields": "file_name,cases.samples.sample_type,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id,cases.demographic.gender,cases.project.project_id,cases.samples.sample_id,cases.samples.submitter_id,cases.case_id,cases.submitter_id",
        "size":"50000"
    }
    response = requests.post("https://api.gdc.cancer.gov/legacy/files", json=payload)
    response.raise_for_status()
    return response.json()

def transform(args):
    """
    Example hit:
    {
      "file_name": "DLP_REDO_FROM_SHOUT_A04.CEL",
      "cases": [
        {
          "project": {
            "project_id": "TCGA-LGG"
          },
          "case_id": "738f5c96-ee44-4fd7-bb8c-e2b86f8053c8",
          "demographic": {
            "gender": "female"
          },
          "samples": [
            {
              "portions": [
                {
                  "analytes": [
                    {
                      "aliquots": [
                        {
                          "submitter_id": "TCGA-FG-A60L-01A-12D-A31K-01"
                        }
                      ]
                    }
                  ]
                }
              ],
              "sample_type": "Primary Tumor",
              "sample_id": "b82e8a8b-1274-4c00-a264-962ee6e5dd21"
            }
          ]
        }
      ],
      "id": "64131536-f0f7-46ed-821a-606463372bff"
    }
    """

    if args.input_file is not None:
        with open(args.input_file) as fh:
            json_data = fh.read()

        data = json.loads(json_data)
    else:
        data = fetch_mapping()

    if not os.path.exists(os.path.dirname(args.output_prefix)):
        os.makedirs(os.path.dirname(args.output_prefix))

    vfile = open(args.output_prefix + ".Vertex.json", "w")
    efile = open(args.output_prefix + ".Edge.json", "w")    

    i = 0
    for hit in data["data"]["hits"]:
      vertex = {
          "gid": "celfile:" + hit["file_name"],
          "label": "CELFile",
          "data": {
              "source": "gdc",
              "cel_file": hit["file_name"],
              "project": hit["cases"][0]["project"]["project_id"],
              "individual_id": hit["cases"][0]["case_id"],
              "individual_barcode": hit["cases"][0]["submitter_id"],
              "aliquot_id": hit["cases"][0]["samples"][0]["portions"][0]["analytes"][0]["aliquots"][0]["aliquot_id"],
              "aliquot_barcode": hit["cases"][0]["samples"][0]["portions"][0]["analytes"][0]["aliquots"][0]["submitter_id"],
              "sample_type": hit["cases"][0]["samples"][0]["sample_type"],
              "sample_id":  hit["cases"][0]["samples"][0]["sample_id"],
              "sample_barcode":  hit["cases"][0]["samples"][0]["submitter_id"]
          }
      }
      vfile.write(json.dumps(vertex)+"\n")
      edge = {
          "gid": "(%s)--%s->(%s)" % (
              vertex["gid"],
              "fileFor",
              "biosample:" + args.biosample_source + ":" + vertex["data"]["sample_barcode"]
          ),
          "label": "fileFor",
          "from": vertex["gid"],
          "to": "biosample:" + args.biosample_source + ":" + vertex["data"]["sample_barcode"],
      }
      efile.write(json.dumps(edge)+"\n")
      if i % 1000 == 0:
          print("Processed", i, "records...")
      i +=1

    vfile.close()
    efile.close()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        "-i",
        help="Input JSON file created from calls to the GDC API"
    )
    parser.add_argument(
        "-o", 
        "--output-prefix", 
        default="celfile.tcga",
        help="Prefix to use for output files"
    )
    parser.add_argument(
        "-s", 
        "--biosample-source", 
        default="tcga",
        help="Biosample source"
    )
    args = parser.parse_args()
    args.output_prefix = os.path.abspath(args.output_prefix)
    transform(args)
