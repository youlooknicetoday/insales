import re


def replace(string: str, min_letters_count: int = 4) -> str:
    """
    Example input: Батут DFC KIDS STREET, output: Батут DFC Kids Street
    :param string: Text with UPPERCASE words
    :param min_letters_count: Minimum letters count in word of target text. Inclusive.
    :return: Text with Capitalized words.
    """
    pattern = r'([А-ЯA-Z]{%d,})' % min_letters_count
    return re.sub(pattern, lambda match: match.group(1).capitalize(), string)
