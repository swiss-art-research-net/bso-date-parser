
DEFAULTCENTURY = '19'
UNCERTAINTYQUALIFIERS = 'ca\.|ca|circa|um|vermutlich um|\?'

MONTHTERMS = {
    'de': {
        '1': ["Januar", "Jan"],
        '2': ["Februar", "Febr", "Feb"],
        '3': ["März", "Maerz", "Merz", "Mrz"],
        '4': ["April", "Apr", "Ap"],
        '5': ["Mai", "Mei"],
        '6': ["Juni", "Juny", "Jun"],
        '7': ["Juli", "July", "Jul"],
        '8': ["August", "Augst", "Aug"],
        '9': ["September", "Sept", "Sep"],
        '10': ["Oktober", "Okt"],
        '11': ["November", "Nov"],
        '12': ["Dezember", "Dez"],
    },
    'en': {
        '1': ["January", "Jan"],
        '2': ["February", "Feb"],
        '3': ["March", "Mar"],
        '4': ["April", "Apr"],
        '5': ["May"],
        '6': ["June", "Juny", "Jun"],
        '7': ["July", "Jul"],
        '8': ["August", "Aug", "Aust"],
        '9': ["September", "Sep", "Sept"],
        '10': ["October", "Oct"],
        '11': ["November", "Nov"],
        '12': ["December", "Dec"],
    },
    'fr': {
        '1': ["Janvier", "Janv", "Jan"],
        '2': ["Février", "Févr", "Fév"],
        '3': ["Mars", "Mar"],
        '4': ["Avrill", "Avril", "Avrl", "Avr"],
        '5': ["Mai"],
        '6': ["Juin"],
        '7': ["Juillet", "Juil"],
        '8': ["Août", "Aout", "Aoust", "Aost", "Aost", "Aou"],
        '9': ["Septembre", "Septbr", "Sept", "Sep", "7bre", "7br"],
        '10': ["Octobre", "octobr", "Octob", "Oct", "8bre", "8br"],
        '11': ["Novembre", "Novbr", "Nov", "9bre", "9br"],
        '12': ["Décembre", "Decbr", "Dec", "Xbre", "Xbr"],
    },
    'roman': {
        '8': ["VIII"],
        '7': ["VII"],
        '12': ["XII"],
        '3': ["III"],
        '11': ["XI"],
        '9': ["IX"],
        '2': ["II"],
        '4': ["IV"],
        '6': ["VI"],
        '10': ["X", "Xbr"],
        '5': ["V"],
        '1': ["I"],
    }
}

CENTURYTERMS = {
    'de': ["Jahrhundert", "Jahrundert", "Jht", "Jh"]
}

BCETERMS = {
    'de': ["v.Chr"]
}

CARDINALTERMS = {
    1: ["1.", "erste"],
    2: ["2.", "zweite"],
}

MIDTERMS = {
    'de': ["Hälfte", "H."]
}

ALLMONTHTERMS = [item for sublist in [month for langMonths in [list(d.values()) for d in [MONTHTERMS[lang] for lang in MONTHTERMS]] for month in langMonths] for item in sublist]
ALLMONTHLANGUAGETERMS = [item for sublist in [month for langMonths in [list(d.values()) for d in [MONTHTERMS[lang] for lang in MONTHTERMS if lang != 'roman']] for month in langMonths] for item in sublist]
ALLBCETERMS = [d for l in [BCETERMS[d] for d in BCETERMS] for d in l]
ALLCENTURYTERMS = [d for l in [CENTURYTERMS[d] for d in CENTURYTERMS] for d in l]
ALLCARDINALTERMS = [d for l in [CARDINALTERMS[d] for d in CARDINALTERMS] for d in l]
ALLMIDTERMS = [d for l in [MIDTERMS[d] for d in MIDTERMS] for d in l]

