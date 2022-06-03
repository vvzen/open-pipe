import os
import dataclasses

import openpipe.naming

@dataclasses.dataclass
class OpenPipeContext:
    show: str = None
    sequence: str = None
    shot: str = None


def make_context_from_path(path):
    """Give an path as input, try to understand to which context it belongs to,
    using the regexes defined in the show_naming configuration

    :param path: absolute path
    :type path: str
    :return: the retrieved context
    :rtype: OpenPipeContext
    """

    shots_regexes = openpipe.naming.get_naming_regexes("shot")
    sequence_regexes = openpipe.naming.get_naming_regexes("sequence")

    show_name = None
    shot_name = None
    sequence_name = None

    path_tokens = path.split(os.path.sep)
    for index, token in enumerate(path_tokens):

        if not shot_name:
            for shot_regex in shots_regexes:
                shot_match = shot_regex.match(token)
                if not shot_match:
                    continue

                # Shots have to be children of sequences
                if not openpipe.naming.is_sequence(path_tokens[index-1]):
                    continue

                shot_name = shot_match.group()
                break

        if not sequence_name:
            for sequence_regex in sequence_regexes:
                sequence_match = sequence_regex.match(token)
                if not sequence_match:
                    continue

                sequence_name = sequence_match.group()
                # If we have found a sequence, then the parent directory is
                # the show name. If needed, this should be made customizable
                # in the future via some type of hooks.
                show_name = path_tokens[index-1]
                break

    # We couldn't find any sequence/shot, check if we're at the show level
    if not any([show_name, sequence_name, shot_name]):
        # If at least one sequence here matches the sequence regex,
        # then we must be at the root of the show
        current_dirs = os.listdir(path)
        for dir_name in current_dirs:
            if openpipe.naming.is_sequence(dir_name):
                show_name = os.path.basename(path)
                break

        # Last resort:
        # Look for the pipeline/etc directory, which is where openpipe
        # stores its configuration files
        if os.path.exists(os.path.join(path, "openpipe", "etc")):
            show_name = os.path.basename(path)

    context = OpenPipeContext(show=show_name,
                              sequence=sequence_name,
                              shot=shot_name)

    return context
