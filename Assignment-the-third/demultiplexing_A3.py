#!/usr/bin/env python

#-----------------------------------------------------------------------------------------------------------------------------------
#                             Implement Argparse
#-----------------------------------------------------------------------------------------------------------------------------------

import argparse
import gzip
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="CHANGE ME")

parser.add_argument("-a", "--r1", type=str, help="filename of 1st biological read", required=True)
parser.add_argument("-b", "--i1", type=str, help="filename of first index read", required=True)
parser.add_argument("-c", "--i2", type=str, help="filename of second index read", required=True)
parser.add_argument("-d", "--r2", type=str, help="filename of 2nd biological read", required=True)
parser.add_argument("-k", "--ki", type=str, help="filename of known indices", required=True)
parser.add_argument("-o", type=str, help="outfile name", required=True)
args = parser.parse_args()

# Global variables
read1 = args.r1
index1 = args.i1
index2 = args.i2
read2 = args.r2
known_i=args.ki
outfile = args.o

#to execute script use ->
#./demultiplexing_A3.py
# -a <1st biological read file loc/name> -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/TEST-input_FASTQ/R1_testfile.fq
# -b <1st index read file loc/name> -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/TEST-input_FASTQ/R2_testfile.fq
# -c <2nd index read file loc/name> -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/TEST-input_FASTQ/R3_testfile.fq
# -d <2nd biological read file loc/name> -> /projects/bgmp/ebart/bioinfo/Bi622/Demultiplex/Demultiplex/TEST-input_FASTQ/R4_testfile.fq
# -o <outfile location/filename>
# -k <known indices file loc/name -> /projects/bgmp/shared/2017_sequencing/indexes.txt

#Need to make sure if the input files are zipped, opens need to be "gzip.open" and the mode has to be "t"

#-------------------------------------------------------------------------------------------------------------------------------------------
#Start zero counts for the number of reads with indices that fall into the bellow catagories
lowq_reads = 0 #reads where an "N" appears in an index or an index (dual matched) doesnt match the known list of indices
hopped_reads = 0 #reads where the index isnt the same across the entitre read, likely index hopping had occured
matched_reads = 0 #reads where the indices match

#Make dictionaries:
#to hold indices that are matched, and total number of reads with that index
#to hold indices that are hopped, total number hopped with that index

matched_dict = {}#key: index, Value: number of times read is considered matched
hopped_dict = {}#key: index, Value: number of times read is considered hopped
#-------------------------------------------------------------------------------------------------------------------------------------------
#                FUNCTIONS
#-------------------------------------------------------------------------------------------------------------------------------------------
def reverse_comp(dna_seq):
    '''This function takes a string of DNA, turns it into its reverse compliment using a dictionary of complimentary base pairs'''
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N' : 'N'}
    reverse_comp_seq = ''.join(complement_dict[base] for base in reversed(dna_seq))
    return reverse_comp_seq

def make_filehandles(known_indices_list: list[str]):
# def make_filehandles(known_indices_list) -> dict[str, (_io.TextIOWrapper, _io.TextIOWrapper)]:
    '''This function take a list of indices plus "lowq" and "hopped" and creates a forward(R1) and reverse(R2) file and filehandle for each item in the list
    it then adds this to a dictionary where the indices, lowq, and hopped are the values, and the two file handles are the values'''
    fh_dict = {}
    for index in known_indices_list:
        fh_r1 = open(f'{index}.R1.fq', 'w')
        fh_r2 = open(f'{index}.R2.fq', 'w')
        fh_dict[index]=(fh_r1, fh_r2)
        #print(f"debug 456 {type(fh_r1)=}")
    return fh_dict

#-------------------------------------------------------------------------------------------------------------------------------------------
#                Set Up Know Indices 
#-------------------------------------------------------------------------------------------------------------------------------------------
#Input: File location and name of file with the known indices for this run, this script was designed for a tab separted
#document with the dindexes stored in the 5th column

