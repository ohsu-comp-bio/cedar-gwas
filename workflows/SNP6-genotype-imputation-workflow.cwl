#!/usr/bin/env cwl-runner
#
# Author: Allison Creason

class: Workflow
cwlVersion: v1.0

doc: "Genotype and Imputation pipeline for SNP6 data"

inputs:

outputs:

steps:

  tar:
    run: ../tools/general/tar.cwl
    in: 
      input:
    out: [output]

  birdsuite:
    run: ../tools/birdsuite/birdsuite.cwl
    in:
    out:

  birdsuite2plink:
    run: ../tools/birdsuite2plink.cwl
    in:
    out:

  eagle:
    run: ../tools/eagle/eagle.cwl
    in:
    out:

  pbwt:
    run: ../tools/pbwt/pbwt.cwl
    in:
    out:
