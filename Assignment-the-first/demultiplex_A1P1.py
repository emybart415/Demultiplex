#!/usr/bin/env python

#starting files
#location: /projects/bgmp/shared/2017_sequencing/
# 1294_S1_L008_R1_001.fastq.gz
# 1294_S1_L008_R2_001.fastq.gz
# 1294_S1_L008_R3_001.fastq.gz
# 1294_S1_L008_R4_001.fastq.gz

import argparse
import gzip
import bioinfo
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt

def get_args():
    '''This function gets arguments about FASTA files to be parsed'''
    parser = argparse.ArgumentParser(description="Retrieves the FASTA file")
    parser.add_argument("-f", "--file_name", help = "Input File", required = True)
    parser.add_argument("-l", "--read_length", type = int, help = "Read Length", required = True)
    parser.add_argument("-o", "--output_file", help = "Output File", required = True)
    args = parser.parse_args()
    return args

'''Set global varibles'''
args = get_args()
filename = args.file_name
read_length: int = args.read_length
outfile = args.output_file

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    i = 0
    while i <= read_length:
        lst.append(value)
        i+=1
    return lst

my_list: list = []
my_list = init_list(my_list)


def populate_list(file: str) -> 'tuple[list, int]':
    """This function takes a fast Q file and calculates the sum of the quality score for each base pair index"""
    num_lines = 0
    my_list: list = []
    my_list = init_list(my_list)

    with gzip.open (filename, "rt") as fh:
            for line in fh: 
                num_lines += 1 #counts number of lines
            
                if num_lines%4==0: #use only the 4th line of the record that contains quality scores
                    phred_scores = line.strip() #strip newline characters
                    for i, character in enumerate(phred_scores): #iterate over each quality score character
                        my_list[i] += bioinfo.convert_phred(character) #convert quality scores to phred scores and add the quality scores to my_list
    return my_list,num_lines # return list of quality scores (my_list) and line count (num_lines)

my_list, num_lines = populate_list(filename)

for i, value in enumerate(my_list):
    mean_list= value/(num_lines/4)
    my_list[i]=mean_list 


plt.bar(range(len(my_list)), my_list)
plt.title('Mean PHRED Score for Each Nucleotide Location')
plt.xlabel('Nucleotide Location')
plt.ylabel('Mean Quality Score')
plt.ylim(0,45)
plt.savefig(f'{args.output_file}.png')