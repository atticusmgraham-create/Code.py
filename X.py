import re


def is_plural(word):
    word = word.strip().lower()
    if not word:
        return False

    # 1. Immediate exceptions (Common singular words ending in 's')
    singular_exceptions = {
        'is', 'was', 'as', 'has', 'this', 'us', 'bus', 'lens', 'alias', 
        'gas', 'news', 'canvas', 'chaos', 'crisis', 'series', 'species',
        'progress', 'success', 'physics', 'mathematics', 'economics'
    }
    if word in singular_exceptions:
        return False

    # 2. Known Irregular Plurals (Hardcoded list replaces the flaky API)
    irregular_plurals = {
        'men', 'women', 'children', 'mice', 'teeth', 'feet', 'geese', 
        'oxen', 'data', 'criteria', 'phenomena', 'people', 'dice'
    }
    if word in irregular_plurals:
        return True

    # 3. Rule Matching via Regular Expressions
    # These match standard English plural ending transformations
    plural_rules = [
        r'.*([^aeiou])ies$',       # babies, flies (singular ends in -y)
        r'.*[sxz]es$',             # boxes, gases, buzzes
        r'.*[^aeiou]o|ch|shes$',   # heroes, potatoes, churches, wishes
        r'.*ves$',                 # wolves, knives, leaves (singular -f/-fe)
        r'.+s$'                    # generic plural ending (cats, dogs, pens)
    ]

    for rule in plural_rules:
        if re.match(rule, word):
            # Double check to prevent short singulars like 'is', 'as' (caught above)
            if len(word) > 2:
                return True

    return False

# --- TEST VERIFICATION ---
