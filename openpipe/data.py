"""Generic functionality to deal with python data structures.
"""

def flatten_list(a_list, parent_list=None):
    """Given a list/tuple as entry point, return a flattened list version.
    EG:
        >>> flatten_list([1, 2, [3, 4]])
        [1, 2, 3, 4]

    NB: The kwargs are only for internal use of the function and should not be
    used by the caller.
    """

    if parent_list is None:
        parent_list = []

    for element in a_list:
        if isinstance(element, list):
            flatten_list(element, parent_list=parent_list)
        elif isinstance(element, tuple):
            flatten_list(element, parent_list=parent_list)
        else:
            parent_list.append(element)

    return parent_list


def flatten_dict(a_dict, parent_keys=None, current_parent_key=None):
    """Given a dict as input, return a version of the dict where the keys
    are no longer nested, and instead flattened.
    EG:
        >>> flatten_dict({"a": {"b": 1}})
        {"a.b": 1}

    NB: The kwargs are only for internal use of the function and should not be
    used by the caller.
    """

    if parent_keys is None:
        parent_keys = []

    for key, value in a_dict.items():
        if current_parent_key:
            key = "%s.%s" % (current_parent_key, key)
        if isinstance(value, dict):
            flatten_dict(value, parent_keys=parent_keys, current_parent_key=key)
        else:
            parent_keys.append((key, value))

    return dict(parent_keys)
