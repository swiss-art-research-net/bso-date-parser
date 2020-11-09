try:
    import SariDateParser.lib.constants as constants
except ImportError:
    try:
        import lib.constants as constants
    except:
        import constants as constants

afterYearWithQualifier = r'^(' + constants.UNCERTAINTYQUALIFIERS + ')?((?:nach|nicht vor)\s?(_{4})|_{4}-|_{4}-❓{1,2})\??$'
beforeYearWithQualifier = r'^(' + constants.UNCERTAINTYQUALIFIERS + ')?((?:vor|nicht nach)\s?(_{4})|-_{4}|❓{1,2}-_{4})\??$'
century = r'_{1,2}(\s|\.)*¢'
centuryRange = r'_{1,2}(\s|\.)*¢?(\/|-)_{1,2}(\s|\.)*¢'
fullDateWithMonthInLangOrRoman = r'_{1,2}(\.|\s)*(🌕)(\.|\s)*(_{2,4})'
midCentury = r'_\.\s?½\s?_{1,2}(\.|\s)*¢'
monthAndYearWithMonthInLangOrRoman = r'🌕(\.|\s)*(_{2,4})'
singleDate = r'(?:i\.e\.|den|le)?\s?(_{1,2}\._{1,2}\._{2,4})'
singleYearWithQualifier = r'^(?:' + constants.UNCERTAINTYQUALIFIERS + '|A°|Ao|Ao\.|A°\.|Anno|anno|gezeichnet nach der Natur|i\.e\.)?\s?(____)\??$'
singleYearRelaxed = r'_{4}'
yearRangeWithQualifier = r'(?:ca\.)?\s?(?:zwischen)?\s?(_{4}\??)\s?(?:-|und|ud|/)\s?(_{2,4}\??)'
yearWithPlaceHolderAndQualifier = r'(([^_]|^)__--|([^_]|^)___-)'