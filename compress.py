from itertools import product

"""
We use the simplest compression method for moves here: 2 byte sqare to 1 byte ascii.
For better result consider compressing moves using indexes in valid move lists.
For more sophisticated encoding consider using lichess method described at:
https://lichess.org/blog/Wqa7GiAAAOIpBLoY/developer-update-275-improved-game-compression
"""

# Create mappings to compress variant, result and uci/usi move lists a little
V2C = {
    "standard": "n",
    "capablanca": "c",
    "capahouse": "i",
    "crazyhouse": "h",
    "makruk": "m",
    "placement": "p",
    "seirawan": "s",
    "shogi": "g",
    "shouse": "z",
    "sittuyin": "y",
    "xiangqi": "x",
    "grand": "q",
    "grandhouse": "p",
}
C2V = {v: k for k, v in V2C.items()}

R2C = {"1-0": "a", "0-1": "b", "1/2-1/2": "c", "*": "d"}
C2R = {v: k for k, v in R2C.items()}

# Create square to int mapping
M2C = dict(zip([a + b for a, b in product("abcdefghij", "0123456789")], list(range(34, 256))))

# Add possible from parts of crazy, placement, sittuyin, shogi, capahouse, shouse drop moves
PIECES = "PNBRQKFGSLACHE"
m2c_len = len(M2C) + 34
for piece in PIECES:
    M2C["%s@" % piece] = m2c_len
    m2c_len += 1

C2M = {v: k for k, v in M2C.items()}


def encode_moves(moves):
    return [chr(M2C[move[0:2]]) + chr(M2C[move[2:4]]) + (move[4] if len(move) == 5 else "") for move in moves]


def decode_moves(moves):
    return [C2M[ord(move[0])] + C2M[ord(move[1])] + (move[2] if len(move) == 3 else "") for move in moves]
