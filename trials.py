import itertools
import string
import struct

import reedsolomon

# 0  0   1760 |  8  8   2788 | 16  g   4422 | 24  o   7014
# 1  1   1864 |  9  9   2953 | 17  h   4684 | 25  p   7431
# 2  2   1974 | 10  a   3128 | 18  i   4962 | 26  q   7872
# 3  3   2091 | 11  b   3314 | 19  j   5257 | 27  r   8340
# 4  4   2215 | 12  c   3511 | 20  k   5569 | 28  s   8835
# 5  5   2346 | 13  d   3719 | 21  l   5900 | 29  t   9360
# 6  6   2485 | 14  e   3940 | 22  m   6250 | 30  u   9916
# 7  7   2632 | 15  f   4174 | 23  n   6621 | 31  v  10505

ints = range(32)
bytes = ''.join(chr(i) for i in ints)
chars = '0123456789abcdefghijklmnopqrstuv'

def b2c(s):
    return string.translate(s, string.maketrans(bytes, chars))

def c2b(s):
    return string.translate(s, string.maketrans(chars, bytes))

def i2c(s):
    return ''.join(chars[i] for i in s)

def c2i(s):
    return [chars.index(c) for c in s]

def mutations(s):
    yield s
    yield s[::-1] # reversed
    yield ''.join(chr(~ord(c) & 0x1f) for c in s) # complement
    yield ''.join(chr(~ord(c) & 0x1f) for c in s[::-1]) # reversed complement

# preamble (2)  data (10)       error correction (8)
# 'hj'          'srg00lgbif'    '4c6u07sq'
# 'hj'          '0b07407074'    '9lir5uo0'

guesses = [
    (18, 10, 5
        frozenset(mutations(c2b('srg00lgbif'))),
        frozenset(mutations(c2b('srg00lgbif4c6u07sq'))),
        ),
    (20, 12, 5
        frozenset(mutations(c2b('hjsrg00lgbif'))),
        frozenset(mutations(c2b('hjsrg00lgbif4c6u07sq'))),
        ),
    (13,  8, 8
        frozenset({struct.pack('>q', int('srg00lgbif', 32)),
                   struct.pack('<q', int('srg00lgbif', 32)),
                   }),
        frozenset({struct.pack('>q', int('srg00lgbif', 32))
                   + struct.pack('>q', int('4c6u07sq', 32))[3:],
                   struct.pack('<q', int('srg00lgbif', 32))
                   + struct.pack('<q', int('4c6u07sq', 32))[:-3],
                   }),
        ),
    (12,  7, 8
        frozenset({struct.pack('>q', int('srg00lgbif', 32))[1:],
                   struct.pack('<q', int('srg00lgbif', 32))[:-1],
                   }),
        frozenset({struct.pack('>q', int('srg00lgbif', 32))[1:]
                   + struct.pack('>q', int('4c6u07sq', 32))[3:],
                   struct.pack('<q', int('srg00lgbif', 32))[:-1]
                   + struct.pack('<q', int('4c6u07sq', 32))[:-3],
                   }),
        ),
    ]

for gfpoly, fcr, prim in itertools.product(xrange(2**8), xrange(2**8), xrange(2**8)):
    for encoded_len, data_len, symbol_size, candidates, expecteds in guesses:
        try:
            codec = reedsolomon.Codec(encoded_len, data_len, symbol_size,
                                      gfpoly, fcr, prim)
        except MemoryError:
            continue
        for candidate in candidates:
            encoded = codec.encode(candidate)
            if encoded in expecteds:
                print "Found (%i, %i, %i) using %s, %s, gfpoly %i, fcr %i, prim %i" \
                      % (encoded_len, data_len, symbol_size, candidate, encoded, gfpoly, fcr, prim)
                      break

