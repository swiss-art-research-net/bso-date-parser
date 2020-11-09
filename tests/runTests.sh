#!/bin/bash
currentdir=$(pwd)
if [[ $currentdir =~ "tests" ]]
then
    dir=../sariDateParser
else
    dir=./sariDateParser
fi

echo "Running tests..."

for f in $(find $dir -type f -name '*.py' -follow -print)
do
    python3 $f
done

echo "All tests completed!"