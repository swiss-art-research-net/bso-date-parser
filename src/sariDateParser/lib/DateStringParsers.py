import re

try:
    import sariDateParser.lib.constants as constants
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

    >>> fullDateWithMonthInLangOrRoman("aufgenommen 1 Novbr 1860")
    '1860-11-01'

    >>> fullDateWithMonthInLangOrRoman("21. Sept. 76")
    '1976-09-21'

    >>> fullDateWithMonthInLangOrRoman("le 2 Aout 1844 -")
    '1844-08-02'

    >>> fullDateWithMonthInLangOrRoman("den 22. Jul. 1820 gzcht")
    '1820-07-22'

    >>> fullDateWithMonthInLangOrRoman("19. 8br. 1803.")
    '1803-10-19'
    """
    allMonthsInLanguagePattern = '(' + ')|('.join(constants.ALLMONTHLANGUAGETERMS) + ')'
    allMonthsPattern = '(' + ')|('.join(constants.ALLMONTHTERMS) + ')'
    datePattern = r'(\d{1,2})(?:t|\.|\s)*(?:' + allMonthsPattern + ')(?:\.|\s)*(?:\d{2,4})'
    yearPattern = r'((\d{2,4})$|(\d{4})|(\d{2,4}).?$)'
    try:
        date = re.search(datePattern, dateString, flags=re.IGNORECASE).group(1).zfill(2) 
    except:
        return None
        
    try:
        monthWords = re.search(allMonthsInLanguagePattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords)).zfill(2)
    except:
        try: 
            monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
            month = str(guessMonth(monthWords)).zfill(2)
        except:
            return None

    try:
        year = re.search(yearPattern, dateString).group(1)
        if len(year) == 2:
            year = constants.DEFAULTCENTURY + year
        year = year.zfill(4)
    except:
        return None
    
    if int(date) > 31:
        # assume a year has been misinterpreted as date
        return '-'.join([year, month])
    else:
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

    >>> midCentury("[erste Hälfte des 17. Jahrhunderts]")
    '1600/1650'

    >>> midCentury("2. H. 16. Jh.")
    '1550/1599'
    """
    cardinalTermsPattern = '(' + '|'.join(constants.ALLCARDINALTERMS) + ')'
    cardinalTermsPattern = cardinalTermsPattern.replace('.','\.')
    centurySearch = re.search(r'(' + cardinalTermsPattern + ')\s?[A-zäöü|\s|\.]*\s?(\d{1,2})', dateString)
    if not centurySearch:
        return None
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    half = centurySearch.group(1)
    century = centurySearch.group(3)
    centuryEDTF = str(int(century)-1)
    qualifier = '?' if uncertain else ''
    whichHalf = [d for d in constants.CARDINALTERMS.keys() if half in constants.CARDINALTERMS[d]][0]
    if whichHalf == 1:
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

    >>> monthAndYearWithMonthInLangOrRoman("Febr. 36.")
    '1936-02'

    >>> monthAndYearWithMonthInLangOrRoman("im 9br 1792")
    '1792-11'
    """
    allMonthsInLanguagePattern = '(' + ')|('.join(constants.ALLMONTHLANGUAGETERMS) + ')'
    allMonthsPattern = '(' + ')|('.join(constants.ALLMONTHTERMS) + ')'
    yearPattern = r'((\d{2,4})\.?$|(\d{4}))'
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    
    qualifier = '~' if uncertain else ''
        
    try:
        monthWords = re.search(allMonthsInLanguagePattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords)).zfill(2)
    except:
        try: 
            monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
            month = str(guessMonth(monthWords)).zfill(2)
        except:
            return None

    try:
        year = re.search(yearPattern, dateString).group(1).replace('.','')
        if len(year) == 2:
            year = constants.DEFAULTCENTURY + year
        else:
            year = year.zfill(4)
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

    >>> singleDate("1784.9.14")
    '1784-09-14'

    >>> singleDate("1.30.1861")
    '1861-01-30'

    >>> singleDate("aufgenommen in Zürich am 30.6.2010 bei Tageslicht")
    '2010-06-30'

    >>> singleDate("6.3.300")
    '0300-03-06'

    """
    date = re.search(r'(\d{1,4})\.(\d{1,2})\.(\d{2,4})', dateString)
    if len(date.group(1)) > 2:
        # YYYY.MM.DD format
        year = date.group(1).zfill(4)
        month = date.group(2).zfill(2)
        day = date.group(3).zfill(2)
    else:
        year = date.group(3).zfill(4)
        month = date.group(2).zfill(2)
        day = date.group(1).zfill(2)
    if int(month) > 12:
        # Assume that month and day have been swapped
        return '-'.join((year, day, month))
    else:
        return '-'.join((year, month, day))

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
    '1530/1570'

    >>> yearRangeWithQualifier("1914/15")
    '1914/1915'

    >>> yearRangeWithQualifier("1779?-1847")
    '1779/1847'

    >>> yearRangeWithQualifier("1870/1828")
    '1828/1870'
    """
    years = re.search(r'(?:ca\.)?\s?(?:zwischen)?\s?(\d{3,4})\??\s?(?:-|und|bis|ud|\/)\s?(?:vor)?\s?(\d{2,4})\??', dateString)
    yearsPair = [years.group(1), years.group(2)]
    if len(yearsPair[1]) < len(yearsPair[0]):
        # Accommodate for 1814/15 type of dates by taking century from first date
        diff = len(yearsPair[0])-len(yearsPair[1])
        yearsPair[1] = yearsPair[0][:diff] + yearsPair[1]
    if int(yearsPair[1]) < int(yearsPair[0]):
        # Make sure dates are in correct order and switch if necessary
        yearsPair = [yearsPair[1], yearsPair[0]]
    yearsPair = [yearsPair[0].zfill(4), yearsPair[1].zfill(4)]
    return "/".join(yearsPair)

if __name__ == '__main__':
    import doctest
    doctest.testmod()