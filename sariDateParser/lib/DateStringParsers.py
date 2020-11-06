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
    '1250?/'
    """
    yearSearch = re.search(r'(\d{4}\??)', dateString)
    if not yearSearch:
        return None
    year = yearSearch.group(1)
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    year = year + "/"
    if uncertain and not '?' in year:
        return year + "?"
    else:
        return year

def beforeYearWithQualifier(dateString):
    """
    Given a string that contains a year, interprets it as before that year

    >>> beforeYearWithQualifier("1940")
    '/1940'

    >>> beforeYearWithQualifier("nach 1250?")
    '/1250?'
    """
    yearSearch = re.search(r'(\d{4}\??)', dateString)
    if not yearSearch:
        return None
    year = yearSearch.group(1)
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    year = "/" + year
    if uncertain and not '?' in year:
        return year + "?"
    else:
        return year

def century(dateString):
    """
    Given a string containing one or two digits, interprets it as a century in EDTF format

    >>> century("19. Jahrhundert")
    '18'

    >>> century("4. Jh.")
    '3'
    """
    centurySearch = re.search(r'(\d{1,2})', dateString)
    if not centurySearch:
        return None
    century = centurySearch.group(1)
    centuryEDTF = str(int(century)-1) ## EDTF uses YY for century. 19th century is 18
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    if uncertain:
        return centuryEDTF + "?"
    else:
        return centuryEDTF

def centuryRange(dateString):
    """
    Given a string containing  two groups of digits, interprets it as a range of centuries in EDTF format

    >>> centuryRange("18/19. Jahrhundert")
    '17/18'

    >>> centuryRange("3/4. Jh.")
    '2/3'

    >>> centuryRange("9/10. Jh.")
    '8/9'
    """
    centurySearch = re.findall(r'(\d{1,2})', dateString)
    if len(centurySearch) <2:
        return None
    centuryFrom = centurySearch[0]
    centuryTo = centurySearch[1]
    centuryFromEDTF = str(int(centuryFrom)-1) ## EDTF uses YY for century. 19th century is 18
    centuryToEDTF = str(int(centuryTo)-1) 
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    if uncertain:
        return centuryFromEDTF + "?/" + centuryToEDTF + "?"
    else:
        return centuryFromEDTF + "/" + centuryToEDTF

def fullDateWithMonthInLangOrRoman(dateString):
    """
    Given a string containing a date with month written as a name or in roman numerals, returns the date in EDTF format

    >>> fullDateWithMonthInLangOrRoman("2 Feb 2020")
    '2.2.2020'

    """
    allMonthsPattern = '|'.join(constants.ALLMONTHTERMS)
    datePattern = r'(\d{1,2})(?:\.|\s)*(?:' + allMonthsPattern + ')(?:\.|\s)*(?:\d{2,4})'
    yearPattern = r'((\d{2,4})\.?$|\d{4})'
    try:
        date = re.search(datePattern, dateString, flags=re.IGNORECASE).group(1)
    except:
        return None
        
    try:
        monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords))
    except:
        return None

    try:
        year = re.search(yearPattern, dateString).group(1)
    except:
        return None
    
    return '.'.join([date, month, year])

def guessMonth(monthString):
    testOrder = ['de', 'en', 'fr', 'roman']
    monthString = re.sub(r'\.|\s', '', monthString)
    for lang in testOrder:
        for i in constants.MONTHTERMS[lang].keys():
            for monthVariation in constants.MONTHTERMS[lang][i]:
                if monthVariation.lower() == monthString.lower():
                    return i
    return 0
    
def midCentury(dateString):
    centurySearch = re.search(r'(\d)\.\s?[A-zäöü]*\s?(\d{1,2})', dateString)
    if not centurySearch:
        return None
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    half = centurySearch.group(1)
    century = centurySearch.group(2)
    centuryEDTF = str(int(century)-1)
    qualifier = '?' if uncertain else ''
    if half == "1":
        return century + "00" + qualifier + "/" + century + "50" + qualifier
    else:
        return century + "50" + qualifier + "/" + century + "99" + qualifier

def monthAndYearWithMonthInLangOrRoman(dateString):
    allMonthsPattern = '|'.join(constants.ALLMONTHTERMS)
    yearPattern = r'((\d{2,4})\.?$|\d{4})'
    uncertain = re.search(r'(' + constants.UNCERTAINTYQUALIFIERS + ')', dateString)
    qualifier = '?' if uncertain else ''
    try:
        monthWords = re.search(allMonthsPattern, dateString, flags=re.IGNORECASE).group(0)
        month = str(guessMonth(monthWords))
    except:
        return None

    try:
        year = re.search(yearPattern, dateString).group(1)
    except:
        return None
    
    return '.'.join([month, year]) + qualifier

def singleDate(dateString):
    date = re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', dateString)
    if date:
        return date.group(0)
    else:
        return None

def singleYearRelaxed(dateString):
    return singleYearWithQualifier(dateString)
    
def singleYearWithQualifier(dateString):
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
    years = re.findall(r'(\d{2,4}\??)', dateString)
    uncertain = re.search(r'(ca)', dateString)
    if uncertain:
        for i, year in enumerate(years):
            if not '?' in year:
                years[i] += '?'
    return "/".join(years)

if __name__ == '__main__':
    import doctest
    doctest.testmod()