#!/usr/bin/env python
import argparse
import json
import os
import tarfile
import subprocess
import glob

def build_cmd():
    celFiles = os.path.join(args.inputsDir,args.celFiles)
    genderFile = os.path.join(args.inputsDir,args.genderFile)

    cmd = ["birdsuite.sh", "--basename=" + basename, "--celFiles=" + celFiles, "--genderFile=" + 
    genderFile, "--chipType=" + args.chipType, "--canary.priors=" + args.canaryPriors, 
    "--canary.allele_freq_weight=" + str(args.canaryAlleleFreqWeight), "--outputDir=" + args.outputDir,
    "--genomeBuild=" + args.genomeBuild, "--firstStep=" + str(args.firstStep), "--lastStep=" + 
    str(args.lastStep), "--exeDir=" + args.exeDir, "--metadataDir=" + args.metadataDir]

    if args.aptProbesetSummarize:
        cmd.append("--apt_probeset_summarize.force")

    if args.noLsf:
        cmd.append("--noLsf")

    return cmd

def write_inputs(inputsDir,response,cels,gender):
    response = json.load(open(response))
    hits = response['data']['hits']

    c = open(os.path.join(inputsDir,cels), "w")
    g = open(os.path.join(inputsDir,gender), "w")

    c.write("cel_files\n")
    g.write("gender\n")

    for hit in hits:
        c.write(os.path.join(inputsDir,hit['file_name']) + "\n")
        if hit['cases'][0]['demographic']['gender'] == 'female':
            g.write("0\n")
        elif hit['cases'][0]['demographic']['gender'] == 'male':
            g.write("1\n")
        else:
            g.write("2\n")

    c.close()
    g.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.add_argument("response")
    args = parser.add_argument("plate")
    args = parser.add_argument("--basename")
    args = parser.add_argument("--celFiles", default="cels.txt")
    args = parser.add_argument("--genderFile", default="gender.txt")
    args = parser.add_argument("--chipType", default="GenomeWideSNP_6")
    args = parser.add_argument("--canaryPriors", default="GenomeWideSNP_6.canary_priors")
    args = parser.add_argument("--canaryAlleleFreqWeight", default=32)
    args = parser.add_argument("--outputDir", default="/opt/output")
    args = parser.add_argument("--genomeBuild", default="hg38")
    args = parser.add_argument("--aptProbesetSummarize", default=False)
    args = parser.add_argument("--noLsf", default=True)
    args = parser.add_argument("--firstStep", default=1)
    args = parser.add_argument("--lastStep", default=12)
    args = parser.add_argument("--exeDir", default="/opt/birdsuite/bin")
    args = parser.add_argument("--metadataDir", default="/opt/metadata")
    args = parser.add_argument("--inputsDir", default="/opt/inputs")
    args = parser.parse_args()

    if args.basename:
        basename = args.basename
    else:
        basename = os.path.basename(args.plate).split("_")[0]

    # Uncompress data
    print "Extracting tarball"
    tar = tarfile.open(args.plate)
    tar.extractall()
    tar.close()

    # Move to inputs dir
    print "Moving files to inputs dir"
    cels = glob.glob("./*/*.CEL")
    for cel in cels:
        os.rename(os.path.abspath(cel),os.path.join(args.inputsDir,os.path.basename(cel)))

    # Write input files
    print "Writing cels and gender files"
    write_inputs(args.inputsDir, args.response, args.celFiles, args.genderFile)

    # Run birdsuite
    cmd = build_cmd()
    print "Running Birdsuite\n%s" % (cmd)
    proc = subprocess.Popen(cmd)
    #stdout, stderr = proc.communicate()
