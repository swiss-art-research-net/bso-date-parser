import csv
import sys
import unittest
import os
if 'tests' in os.getcwd():
    sys.path.append('../src')
    examplesFile = "examples.csv"
else:
    sys.path.append('./src')
    examplesFile = "tests/examples.csv"

from sariDateParser.dateParser import parse

examples = []

with open(examplesFile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        examples.append(row)

countErrors = 0
for i, example in enumerate(examples):
    try:
        assert parse(example['input']) == example['output'], example['input'] + " should be " + example['output']
    except AssertionError: 
        countErrors +=1
        sys.stderr.write("%d: %s is %s instead of %s\n" % (i, example['input'], str(parse(example['input'])), example['output']))

print("Completed with %d out of %d tests failed" % (countErrors, len(examples)))