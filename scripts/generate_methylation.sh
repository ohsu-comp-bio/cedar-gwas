#!/bin/bash

proj=$1

cd $proj
tar -zxvf gdc_download_2018071*.tar.gz
mv */*.txt .

grep 'cg03943081' jhu-usc.edu*.txt | cut -f1,2 > /mnt/cedar/methylation/cg03943081/TCGA-${proj}_cg03943081.tsv
grep 'cg18360873' jhu-usc.edu*.txt | cut -f1,2 > /mnt/cedar/methylation/cg18360873/TCGA-${proj}_cg18360873.tsv

rm jhu*
rmdir *
rm MANIFEST.txt
