# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first/demultiplex_A1P1.py

https://github.com/emybart415/Demultiplex/blob/master/Assignment-the-first/demultiplex_A1P1.py

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz |R1 Biological sequence|101|+33|
| 1294_S1_L008_R2_001.fastq.gz |R2 Index1|8|+33|
| 1294_S1_L008_R3_001.fastq.gz |R3 Index2|8|+33|
| 1294_S1_L008_R4_001.fastq.gz |R4 Biological sequence|101|+33|

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. [R1 Qscore Distribution](https://github.com/emybart415/Demultiplex/blob/master/Assignment-the-first/R1_V2_results.png)
    3. [R2 Index Qscore Distribution](https://github.com/emybart415/Demultiplex/blob/master/Assignment-the-first/R2_V2_results.png)
    4. [R3 Index Qscore Distribution](https://github.com/emybart415/Demultiplex/blob/master/Assignment-the-first/R3_V2_results.png)
    5. [R4 Qscore Distribution](https://github.com/emybart415/Demultiplex/blob/master/Assignment-the-first/R4_V2_results.png)

UPDATE: as of 20230801 scripts are re-running:
Histograms will be at:
/projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/Assignment-the-first as R1_V2_results.png, R2_V2_results.png, R3_V2_results.png, R4_V2_results.png

UPDATE 20230801 14:56 - everything is up to date, linked files are the correct V2 and up on github

- What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer.
```
A good quality score cutoff would be higher for the indices than it would for the sequence. I think 30 would be good for indices because it makes sure that the correct samples are being assigned to the sequence. Since illumin claims Q30 is benchmark, I would like to say a cutoff for biological sequencing data is 30, but I am pretty sure you can get away with a qscore of 25, especially if you have good coverage considering you are pulling an average. I think it would also depend what your goals are for downstream analysis of the sequences. 
```
- How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)
```
zcat 1294_S1_L008_R2_001.fastq.gz | grep -A1 "^@" | grep -v "^@" | grep -v "^--$" | grep "N" | wc -l --> 3976613 indices
zcat 1294_S1_L008_R3_001.fastq.gz | grep -A1 "^@" | grep -v "^@" | grep -v "^--$" | grep "N" | wc -l --> 3328051 indices
```

## Part 2
1. Define the problem

This script will need to move through 4 files in parallel, two with biological sequence data in both a R1 and R2 direction, two with indices as reverse compliments of eachother. The program will need to determine if the indices are a perfect match, too low quality (contain N's), or are "hopped" indices and do not match.
Based on this, it will parse the read 1 data and read 4 data into different files (see bellow) after appending the index to the eand of each reads header in the following format @HEADER INDEX1-(REVCOMP(INDEX2))

2. Describe output
```
-> Need to create >= 6 files:
        - R1 $ R2 FASTQ files for matching/high quality indices (24 for each read)
                -R1_Index 1-24.fq
                -R2_Index 1-24.fq
        - R1 $ R2 FASTQ files for low quality indices (2 total files)
            -R1_lowq.fq
            -R2_lowq.fq
        - R1 $ R2 FASTQ files for hopped indices (2 total files)
            -R1_hopped.fq
            -R2_hopped.fq
```

3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include: 
In Pseudocode file
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
