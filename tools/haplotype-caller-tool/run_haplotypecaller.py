#!/usr/bin/env python
import argparse
import os
import subprocess

def build_cmd():
    cmd = ["gatk-launch", "--javaOptions", "-Xmx16g", "HaplotypeCaller", "--input", 
            args.input, "--reference", args.reference, "--output", os.path.join(args.workDir,args.output)]

    if args.emitRefConfidence:
        cmd.extend(["--emitRefConfidence",args.emitRefConfidence])

    return cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.add_argument("--input", required=True, help="BAM/SAM/CRAM file containing reads")
    args = parser.add_argument("--reference", required=True, help="Reference sequence file")
    args = parser.add_argument("--emitRefConfidence", required=False)
    args = parser.add_argument("--output", required=True, help="File to which variants should be written")
    args = parser.add_argument("--workDir", default="/work")
    args = parser.parse_args()

    # Run birdsuite
    cmd = build_cmd()
    print "Running Haplotype Caller\n%s" % (" ".join(cmd))
    proc = subprocess.Popen(cmd)
    proc.wait()
