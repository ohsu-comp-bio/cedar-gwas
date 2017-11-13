#!/usr/bin/env cwl-runner
#
# Author: Allison Creason

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [birdsuite.sh]

doc: "Birdsuite framework for calling SNVs and CNVs from SNP6 genotype arrays"

hints:
    DockerRequirement:
        dockerPull: alliecreason/birdsuite:hg38

requirements:
    - class: InlineJavascriptRequirement

inputs:

    basename:
        type: string
        inputBinding:
            position: 1
            prefix: "--basename="
            separate: false

    celFiles:
        type: Directory
        inputBinding:
            valueFrom: $(inputs.celFiles.listing)
            itemSeparator: " "
            position: 2 

    chipType:
        type: string
        inputBinding:
            position: 1
            prefix: "--chipType="
            separate: false

    genderFile:
        type: File
        inputBinding:
            position: 1
            prefix: "--genderFile="
            separate: false

    canaryPriors:
        type: string
        inputBinding:
            position: 1
            prefix: "--canary.priors="
            separate: false

    canaryAlleleFreqWeight:
        type: int?
        inputBinding:
            position: 1
            prefix: "--canary.allele_freq_weight="
            separate: false

    outputDir:
        type: string
        inputBinding:
            position: 1
            prefix: "--outputDir="
            separate: false

    genomeBuild:
        type: string
        inputBinding:
            position: 1
            prefix: "--genomeBuild="
            separate: false

    aptProbesetSummarize:
        type: boolean
        inputBinding:
            position: 1
            prefix: "--apt_probeset_summarize.force"
            separate: false

    noLsf:
        type: boolean
        inputBinding:
            position: 1
            prefix: "--noLsf"
            separate: false

    firstStep:
        type: int?
        inputBinding:
            position: 1
            prefix: "--firstStep="
            separate: false

    lastStep:
        type: int?
        inputBinding:
            position: 1
            prefix: "--lastStep="
            separate: false

    exeDir:
        type: string
        inputBinding:
            position: 1
            prefix: "--exeDir="
            separate: false

    metadataDir:
        type: string
        inputBinding:
            position: 1
            prefix: "--metadataDir="
            separate: false

outputs:
    outputFiles:
        type: Directory
        outputBinding:
            glob: $(inputs.outputDir + "/")
