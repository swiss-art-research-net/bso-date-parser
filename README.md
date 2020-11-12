# sari/bso-date-parser

A parser to convert textual dates into EDTF

## Installation

Install using pip

```sh
$ pip install date-parser-sari
```

## Usage

```python
>>> from sariDateParser.dateParser import parse
>>> parse("4 December 1920")
'4.12.1920'
>>> parse("um 1920")
'1920?'
>>> parse("zwischen 1870 und 1890")
'1870/1890'
>>> parse("nicht vor 1450?")
'1450/'
```