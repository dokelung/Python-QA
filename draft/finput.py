# author: dokelung

import re
from ast import literal_eval
from functools import partial


class InputDoesNotMatchFStr(Exception): pass
class TypeConvertError(Exception): pass
class InputCountNotInRange(Exception): pass


FORMAT_SPECIFIER = {
    '%a': literal_eval,
    '%d': int,
    '%f': float,
    '%o': partial(int, base=8),
    '%s': str,
    '%x': partial(int, base=16),
}


def finput(prompt='', fstr='%s', expand_fsp=None,
           whitespace=False,
           escape_parenthesis=True):
    """format input
    """
    fsp = FORMAT_SPECIFIER
    if expand_fsp is not None:
        fsp.update(expand_fsp)
    if escape_parenthesis:
        rstr = fstr.replace('(', '\(').replace(')', '\)')
    else:
        rstr = fstr
    regex = '(.+)' if whitespace else '(\S+)'
    for sp, typ in fsp.items():
        rstr = rstr.replace(sp, regex)
    types = []
    for idx, c in enumerate(fstr):
        pattern = fstr[idx:idx+2]
        if pattern in fsp:
            types.append(fsp[pattern])
    pure_input = input(prompt)
    mobj = re.match(rstr, pure_input)
    if mobj:
        try:
            return tuple(typ(value) for value, typ in zip(mobj.groups(), types))
        except Exception as err:
            raise TypeConvertError(err)
    else:
        msg = 'input does not match format string "{}"'
        raise InputDoesNotMatchFStr(msg.format(fstr))


def minput(prompt='', typ=str, sep=None, min=1, max=100000):
    """multiple input
    """
    pure_input = input(prompt)
    try:
        if sep is None:
            values = tuple(typ(item) for item in pure_input.split())
        else:
            values = tuple(typ(item) for item in pure_input.split(sep))
    except Exception as err:
        raise TypeConvertError(err)
    if len(values) < min or len(values) > max:
        msg = 'input count {} is not in range [{}, {}]'
        raise InputCountNotInRange(msg.format(len(values), min, max))
    return values


if __name__ == '__main__':
    #res = finput('>>> ', fstr='%s, *%d, *%f')
    #print(res)
    res = minput('>>> ', typ=int, min=1, max=3)
    print(res)
