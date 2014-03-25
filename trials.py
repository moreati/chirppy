import itertools
import string
import struct
import sys

import reedsolomon

# 0  0   1760 |  8  8   2788 | 16  g   4422 | 24  o   7014
# 1  1   1864 |  9  9   2953 | 17  h   4684 | 25  p   7431
# 2  2   1974 | 10  a   3128 | 18  i   4962 | 26  q   7872
# 3  3   2091 | 11  b   3314 | 19  j   5257 | 27  r   8340
# 4  4   2215 | 12  c   3511 | 20  k   5569 | 28  s   8835
# 5  5   2346 | 13  d   3719 | 21  l   5900 | 29  t   9360
# 6  6   2485 | 14  e   3940 | 22  m   6250 | 30  u   9916
# 7  7   2632 | 15  f   4174 | 23  n   6621 | 31  v  10505
CHARS = '0123456789abcdefghijklmnopqrstuv'
BYTES = ''.join(chr(i) for i in xrange(len(CHARS)))

_B2C = string.maketrans(BYTES, CHARS)
_C2B = string.maketrans(CHARS, BYTES)
_C2I = {c: i for i, c in enumerate(CHARS)}

def b2c(s):
    r"""Convert a string of bytes containing symbol indexes to a
    string of symbols.

    >>> b2c('\x00\x01\x0a\x11')
    '01ah'
    """
    return string.translate(s, _B2C)

def c2b(s):
    r"""Convert a string of symbols to a string of bytes containing
    symbol indexes.

    >>> c2b('01ah')
    '\x00\x01\n\x11'
    """
    return string.translate(s, _C2B)

def i2c(s):
    r"""Convert an interable of symbol indexes to a string of symbols.

    >>> i2c([0, 1, 10, 17])
    '01ah'
    """
    return ''.join(CHARS[i] for i in s)

def c2i(s):
    r"""Convert a string of symbols to an list of symbol indexes.

    >>> i2c('01ah')
    [0, 1, 10, 17]
    """
    return [_C2I[c] for c in s]

def mutations(s):
    yield s
    yield s[::-1] # reversed
    yield ''.join(chr(~ord(c) & 0x1f) for c in s) # complement
    yield ''.join(chr(~ord(c) & 0x1f) for c in s[::-1]) # reversed complement

# preamble (2)  data (10)       error correction (8)
# 'hj'          'srg00lgbif'    '4c6u07sq'
# 'hj'          '0b07407074'    '9lir5uo0'
# 'hj'          'unvaufl1j3'
# 'hj'          'mnac2dvevb'
# 'hj'          '8ehqbur4bk'
# 'hj'          'gfhd9532dm'    '4fbeu0mo' 
# 'hj'          'ovkp99793i'    'ao89q5ku'

guesses = [
    (18, 10, 5,
        frozenset(mutations(c2b('gfhd9532dm'))),
        frozenset(mutations(c2b('gfhd9532dm4fbeu0mo'))),
        ),
# Unlikely variations of how a chirp might be bit packed
#    (20, 12, 5
#        frozenset(mutations(c2b('hjsrg00lgbif'))),
#        frozenset(mutations(c2b('hjsrg00lgbif4c6u07sq'))),
#        ),
#    (13,  8, 8
#        frozenset({struct.pack('>q', int('srg00lgbif', 32)),
#                   struct.pack('<q', int('srg00lgbif', 32)),
#                   }),
#        frozenset({struct.pack('>q', int('srg00lgbif', 32))
#                   + struct.pack('>q', int('4c6u07sq', 32))[3:],
#                   struct.pack('<q', int('srg00lgbif', 32))
#                   + struct.pack('<q', int('4c6u07sq', 32))[:-3],
#                   }),
#        ),
#    (12,  7, 8
#        frozenset({struct.pack('>q', int('srg00lgbif', 32))[1:],
#                   struct.pack('<q', int('srg00lgbif', 32))[:-1],
#                   }),
#        frozenset({struct.pack('>q', int('srg00lgbif', 32))[1:]
#                   + struct.pack('>q', int('4c6u07sq', 32))[3:],
#                   struct.pack('<q', int('srg00lgbif', 32))[:-1]
#                   + struct.pack('<q', int('4c6u07sq', 32))[:-3],
#                   }),
#        ),
    ]

def tryone((encoded_len, data_len, symbol_size, gfpoly, fcr, prim,
           candidates, expecteds)):
    try:
        codec = reedsolomon.Codec(encoded_len, data_len, symbol_size,
                                  gfpoly, fcr, prim)
    except MemoryError, e:
        return
    for candidate in candidates:
        encoded = codec.encode(candidate)
        if encoded in expecteds:
            print "Found (%i, %i, %i) using %s, %s, gfpoly %i, fcr %i, prim %i" \
                  % (encoded_len, data_len, symbol_size, candidate, encoded, gfpoly, fcr, prim)
            return

if __name__ == '__main__':
    # Valid ranges for fcr/prim ranges found experimentally
    inputs = ((encoded_len, data_len, symbol_size, gfpoly, fcr, prim,
              candidates, expecteds)
              for gfpoly, fcr, prim in itertools.product(xrange(1, 2**20, 2), xrange(1, 32), xrange(1, 32))
              for encoded_len, data_len, symbol_size, candidates, expecteds in guesses
              )
    for t in inputs:
        tryone(t)

