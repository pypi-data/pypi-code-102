#!/usr/bin/env python
import argparse
from sarscov2formatter import formatter


def main():
	parser = argparse.ArgumentParser(description='Metadata extractor for SARS-CoV-2 selection analysis pipeline in Galaxy')
	parser.add_argument('-a', '--alignment', dest='alignment', action='store', help='Mulitple sequence alignment file', required=True)
	parser.add_argument('-n', '--ncbimetadata', dest='ncbimetadata', action='store', help='yaml metadata from NCBI. if neither -n nor -m is given it will be downloaded from https://www.ncbi.nlm.nih.gov/projects/genome/sars-cov-2-seqs/ncov-sequences.yaml')
	parser.add_argument('-m', '--metadata', dest='metadata', action='store', help='tabular metadata')
	args = parser.parse_args()

	formatter(args.alignment, args.metadata, args.ncbimetadata)

if __name__ == '__main__':
    exit(main())