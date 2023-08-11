#!/usr/bin/bash

#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --cpus-per-task=1                 #optional: number of cpus, default is 1
#SBATCH --mem=8GB                        #optional: amount of memory, default is 4GB
#SBATCH --error=demultiplex.err


/usr/bin/time -v /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/demultiplexing_A3.py \
    -a /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
    -b /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
    -c /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
    -d /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
    -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/2017_summary_1 \
    -k /projects/bgmp/shared/2017_sequencing/indexes.txt



# -a <1st biological read file loc/name> -> /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz
# -b <1st index read file loc/name> -> /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz
# -c <2nd index read file loc/name> -> /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz
# -d <2nd biological read file loc/name> -> /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz
# -o <outfile location/filename> -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third
# -k <known indices file loc/name -> /projects/bgmp/shared/2017_sequencing/indexes.txt
