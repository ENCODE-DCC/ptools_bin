#!/bin/sh



bam_path=$1
gref=$2
tref=$3
gtf=$4

bam_basename=$(basename "$bam_path")
bam_prefix=${bam_basename%.bam}

samtools view -H "${bam_path}" > header.txt
samtools view "${bam_path}" | pbam_mapped_transcriptome "${tref}" "${gref}" header.txt "${gtf}" | samtools view -h -bS > "${bam_prefix}".p.bam
rm header.txt
