import string

import six


def name_for_filesystem(input_name):
    """Generate a name 'safe' and 'clean' for filesystem usage (no spaces,
    only lowercase, etc.)

    :param input_name: name to use as input
    :type input_name: str
    :raises TypeError: if the input name is not a valid string
    :return: the safe name
    :rtype: str
    """

    if not isinstance(input_name, six.string_types):
        raise TypeError("Please provide a valid string. "
                        "Received: %s, %s" % (input_name, type(input_name)))

    input_name = input_name.replace(" ", "_")
    input_name = input_name.replace("-", "_")

    letters = [
        a for a in input_name
        if a in string.ascii_letters or a in string.digits or a == "_"
    ]
    return "".join(letters).lower()
