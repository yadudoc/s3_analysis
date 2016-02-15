#!/usr/bin/env python
import csv

def load_mapping_csvs(filename) :
    rdr = csv.DictReader(open(filename, 'r'))
    return list(rdr)


def init():
    mappings = load_mapping_csvs("ami_mapping.csv")
    for m in mappings:
        print m

if __name__ == "__main__":
    init()
