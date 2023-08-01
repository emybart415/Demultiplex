De Multiplexing Lab Notebook

#Known Index 
#File location: /projects/bgmp/shared/2017_sequencing
# B1	GTAGCGTA    A5	CGATCGAT    C1	GATCAAGG
# B9	AACAGCGA    C9	TAGCCATG    C3	CGGTAATC
# B3	CTCTGGAT    C4	TACCGGAT    A11	CTAGCTCA
# C7	CACTTCAC    B2	GCTACTCT    A1	ACGATCAG
# B7	TATGGCAC    A3	TGTTCCGT    B4	GTCCTAAG
# A12	TCGACAAG    C10	TCTTCGAC    A2	ATCATGCG
# C2	ATCGTGGT    A10	TCGAGAGT    B8	TCGGATTC
# A7	GATCTTGC    B10	AGAGTCCA    A8	AGGATAGC

#starting files
#File Location: /projects/bgmp/shared/2017_sequencing
# 1294_S1_L008_R1_001.fastq.gz -> R1 Biological sequence (101 bp)
# 1294_S1_L008_R2_001.fastq.gz -> R2 Index (8 bp)
# 1294_S1_L008_R3_001.fastq.gz -> R3 Index (8 bp)
# 1294_S1_L008_R4_001.fastq.gz -> R4 Biological Sequence (101 bp)


Original data explorataion:

```zcat 1294_S1_L008_R1_001.fastq.gz | head```
-> @K00337:83:HJKJNBBXX:8:1101:1265:1191 1:N:0:1
```zcat 1294_S1_L008_R2_001.fastq.gz | head```
-> @K00337:83:HJKJNBBXX:8:1101:1265:1191 2:N:0:1
```zcat 1294_S1_L008_R3_001.fastq.gz | head```
-> @K00337:83:HJKJNBBXX:8:1101:1265:1191 3:N:0:1
```zcat 1294_S1_L008_R4_001.fastq.gz | head```
-> @K00337:83:HJKJNBBXX:8:1101:1265:1191 4:N:0:1 --> The first read (first 4 lines of every file) are tied to the same cluster, they have the same header except for the 4* in 4:N:0:1

Phred encoding:
+33
-> Quality score include >,J,F which correalte on the ascii table to +33 encoding

```zcat 1294_S1_L008_R4_001.fastq.gz | wc -l```
-> 1452986940
```zcat 1294_S1_L008_R1_001.fastq.gz | wc -l &```
[1] 2648853 
-> 1452986940
```zcat 1294_S1_L008_R2_001.fastq.gz | wc -l &```
[2] 2648910 
-> 1452986940
```zcat 1294_S1_L008_R3_001.fastq.gz | wc -l &```
[3] 2648914

- How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)
```
zcat 1294_S1_L008_R2_001.fastq.gz | grep -A1 "^@" | grep -v "^@" | grep -v "^--$" | grep "N" | wc -l --> 3976613 indices
zcat 1294_S1_L008_R3_001.fastq.gz | grep -A1 "^@" | grep -v "^@" | grep -v "^--$" | grep "N" | wc -l --> 3328051 indices

Test FastQ Files

R1_testfile.fq
R2_testfile.fq
R3_testfile.fq
R4_testfile.fq
    Read 1 - N
    Read 2 - hopped
    Read 3 - MATCH
    Read 4 - MATCH

▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼
ಠ_ಠ

Python Script: /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py
s batch bash script: /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/A1P1.sh
- For the bash scripy you need to go in and change:
    -#SBATCH --error=R4_error.err the name of the error
    - '-f' location of the input fastq file 
    - '-l' read length of sequence in fatsq file
    - '-o' location and the name you want your output file to be, should reflect name of input file 

Quick run down:
- Created python script to move through fastq file, find and analyze quality score line. Cover qscores to their numerical value from ascii scores (using functions in bioninfo.py). Mean qscore is calculated along NUCLEOTIDE position, and that is stored in a list where the value is the nuclotide position, and the value is the mean qscore.
- Added argparse to py script so you can easily denote input file location/name, read length, output file location/name
    <python script location/name> -f <location/name of input fatsq> -l <read length> -o <location/name of output file(s)>
- To reun we need to create a bash (.sh) script to use to que on a HPT, you will include the above bash command with argparse in your file along with all of the SBATCH commands 


August 1st, 2023
-> Submitted batch job 23956 for R1
-> Submitted batch job 23957 for R2
-> Submitted batch job 23958 for R3
-> Submitted batch job 23959 for R4

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -l 101 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R1_results"
	User time (seconds): 5358.84
	System time (seconds): 8.49
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:29:39
	Maximum resident set size (kbytes): 68376
	Page size (bytes): 4096
	Exit status: 0
    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R1_results.png

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -l 8 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R2_results"
	User time (seconds): 742.44
	System time (seconds): 2.20
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 12:28.60
	Maximum resident set size (kbytes): 77432
	Page size (bytes): 4096
	Exit status: 0
    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R2_results.png

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -l 8 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R3_results"
	User time (seconds): 857.29
	System time (seconds): 2.13
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 14:20.68
	Maximum resident set size (kbytes): 64280
	Page size (bytes): 4096
	Exit status: 0
    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R3_results.png

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -l 101 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R4_results"
	User time (seconds): 5355.23
	System time (seconds): 10.12
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:29:37
	Maximum resident set size (kbytes): 71680
	Page size (bytes): 4096
	Exit status: 0
    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R4_results.png