## Gamze Gursoy ##
##last edit Nov 23rd, 2020
## input arguments
## (1) reference transcriptome
## (2) reference genome
## (3) header
## (4) gtf file
import os
import string
import re
import csv
import zlib, sys, time, base64
import gzip
import numpy as np
import io
from collections import namedtuple
from . import PrintTransSequence
from . import PrintSequence

TranscriptInfo = namedtuple("Transcriptinfo", ["chromosome", "position"])


def getFromGtfandGFa(
    transcript_id, position, length, transcript_search_index, reference_lookup
):
    transcript_info = transcript_search_index[transcript_id]
    chrom = transcript_info.chromosome
    start_position = transcript_info.position + position
    sequence = reference_lookup.query(chrom, start_position - 1, length)
    return sequence


def build_transcript_search_dict(path_to_gtf):
    """Build a dict whose keys are transcript IDs and values are TranscriptInfo instances."""
    search_dict = {}
    with open(path_to_gtf) as fp:
        for line in fp:
            if line.startswith("#"):
                continue
            gtf_record = line.split("\t")
            if gtf_record[2] == "transcript" or gtf_record[2] == "tRNA":
                chromosome = str(gtf_record[0])
                position = int(gtf_record[3])
                transcript_id_raw = gtf_record[8].split()[3]
                transcript_id = re.sub('"|;', "", transcript_id_raw)
                search_dict[transcript_id] = TranscriptInfo(chromosome, position)
    return search_dict


# following is necessary for querying sequences from reference genome
# ref transcriptome
def main():
    with open(sys.argv[1], "rt") as f1:
        ref = PrintTransSequence.Lookup(f1)

    # ref genome
    with open(sys.argv[2], "rt") as f2:
        ref2 = PrintSequence.Lookup(f2)

    bam = []

    # header
    hed = open(sys.argv[3], "r")
    header = []
    for line in hed:
        header.append(line.split("\n")[0])
    hed.close()

    gtf_path = sys.argv[4]
    transcript_search_index = build_transcript_search_dict(gtf_path)

    for i in range(0, len(header)):
        print("%s" % header[i])

    fileB = sys.stdin
    for lineB in fileB:
        p = lineB.rstrip()
        pbam = p.split("\t")
        is_spikein = "Spikein" in pbam[2]
        # Leave spikeins and unaligned as is
        if pbam[2] == "*" or is_spikein:
            print(p)
        if pbam[2] != "*" and (not is_spikein):
            RL = len(pbam[9])
            nColpbam = len(pbam)
            for i in range(0, nColpbam):
                t = pbam[i].split(":")
                if t[0] == "MD":
                    pbam[i] = "MD:Z:" + str(RL)
                if t[0] == "AS":
                    pbam[i] = "AS:i:" + str(RL)
                if t[0] == "NM":
                    pbam[i] = "NM:i:0"
                if t[0] == "nM":
                    pbam[i] = "nM:i:0"
                if t[0] == "MC":
                    pbam[i] = "MC:Z:" + str(RL) + "M"
            chrom = str(pbam[2])
            startPos = int(pbam[3])
            k = ref.query(chrom, startPos - 1, int(RL))
            if k == 0:
                pbam[9] = getFromGtfandGFa(
                    chrom, startPos - 1, int(RL), transcript_search_index, ref2
                )
            else:
                pbam[9] = ref.query(chrom, startPos - 1, int(RL))
            pbam[5] = str(RL) + "M"
            if len(pbam[9]) < int(RL):
                a = int(RL) - len(pbam[9])
                for i in range(0, a):
                    pbam[9] = pbam[9] + "N"
            pbam[9] = pbam[9].upper()
            nbam = str(pbam[0]) + "\t"
            for i in range(1, nColpbam - 1):
                nbam = nbam + str(pbam[i]) + "\t"
            nbam = nbam + str(pbam[nColpbam - 1])
            print(nbam)
            nbam = ""
            bam = []
