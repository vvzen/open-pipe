"""
This module is concerned with parsing strings and understanding if they match
some internal (customizable) naming convention.
"""

import re

from openpipe.config import get_config, MalformedConfigError

def get_naming_regexes(name):

    regexes_patterns = []

    naming_config = get_config("show_naming")
    naming_entry = naming_config.get(name)
    if not naming_entry:
        return

    patterns = naming_entry.get("patterns")
    if not patterns:
        raise MalformedConfigError("Naming entry for '%s' "
                                  "didn't contain a 'patterns' key." % name)

    compound = naming_entry.get("appends_to")
    if compound:
        appends_with = naming_entry.get("appends_with")
        if not appends_with:
            raise MalformedConfigError(
                    "Naming entry for '%s' is compounded, "
                    "but is not defining the required 'appends_with' key.")

        other_entry = naming_config.get(compound)
        if not other_entry:
            raise MalformedConfigError("Naming entry for '%s' is compounded, "
                                      "but the other entry specified ('%s') "
                                      "doesn't exist." % (name, compound))

        other_entry_patterns = other_entry.get("patterns")
        if not other_entry_patterns:
            raise MalformedConfigError(
                             "Naming entry for '%s' is compounded, but "
                             "the 'pattern' of '%s' isn't defined" %
                             (name, other_entry))

        for pattern in patterns:
            for other_pattern in other_entry_patterns:
                regexes_patterns.append(
                    "^(" + other_pattern + appends_with + pattern + ")$")
    else:
        for pattern in patterns:
            regexes_patterns.append("^(" + pattern + ")$")

    if not regexes_patterns:
        return

    return [re.compile(p) for p in regexes_patterns]


def is_shot(input_name):
    shot_regexes = get_naming_regexes("shot")
    for shot_regex in shot_regexes:
        if shot_regex.match(input_name):
            return True
    return False


def is_sequence(input_name):
    sequence_regexes = get_naming_regexes("sequence")
    for sequence_regex in sequence_regexes:
        if sequence_regex.match(input_name):
            return True
    return False


def sequence_name_from_shot_name(shot_name):

    if not is_shot(shot_name):
        raise ValueError("'%s' is not a valid shot name")

    sequence_regexes = get_naming_regexes("sequence")
    for regex in sequence_regexes:
        # Remove anchors of the regex
        unconstrained_regex = re.compile(regex.pattern.replace("$", ""))
        match = unconstrained_regex.match(shot_name)
        if match:
            return match.groups()[0]

    raise ValueError("Cannot extract sequence name from '%s'" % shot_name)
