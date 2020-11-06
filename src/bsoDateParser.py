import re
import sys

import lib.constants as constants
import lib.DateStringParsers as DateStringParsers
import lib.TestPatterns as TestPatterns

def cleanDateString(dateString):
    s = re.sub('\[|\]', '', dateString)
    return s

def extractPattern(dateString):
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
    pattern = extractPattern(dateString)
    return interpret(dateString, pattern)

if __name__ == "__main__":
    import sys
    print(parse(sys.argv[1]))