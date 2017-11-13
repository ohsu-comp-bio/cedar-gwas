#!/bin/bash

PLATE_NAMES=$1
TOKEN=$2


PWD=$(pwd)
SCRIPTS="/mnt/cedar-gwas/scripts"
CONTAINER="cedar-gwas"
THREADS=4

cat $PLATE_NAMES | xargs -n 5 | while read plates; do
    echo "Running $plates"

    for plate in $plates; do

        echo "Downloading CEL files from GDC for plate $plate" && \
        $SCRIPTS/download_gdc_data.py --workdir $PWD/$plate $plate $TOKEN && \
        echo "Uploading $plate to object store" && \
        swift upload --object-threads $THREADS --object-name $plate $CONTAINER $PWD/$plate && \
        echo "Cleaning up $plate files" && \
        rm -rf $PWD/$plate &

    done
    wait

done
