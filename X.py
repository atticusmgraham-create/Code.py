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
test_words = {
    "mice": True,       # Irregular plural
    "cats": True,       # Standard plural
    "boxes": True,      # -es plural
    "babies": True,     # -ies plural
    "leaves": True,     # -ves plural
    "cat": False,       # Regular singular
    "bus": False,       # Singular ending in -s
    "physics": False,   # Singular academic discipline 
}

print("Running validation tests:")
for word, expected in test_words.items():
    result = is_plural(word)
    status = "PASS" if result == expected else "FAIL"
    print(f"  {word.ljust(10)} -> Found Plural: {str(result).ljust(5)} (Expected: {str(expected).ljust(5)}) [{status}]")
#Use code with caution.Why this approach fixes the issueZero Dependency on Web Changes: The Free Dictionary API updates its data format often, causing properties like definitions[0] to randomly break. A local regex script remains stable.Solves the 404 Bug: You no longer have to worry about an external server throwing a connection error or hiding valid results behind a error code.Granular Control: If your code encounters specific words that break the rules (such as a unique slang word or an industry-specific noun), you can simply add it straight to the singular_exceptions or irregular_plurals sets at the top of the function.Are there specific words or datasets your code is evaluating that are still returning the wrong value?1 siteHow do you extract definition from Dictionary API?Apr 8, 2023 — Utkarsh_Seth April 8, 2023, 4:05pm 1. I am using https://dictionaryapi.dev/ API. Example https://api.dictionaryapi.dev/api/v2/entr...
