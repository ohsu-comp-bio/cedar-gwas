from __future__ import print_function

import argparse
import aql
import json
import os

from bmeg import conversions


def run(args):
    conn = aql.Connection(args.arachne)
    O = conn.graph(args.graph)
    ensembl_id = conversions.hugo_ensembl(args.gene)
    gid = "gene:" + ensembl_id
    
    sample_mutation_status = {}

    query =  O.query().V(gid).\
             in_("variantIn").mark("variant").\
             out("variantCall").where(aql.eq("method", "MUTECT")).mark("callset").\
             out("callSetOf").where(aql.eq("sample_type", "Primary Tumor")).mark("sample").\
             in_("fileFor").mark("cel")
    if args.project is not None:
        query = query.where(aql.eq("project", args.project))
    query = query.mark("cel").\
            select(["variant", "sample", "callset", "cel"])

    for res in query:
        if res.variant.data.alternateBases != res.variant.data.referenceBases:
            if res.cel.data.individual_barcode not in sample_mutation_status:
                sample_mutation_status[res.cel.data.individual_barcode] = 1

    query = O.query().V().where(aql.eq("_label", "CELFile"))
    if args.project is not None:
        query = query.where(aql.eq("project", args.project))

    for res in query:
        if res.data.individual_barcode not in sample_mutation_status:
            sample_mutation_status[res.data.individual_barcode] = 0
    
    for k in sample_mutation_status:
        print(k, k, sample_mutation_status[k], sep="\t")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--arachne",
        "-a",
        default="http://localhost:80",
        help="arachne server"
    )
    parser.add_argument(
        "--graph",
        "-G",
        default="cedar",
        help="graph to query"
    )
    parser.add_argument(
        "--gene",
        "-g",
        type=str, 
        required=True,
        help="gene to check for variant in"
    )
    parser.add_argument(
        "--project",
        "-p",
        type=str, 
        help="TCGA project (e.g. BRCA)"
    )

    args = parser.parse_args()
    run(args)
