#!/bin/bash
currentdir=$(pwd)
if [[ $currentdir =~ "tests" ]]
then
    dir=../src
else
    dir=./src
fi

echo "Running tests..."
getopts v flag

echo "Running tests in source code"
for f in $(find $dir -type f -name '*.py' -follow -print)
do
    python3 $f -$flag
done

read -p "Run test cases? (y/n)" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Running test cases"
fi

echo "All tests completed!"