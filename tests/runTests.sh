#!/bin/bash
currentdir=$(pwd)
if [[ $currentdir =~ "tests" ]]
then
    srcdir=../src
    testsdir=.
else
    srcdir=./src
    testsdir=./tests
fi

echo "Running tests..."
getopts v flag

echo "Running tests in source code"
for f in $(find $srcdir -type f -name '*.py' -follow -print)
do
    python3 $f -$flag
done

read -p "Run test cases? (y/n)" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Running test cases"
  python3 $testsdir/testExamples.py
fi

echo "All tests completed!"