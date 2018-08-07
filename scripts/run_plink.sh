#!/bin/bash

proj=$1
pheno=$2

plink --bfile /mnt/cedar/plink/chr10/${proj}_barcode_all_merged_20180501.chr10.imputed.dose --pheno /mnt/cedar/methylation/${pheno}/${proj}_${pheno}_joined.tsv --R /mnt/cedar/cedar-gwas/scripts/Rplink.spearman.correlation.R --noweb --maf 0.1 --hwe 1e-8  --out /mnt/cedar/plink/chr10/${proj}_${pheno}_chr10

sed 's/^ \+//' /mnt/cedar/plink/chr10/${proj}_${pheno}_chr10.auto.R | sed 's/ \+/\t/g' | sed 's/\t$//' > tmp && mv tmp /mnt/cedar/plink/chr10/${proj}_${pheno}_chr10.auto.R

sed -i "1iCHR\tSNP\tBP\tA1\tCOEF\tP\tLCI\tUCI" /mnt/cedar/plink/chr10/${proj}_${pheno}_chr10.auto.R

Rscript /mnt/cedar/cedar-gwas/scripts/make_manhattan.R --project ${proj} --phenotype ${pheno}  --chromosome chr10 --file /mnt/cedar/plink/chr10/${proj}_${pheno}_chr10.auto.R
