import re

try:
    import SariDateParser.lib.constants as constants
except ImportError:
    try:
         import lib.constants as constants
    except ImportError:
        import constants as constants
            
def afterYearWithQualifier(dateString):
    """
    Given a string that contains a year, interprets it as after that year

    >>> afterYearWithQualifier("1940")
    '1940/'

    >>> afterYearWithQualifier("nach 1250?")
    '1250/'
    """
    yearSearch = re.search(r'(\d{4})\??', dateString)
    if not yearSearch:
        return None
    year = yearSearch.group(1)
    year = year + "/"
    return year

def beforeYearWithQualifier(dateString):
    """
    Given a string that contains a year, interprets it as before that year

    >>> beforeYearWithQualifier("1940")
    '/1940'

    >>> beforeYearWithQualifier("nach 1250?")
    '/1250'
    """
    yearSearch = re.search(r'(\d{4})\??', dateString)
    if not yearSearch:
        return None
    year = yearSearch.group(1)
    year = "/" + year
    return year

def century(dateString):
    """
    Given a string containing one or two digits, interprets it as a century in EDTF format

    >>> century("19. Jahrhundert")
    '18XX'

    >>> century("4. Jh.")
    '03XX'
    """
    centurySearch = re.search(r'(\d{1,2})', dateString)
    if not centurySearch:
        return None
    century = centurySearch.group(1)
    centuryEDTF = str(int(century)-1).zfill(2) ## EDTF uses YY for century. 19th century is 18
    return centuryEDTF + "XX"

def centuryRange(dateString):
    """
    Given a string containing  two groups of digits, interprets it as a range of centuries in EDTF format

    >>> centuryRange("18/19. Jahrhundert")
    '17XX/18XX'

    >>> centuryRange("3/4. Jh.")
    '02XX/03XX'

    >>> centuryRange("9/10. Jh.")
    '08XX/09XX'
    """
    centurySearch = re.findall(r'(\d{1,2})', dateString)
    if len(centurySearch) <2:
        return None
    centuryFrom = centurySearch[0]
    centuryTo = centurySearch[1]
    centuryFromEDTF = str(int(centuryFrom)-1).zfill(2) ## EDTF uses YY for century. 19th century is 18
    centuryToEDTF = str(int(centuryTo)-1) .zfill(2)
    return centuryFromEDTF + "XX/" + centuryToEDTF + "XX"

def fullDateWithMonthInLangOrRoman(dateString):
    """
    Given a string containing a date with month written as a name or in roman numerals, returns the date in EDTF format

    >>> fullDateWithMonthInLangOrRoman("2 Feb 2020")
    '2020-02-02'

    >>> fullDateWithMonthInLangOrRoman("6 VII 1938")
    '1938-07-06'

    >>> fullDateWithMonthInLangOrRoman("aufgenommen 1 Novbr 1860")
    '1860-11-01'

    """
    allMonthsPattern = '(' + ')|('.join(constants.ALLMONTHTERMS) + ')'
    datePattern = r'(\d{1,2})(?:\.|\s)*(?:' + allMonthsPattern + ')(?:\.|\s)*(?:\d{2,4})'
    yearPattern = r'((\d{2,4})\.?$|\d{4})'
    try:
        date = re.search(datePattern, dateString, flags=re.IGNORECASE).group(1).zfill(2)
    except:
        return None
        
    try:
        monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords)).zfill(2)
    except:
        return None

    try:
        year = re.search(yearPattern, dateString).group(1).zfill(4)
    except:
        return None
    
    return '-'.join([year, month, date])

def guessMonth(monthString):
    """
    Given a string that contains a (only) term for a month either in text or roman numerals returns the month as a number

    >>> guessMonth("February")
    '2'

    >>> guessMonth("Okt")
    '10'

    >>> guessMonth("9br")
    '11'

    >>> guessMonth("Ap.")
    '4'

    >>> guessMonth("5 January 1910")
    
    
    >>> guessMonth("2.10.10")
    
    """
    testOrder = ['de', 'en', 'fr', 'roman']
    monthString = re.sub(r'\.|\s', '', monthString)
    for lang in testOrder:
        for i in constants.MONTHTERMS[lang].keys():
            for monthVariation in constants.MONTHTERMS[lang][i]:
                if monthVariation.lower() == monthString.lower():
                    return i
    return None
    
