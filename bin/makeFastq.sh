#!/bin/sh

pbam_path=$1

pbam_basename=$(basename "$pbam_path")
pbam_prefix=${pbam_basename%.bam}

samtools view -H "${pbam_path}" > header.txt
samtools view "${pbam_path}" | make_unique > reads.txt
awk '!seen[$1$2$3$4]++' reads.txt > unique_reads.txt
awk '{print $5}' unique_reads.txt > linenumbers.txt
samtools view "${pbam_path}" | print_unique | samtools view -h -bS - > filtered.bam
samtools view filtered.bam | 10x_bam2fastq "${pbam_prefix}"
rm header.txt
rm reads.txt
rm unique_read.txt
rm linenumbers.txt
rm filtered.bam