#create a list of all the known indices plus a low quality and a hopped catagory
#list of strings
known_indices_list = [] #create a new list to hold the indices in known indices files
known_indices_list.append('lowq') #add "lowq" to list in preparation of making file handles
known_indices_list.append('hopped') #add "lowq" to list in preparation of making file handles

#using a known indices file (as a tab separated file with indices in the 5th column) and add "hopped" and "lowq" to create file handles with those names
with open(f'{known_i}', 'r') as fh1: #open known indices file
    lines = fh1.readlines()
    for line in lines[1:]: #for each line in the file (starting at the second line)
        indices = line.strip().split('\t')[4] #split the lines by their white space wich is tab separated and grab the 5th column
        known_indices_list.append(indices) #append indices to known_indices_list

#Call the 'make_filehandles' function on our known idex+lowq+hopped list
#Turn the dictionary the 'make_filehandles' function created into a variable
#keys: indices as a string
#values: Tuple of forward and reverse file handles 
fh_dict = make_filehandles(known_indices_list)

#-------------------------------------------------------------------------------------------------------------------------------------------
#                Open Read 1, Read 2, Read 3, and Read 4 input files
#-------------------------------------------------------------------------------------------------------------------------------------------
#Open the inut files, move through in parallel and assign variables based on the standard FASTQ setup

with gzip.open(read1, 'rt') as r1, gzip.open(index1, 'rt') as i1, gzip.open(index2, 'rt') as i2, gzip.open(read2, 'rt') as r2:
    while True:#loop through 4 lines at a time and assign a corresponding label
        header_r1=r1.readline().strip()
        seq_r1=r1.readline().strip()
        plus_r1=r1.readline().strip()
        qual_r1=r1.readline().strip()

        header_i1=i1.readline().strip()
        seq_i1=i1.readline().strip()
        plus_i1=i1.readline().strip()
        qual_i1=i1.readline().strip()

        header_i2=i2.readline().strip()
        seq_i2=reverse_comp(i2.readline().strip())
        plus_i2=i2.readline().strip()
        qual_i2=i2.readline().strip()

        header_r2=r2.readline().strip()
        seq_r2=r2.readline().strip()
        plus_r2=r2.readline().strip()
        qual_r2=r2.readline().strip()

        if header_r1 == '' or header_i1 == '' or header_i2 == '' or header_r2 == '': #break when you get to the end of the fastq files
            break
#-------------------------------------------------------------------------------------------------------------------------------------------
#                Write to the Files
#-------------------------------------------------------------------------------------------------------------------------------------------
#Write the reads with a modified header to the output files stored in the fh_dict dictionary
#Header midified to include "index1-index2" at the end of the reads header
#Each read will be put into a fastq file that:
#      Holds reads with low quality and unknown indices, both fwd and rev
#      Holds reads where the dual matched indices dont match, both rwd and rev
#      Holds reads where the indices match, they will be paresed to the fastq file corresponding to the reads index, both fwd and rev

        lowq='lowq'#Set as vaiable so you can call it as such when accessing dictionary
        hopped='hopped'#Set as vaiable so you can call it as such when accessing dictionary

        if seq_i1 not in fh_dict or seq_i2 not in fh_dict: #check if read falls into lowq index catagory
            appended_header_r1 = header_r1 + " " + seq_i1 + "-" + seq_i2
            appended_header_r2 = header_r2 + " " + seq_i1 + "-" + seq_i2
            fh_dict[lowq][0].write((f'{appended_header_r1}\n{seq_r1}\n{plus_r1}\n{qual_r1}\n'))
            fh_dict[lowq][1].write((f'{appended_header_r2}\n{seq_r2}\n{plus_r2}\n{qual_r2}\n'))
            lowq_reads+=1 #keep a count of the number of reads that fall into this catagory

        elif seq_i1 != seq_i2: #check if read falls into hopped index catagory
            appended_header_r1 = header_r1 + " " + seq_i1 + "-" + seq_i2
            appended_header_r2 = header_r2 + " " + seq_i1 + "-" + seq_i2
            fh_dict[hopped][0].write((f'{appended_header_r1}\n{seq_r1}\n{plus_r1}\n{qual_r1}\n'))
            fh_dict[hopped][1].write((f'{appended_header_r2}\n{seq_r2}\n{plus_r2}\n{qual_r2}\n'))
            hopped_reads+=1 #keep a count of the number of reads that fall into this catagory
            if (seq_i1,seq_i2) not in hopped_dict: #increment hopped dict count by one if index already in dict, if not start the counter at 1
                hopped_dict[(seq_i1,seq_i2)] = 1
            else:
                hopped_dict[(seq_i1,seq_i2)] += 1