def midCentury(dateString):
    """
    Given a string that contains a statement about either half of a century, returns a date in EDTF format

    >>> midCentury("2. Hälfte 19. Jahrhundert")
    '1850/1899'

    >>> midCentury("ca 1. Hälfte 15. Jh.")
    '1400?/1450?'
    """
    centurySearch = re.search(r'(\d)\.\s?[A-zäöü]*\s?(\d{1,2})', dateString)
    if not centurySearch:
        return None
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    half = centurySearch.group(1)
    century = centurySearch.group(2)
    centuryEDTF = str(int(century)-1)
    qualifier = '?' if uncertain else ''
    if half == "1":
        return centuryEDTF + "00" + qualifier + "/" + centuryEDTF + "50" + qualifier
    else:
        return centuryEDTF + "50" + qualifier + "/" + centuryEDTF + "99" + qualifier

def monthAndYearWithMonthInLangOrRoman(dateString):
    """
    Given a string containing a date expressed by a month term and a year returns the date in EDTF format

    >>> monthAndYearWithMonthInLangOrRoman("April 1450")
    '1450-04'

    >>> monthAndYearWithMonthInLangOrRoman("October 2007?")
    '2007-10~'

    >>> monthAndYearWithMonthInLangOrRoman("VII 1893")
    '1893-07'
    """
    allMonthsPattern = '(' + ')|('.join(constants.ALLMONTHTERMS) + ')'
    yearPattern = r'((\d{2,4})\.?$|\d{4})'
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    qualifier = '~' if uncertain else ''
    try:
        monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords)).zfill(2)
    except:
        return None

    try:
        year = re.search(yearPattern, dateString).group(1).zfill(4)
    except:
        return None
    
    return '-'.join([year, month]) + qualifier

def singleDate(dateString):
    """
    Given a string containing a date expressed in numeric date format, returns it in EDTF

    >>> singleDate("10.4.1983")
    '1983-04-10'

    >>> singleDate("am 5.10.1930")
    '1930-10-05'

    >>> singleDate("aufgenommen in Zürich am 30.6.2010 bei Tageslicht")
    '2010-06-30'

    >>> singleDate("6.3.300")
    '0300-03-06'

    """
    date = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})', dateString)
    year = date.group(3).zfill(4)
    month = date.group(2).zfill(2)
    day = date.group(1).zfill(2)
    if date:
        return '-'.join((year, month, day))
    else:
        return None

def singleYearRelaxed(dateString):
    """
    Given a string that contains numbers, interprets those numbers as a year and returns it in EDTF

    >>> singleYearRelaxed("1430")
    '1430'

    >>> singleYearRelaxed("ca. 1830")
    '1830?'

    >>> singleYearRelaxed("I think it must have been in 1530 because that's when the castle has been built")
    '1530?'
    """
    return singleYearWithQualifier(dateString)
    
def singleYearWithQualifier(dateString):
    """
    Given a string that contains four digits interprets it as a year
    
    >>> singleYearWithQualifier("1965")
    '1965'

    >>> singleYearWithQualifier("ca. 1830")
    '1830?'
    """
    yearSearch = re.search(r'(\d{4}\??)', dateString)
    if not yearSearch:
        return None
    year = yearSearch.group(1)
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    if uncertain and not '?' in year:
        return year + "?"
    else:
        return year

def yearWithPlaceHolderAndQualifier(dateString):
    """
    Converts a string containing a year, in which the last one or two digits are unknown

    >>> yearWithPlaceHolderAndQualifier("18--")
    '1800/1899'

    >>> yearWithPlaceHolderAndQualifier("193-")
    '1930/1939'

    >>> yearWithPlaceHolderAndQualifier("17--?")
    '1700?/1799?'
    """
    uncertain = re.search(r'(ca|\?)', dateString)
    quantifier = '?' if uncertain else ''
    m = re.search(r'(\d{2})--', dateString)
    if m:
        century = m.group(1)
        return "%s00%s/%s99%s" % (century, quantifier, century, quantifier)
    m = re.search(r'(\d{3})-', dateString)
    if m:
        century = m.group(1)
        return "%s0%s/%s9%s" % (century, quantifier, century, quantifier)

def yearRangeWithQualifier(dateString):
    """
    Converts a string containing two digits as a range of years

    >>> yearRangeWithQualifier("zwischen 1980 und 1990")
    '1980/1990'
    >>> yearRangeWithQualifier("von ca. 1530 bis 1570")
    '1530?/1570?'
    """
    years = re.findall(r'(\d{2,4}\??)', dateString)
    uncertain = re.search(r'(ca)', dateString)
    if uncertain:
        for i, year in enumerate(years):
            if not '?' in year and year:
                years[i] += '?'
    return "/".join(years)

if __name__ == '__main__':
    import doctest
    doctest.testmod()