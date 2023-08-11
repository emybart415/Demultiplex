De Multiplexing Lab Notebook

#Known Index 
```
#File location: /projects/bgmp/shared/2017_sequencing
#B1	GTAGCGTA    A5	CGATCGAT    C1	GATCAAGG
#B9	AACAGCGA    C9	TAGCCATG    C3	CGGTAATC
#B3	CTCTGGAT    C4	TACCGGAT    A11	CTAGCTCA
#C7	CACTTCAC    B2	GCTACTCT    A1	ACGATCAG
#B7	TATGGCAC    A3	TGTTCCGT    B4	GTCCTAAG
#A12	TCGACAAG    C10	TCTTCGAC    A2	ATCATGCG
#C2	ATCGTGGT    A10	TCGAGAGT    B8	TCGGATTC
#A7	GATCTTGC    B10	AGAGTCCA    A8	AGGATAGC
```

#starting files
```
#File Location: /projects/bgmp/shared/2017_sequencing
#1294_S1_L008_R1_001.fastq.gz -> R1 Biological sequence (101 bp)
#1294_S1_L008_R2_001.fastq.gz -> R2 Index (8 bp)
#1294_S1_L008_R3_001.fastq.gz -> R3 Index (8 bp)
#1294_S1_L008_R4_001.fastq.gz -> R4 Biological Sequence (101 bp)
```

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

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R1_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R2_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R3_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R4_results.png

Everything worked but histograms look incorrect! 1.4e10 max qscore mean on y axis
- realized its because i failed to divide my num_lines by 4


    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R1_V2_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R2_V2_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R3_V2_results.png

    -> Reulted in /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R4_V2_results.png

Resubmitted jobs:
sbatch A1P1.sh
Submitted batch job 23990 - R1
sbatch A1P1.sh
Submitted batch job 23991 - R4
sbatch A1P1.sh
Submitted batch job 23992 - R2
sbatch A1P1.sh
Submitted batch job 23993 - R3

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -l 101 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R1_V2_results"
	User time (seconds): 5091.57
	System time (seconds): 8.25
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:25:17
	Maximum resident set size (kbytes): 67444
	Page size (bytes): 4096
	Exit status: 0

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -l 8 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R2_V2_results"
	User time (seconds): 729.37
	System time (seconds): 2.00
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 12:13.73
	Maximum resident set size (kbytes): 73824
	Page size (bytes): 4096
	Exit status: 0

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -l 8 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R3_V2_results"
	User time (seconds): 725.62
	System time (seconds): 2.10
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 12:08.46
	Maximum resident set size (kbytes): 74700
	Page size (bytes): 4096
	Exit status: 0

	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -l 101 -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/R4_V2_results"
	User time (seconds): 5076.57
	System time (seconds): 10.05
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:24:59
	Maximum resident set size (kbytes): 71040
	Page size (bytes): 4096
	Exit status: 0

▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼
August 10, 2023
▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼△▼▼△▼△▼△▼△▼△▼

Final script location: /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/demultiplexing_A3.py
Inputs:
R1 Biological sequence
R2 Index
R3 Index
R4 Biological Sequence
Known index file (tab separated, with Indices in 5th column)

Outputs:
-o output file with a summary (.txt form)
Hopped Reads.tsv
Matched Reads.tsv

SBATCH Script location: /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/A3.sh
sbatch ./A3.sh
Submitted batch job 27595
-> Worked successfully, BUT I had my header inside my loop writing to my TSV output files. So after every data line there was a whole header line. 
->Fixed and re-ran

sbatch ./A3.sh
Submitted batch job 28489
-> When I fixed the above problem, I forgot to add new line characters. Fixed and re-ran.

sbatch ./A3.sh 
Submitted batch job 28493
	Command being timed: "/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/demultiplexing_A3.py -a /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -b /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -c /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -d /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -o /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third/2017_summary_1 -k /projects/bgmp/shared/2017_sequencing/indexes.txt"
	User time (seconds): 3000.81
	System time (seconds): 68.68
	Percent of CPU this job got: 62%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:21:22
	Maximum resident set size (kbytes): 288124
	Page size (bytes): 4096
	Exit status: 0

Created:
3 output files: 
Location -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-third
Names:  2017_summary_1.txt , 'Hopped Reads.tsv', 'Matched Reads.tsv' 
52 FATSTQ files

Summary of results:
Total Number of Reads Parsed:
363246735
Total Number of Matched Reads:
331755033
Total Number of Reads Considered to Have Unknown or Low Quality Indices:
30783962
Percent of Total Reads with Indices Considered Low Quality:
8.474669978795541%
Total Number of Reads with Index Hopped Indices:
707740
Percent of Total Reads with Index Hopped Indices:
0.19483726398807136%
Index Pair that hopped the most: ('TATGGCAC', 'TGTTCCGT')	88571	12.51462401446859%
Most "matched" reads had the following index: TACCGGAT	76363857	23.018145741288574%

---Overall this looks like a decent run. Would have liked my low quality and unknown indices to be lower than 8% of the total read number, but it isnt the worst. The hopping rate is low, which is good. Meaning if anything it could be the sequencer needs a PM, but overall labratory protocol and environment for wet lab work is sufficient. 
---Choosing low quality cutoff: Others chose to do a low quality cutoff for the indices based on qscore or average qscore. I figured this was unnecessary because quality trimming of the individual sequences can be done later on. Also with illumina data, the final result is based off of the cumulation of reads. If a specific biological read had truly been low quality, downstream anaylysis could solve some of those problems. 