#f'{seq_i1} : {seq_i2}'
        else: #all else should be matched and paresed into corresponding index FATSQ
            appended_header_r1 = header_r1 + " " + seq_i1 + "-" + seq_i2
            appended_header_r2 = header_r2 + " " + seq_i1 + "-" + seq_i2
            fh_dict[seq_i1][0].write((f'{appended_header_r1}\n{seq_r1}\n{plus_r1}\n{qual_r1}\n'))
            fh_dict[seq_i2][1].write((f'{appended_header_r2}\n{seq_r2}\n{plus_r2}\n{qual_r2}\n'))
            matched_reads+=1 #keep a count of the number of reads that fall into this catagory
            if seq_i1 not in matched_dict: #increment matched dict count by one if index already in dict, if not start the counter at 1
                matched_dict[seq_i1] = 1
            else:
                matched_dict[seq_i1] += 1

#----------------------------------------------------------------------------------------------------------------------------------
#                Create human readable summary
#----------------------------------------------------------------------------------------------------------------------------------
#currently working with
#lowq_reads - total number of reads considered lowq
#hopped_reads - total number of reads considered hopped
#matched_reads - total number of reads considered matched
total_reads=lowq_reads+hopped_reads+matched_reads
percent_lowq=(lowq_reads/total_reads)*100
percent_hopped=(hopped_reads/total_reads)*100

# print(hopped_dict)
# print(matched_dict)
print(lowq_reads)
print(hopped_reads)
print(matched_reads)
print(total_reads)
with open('Hopped Reads.tsv', 'w') as fh1:
    fh1.write(f'Hopped Index Pairs\n')
    fh1.write(f'Hopped Indices\t#Reads with Index\tPercentage of total Hopped Reads\n\n')
    for key in hopped_dict:
        x=hopped_dict[key]
        percents=(((hopped_dict[key])/(hopped_reads))*100)
        fh1.write(f'{key}\t{x}\t{percents}%\n')

with open('Matched Reads.tsv', 'w') as fh2:
    fh2.write(f'Number of Reads With Each Index\n')
    fh2.write(f'Index\t#Reads with Index\tPercentage of total Matched Reads\n\n')
    for key in matched_dict:
        x2=matched_dict[key]
        percents2=(((matched_dict[key])/(matched_reads))*100)
        fh2.write(f'{key}\t{x2}\t{percents2}%\n')

with open(f'{outfile}.txt', 'w') as fout:
    fout.write(f'Summary:\n\nTotal Number of Reads Parsed:\n{total_reads}\n\n')
    fout.write(f'Total Number of Matched Reads:\n{matched_reads}\n\n')
    fout.write(f'Total Number of Reads Considered to Have Unknown or Low Quality Indices:\n{lowq_reads}\n\n')
    fout.write(f'Percent of Total Reads with Indices Considered Low Quality:\n{percent_lowq}%\n\n')
    fout.write(f'Total Number of Reads with Index Hopped Indices:\n{hopped_reads}\n\n')
    fout.write(f'Percent of Total Reads with Index Hopped Indices:\n{percent_hopped}%\n\n\n')
    fout.write(f'----------------------------------------------------------------------------------------------------------\n')
    fout.write(f'To see a comprehesive list of matched index pairs, see "Matched Reads.tsv"\n')
    fout.write(f'To see a comprehesive list of hopped index pairs, see "Hopped Reads.tsv"\n')
