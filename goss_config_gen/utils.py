import os


def expand_env(value):
    """
    Expand environment and user variables

    :param str value: Value to expand
    :return: Expanded value
    :rtype: str
    """
    return os.path.expandvars(os.path.expanduser(value))
