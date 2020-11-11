import re

try:
    import SariDateParser.lib.constants as constants
    import SariDateParser.lib.DateStringParsers as DateStringParsers
    import SariDateParser.lib.TestPatterns as TestPatterns
except ImportError:
    import lib.constants as constants
    import lib.DateStringParsers as DateStringParsers
    import lib.TestPatterns as TestPatterns

def cleanDateString(dateString):
    """
    Removes characters in date string that will be disregarded when interpreting the date

    >>> cleanDateString("[18]42")
    '1842'

    >>> cleanDateString("vermutlich um 1900")
    'vermutlich um 1900'

    """
    s = re.sub('\[|\]', '', dateString)
    return s

def extractPattern(dateString):
    """
    Normalises a date string by replacing digits and date terms with placeholders

    >>> extractPattern("10.5.1985")
    '__._.____'

    >>> extractPattern("10 Mai 1985")
    '__ 🌕 ____'

    >>> extractPattern("7 9br 1950")
    '_ 🌕 ____'

    """
    # Remove square brackets that indicate deducted dates
    genericDate = re.sub(r'\[|\]', '', dateString)

    # Order of language preference for month detections
    langOrder = ['de', 'en', 'fr']
    # Normalise months in different languages
    for lang in langOrder:
        regexPattern = r'(' + ')|('.join([month for variations in [constants.MONTHTERMS[lang][d] for d in constants.MONTHTERMS[lang]] for month in variations]) + ')'                            
        genericDate = re.sub(regexPattern, '🌕', genericDate, flags=re.IGNORECASE)
    genericDate = re.sub(r'🌕r|🌕re|🌕s|🌕br|🌕st|🌕obr|🌕ob|🌕t', '🌕', genericDate, flags=re.IGNORECASE)

    # Normalise indicators of unknown data
    genericDate = re.sub(r'XX|xx', '❓', genericDate)

    # Normalise month in roman numerals
    monthsRoman = r'(' + ')|('.join([month for variations in [constants.MONTHTERMS['roman'][d] for d in constants.MONTHTERMS['roman']] for month in variations]) + ')'                            
    genericDate = re.sub(monthsRoman, '🌕', genericDate)

    # Normalise century terms
    centuriesPattern = r'(' + ')|('.join(constants.ALLCENTURYTERMS) + ')'
    genericDate = re.sub(centuriesPattern, '¢', genericDate)

    # Normalise terms for half
    midTermPattern = r'(' + ')|('.join(constants.ALLMIDTERMS) + ')'
    genericDate = re.sub(midTermPattern, '½', genericDate)

    # Normalise digits
    genericDate = re.sub(r'\d','_', genericDate)

    # Strip whitespace
    genericDate = genericDate.strip()

    return genericDate

def interpret(dateString, pattern):
    """
    Converts a string containing date to an EDTF date using the provided pattern

    >>> interpret("1840","____")
    '1840'

    >>> interpret("ca. 19. Jh.","ca. __. ¢")
    '18XX'

    >>> interpret("22 Aug [18]59","__ 🌕____")
    '1859-08-22'
    """
    ds = cleanDateString(dateString)
    testOrder = ['singleDate', 'fullDateWithMonthInLangOrRoman', 'monthAndYearWithMonthInLangOrRoman', 'singleYearWithQualifier', 'beforeYearWithQualifier', 'afterYearWithQualifier', 'yearRangeWithQualifier', 'yearWithPlaceHolderAndQualifier', 'centuryRange', 'midCentury', 'century', 'singleYearRelaxed']

    for test in testOrder:
        m = re.search(getattr(TestPatterns, test), pattern)
        if m:    
            f = getattr(DateStringParsers, test)
            if not f:
                raise NotImplementedError("Function %s not implemented" % test)
            return f(ds)
    
    return None

def parse(dateString):
    """
    Parse a date string into EDTF Format.

    >>> parse("1751")
    '1751'

    >>> parse("[zwischen 1854 und 1861]")
    '1854/1861'

    >>> parse("vermutlich um 1856")
    '1856?'

    >>> parse("ca. April 1940")
    '1940-04~'

    >>> parse("den 12. Ap. [17]94")
    '1794-04-12'

    >>> parse("1847-?")
    '1847/'

    >>> parse("186? [i.e. zwischen 1860 und 1869]")
    '1860/1869'

    >>> parse("Aug 95 [August 1895]")
    '1895-08'
    """

    pattern = extractPattern(dateString)
    return interpret(dateString, pattern)

if __name__ == '__main__':
    import doctest
    doctest.testmod()