import csv
import sys
import unittest
sys.path.append('../src')

examplesFile = "examples.csv"

from sariDateParser.dateParser import parse

examples = []

with open(examplesFile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        examples.append(row)

for i, example in enumerate(examples):
    try:
        assert parse(example['input']) == example['output'], example['input'] + " should be " + example['output']
    except AssertionError: 
        sys.stderr.write("%d: %s is %s instead of %s\n" % (i, example['input'], str(parse(example['input'])), example['output']))