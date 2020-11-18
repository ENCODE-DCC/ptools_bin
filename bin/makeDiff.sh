#### Gamze Gursoy #####

bam_path=$1

bam_basename=$(basename "$bam_path")
bam_prefix=${bam_basename%.bam}

samtools view "${bam_path}" | createDiff > temp.diff

compress temp.diff "${bam_prefix}".diff
rm temp.diff
