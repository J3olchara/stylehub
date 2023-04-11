"""
Utils for core app

Write your util functions here.
"""
from string import punctuation
from typing import Any, Dict, Optional


def get_normalize_table() -> Dict[str, Optional[Any]]:
    """
    returns table for name-normalizing in model Item

    replaces all russian letters that simplify
    english letters to english letter and deletes
    all punctuation from string.
    """
    tab = dict.fromkeys(punctuation)
    alphabet = {  # rus: eng
        'А': 'A',
        'В': 'B',
        'Е': 'E',
        'Т': 'T',
        'О': 'O',
        'Р': 'P',
        'Н': 'H',
        'К': 'K',
        'Х': 'X',
        'С': 'C',
        'М': 'M',
        ' ': '',
    }
    tab.update(alphabet)
    return tab


normalize_table = get_normalize_table()
