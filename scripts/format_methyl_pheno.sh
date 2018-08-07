#!/bin/bash

proj=$1
pheno=$2
proj2=$(echo $proj | cut -f2 -d-)

sed "s/:${pheno}//" /mnt/cedar/methylation/${pheno}/${proj}_${pheno}.tsv > tmp && mv tmp /mnt/cedar/methylation/${pheno}/${proj}_${pheno}.tsv

join -1 1 -2 1 <(sort -k1 /mnt/cedar/methylation/${pheno}/${proj}_${pheno}.tsv) <(sort /mnt/cedar/requests/${proj2}/${proj}_methyl_mapping.tsv) | awk '{print$3"\t"$2}' | sort -k1,1 -u > tmp && mv tmp /mnt/cedar/methylation/${pheno}/${proj}_${pheno}.tsv

join -1 1 -2 1 <(sort -k1 /mnt/cedar/plink/chr10/${proj}_barcode_all_merged_20180501.chr10.imputed.dose.fam) <(sort -k1 /mnt/cedar/methylation/${pheno}/${proj}_${pheno}.tsv) | cut -f1,2,7 -d ' ' | sort -k1,1 -u | sed 's/ /\t/g' > /mnt/cedar/methylation/${pheno}/${proj}_${pheno}_joined.tsv
