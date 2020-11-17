try:
    import sariDateParser.lib.constants as constants
except ImportError:
    try:
        import lib.constants as constants
    except:
        import constants as constants

import re

cardinalTermsPattern = r'(' + '|'.join(constants.ALLCARDINALTERMS) + ')'
cardinalTermsPattern = re.sub(r'\d','_', cardinalTermsPattern.replace('.','\.')) 

afterYearWithQualifier = r'^(' + constants.UNCERTAINTYQUALIFIERS + ')?((?:nach|nicht vor)\s?(_{4})|_{4}-|_{4}-❓{1,2})\??$'
beforeYearWithQualifier = r'^(' + constants.UNCERTAINTYQUALIFIERS + ')?((?:vor|nicht nach)\s?(_{4})|-_{4}|❓{1,2}-_{4})\??$'
century = r'_{1,2}(\s|\.)*¢'
centuryRange = r'_{1,2}(\s|\.)*¢?(\/|-)_{1,2}(\s|\.)*¢'
fullDateWithMonthInLangOrRoman = r'_{1,2}(t|\.|\s)*(🌕)(\.|\s)*(_{2,4})'
midCentury = cardinalTermsPattern +'\s?½[A-zäöü|\s]*_{1,2}(\.|\s)*¢'
monthAndYearWithMonthInLangOrRoman = r'🌕(\.|\s)*(_{2,4})'
singleDate = r'(?:i\.e\.|den|le)?\s?(_{1,2}\._{1,2}\._{2,4})'
singleYearWithQualifier = r'^(?:' + constants.UNCERTAINTYQUALIFIERS + '|A°|Ao|Ao\.|A°\.|Anno|anno|gezeichnet nach der Natur|i\.e\.)?\s?(____)\??$'
singleYearRelaxed = r'_{4}'
yearRangeWithQualifier = r'(?:ca\.)?\s?(?:zwischen)?\s?(_{3,4}\??)\s?(?:-|und|ud|/)\s?(?:vor)?\s?(_{2,4}\??)'
yearWithPlaceHolderAndQualifier = r'(([^_]|^)__--|([^_]|^)___-)'