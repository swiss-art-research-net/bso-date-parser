#!/bin/bash
currentdir=$(pwd)
if [[ $currentdir =~ "tests" ]]
then
    dir=../src
else
    dir=./src
fi

echo "Running tests..."

for f in $(find $dir -type f -name '*.py' -follow -print)
do
    python3 $f
done

echo "All tests completed!"