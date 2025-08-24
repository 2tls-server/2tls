# https://stackoverflow.com/a/2267446

import string
digs = string.digits + string.ascii_letters


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x = x // base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

from random import SystemRandom

def get_id() -> str:
    return int2base(SystemRandom().randint(62 ** 19, 62 ** 20 - 1), 62)

from unidecode import unidecode
from pykakasi import kakasi

def romanize(original_text: str) -> str:
    kks = kakasi()

    text = original_text.lower().replace(' ', '')

    unidecode_text = unidecode(text).lower().replace(' ', '')
    kakasi_text = ''.join([item['hepburn'] for item in kks.convert(text)]).lower().replace(' ', '')

    texts = []

    texts.append(text)
    if unidecode_text != text:
        texts.append(unidecode_text)

    if kakasi_text != text and kakasi_text != unidecode_text:
        texts.append(kakasi_text)

    return ''.join(texts)