SP = 0
HE = 1
DI = 2
CL = 3

SPADES = 0
HEARTS = 1
DIAMONDS = 2
CLUBS = 3
NOTRUMP = 4

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

VUL_NONE = 0
VUL_BOTH = 1
VUL_NS = 2
VUL_EW = 3

R2 = 0x0004
R3 = 0x0008
R4 = 0x0010
R5 = 0x0020
R6 = 0x0040
R7 = 0x0080
R8 = 0x0100
R9 = 0x0200
RT = 0x0400
RJ = 0x0800
RQ = 0x1000
RK = 0x2000
RA = 0x4000

K2 = 2
K3 = 3
K4 = 4
K5 = 5
K6 = 6
K7 = 7
K8 = 8
K9 = 9
KT = 10
KJ = 11
KQ = 12
KK = 13
KA = 14

trump = [NOTRUMP]
first = [WEST]
dealer = [NORTH]
vul = [VUL_NONE]


holdings = [
    [
        [RQ | RJ | R3, R9 | R8 | R6 | R4, RK | RT | R2,  RA | R7 | R5],
        [RT | R4, RQ | RJ | R6 | R2, RK | R7 | R5, RA | R9 | R8 | R3],
        [RK | RQ | RJ | R9 | R6 | R5 | R2, None, RA | R8 | R7 | R4, RT | R3],
        [RK, RA | R8 | R7 | R6 | R2, RJ | R5 | R3, RQ | RT | R9 | R4]
    ],
]


# //////////////////////////////////////////////////////////
# //                 Expected outputs                     //
# //////////////////////////////////////////////////////////

# // Number of cards returned for solutions == 2, i.e. for
# // all cards leading to the optimal score (taking into
# // account equivalences.

cardsSoln2 = [6, 3, 4]

# // Number of cards returned for solutions == 3, i.e. for
# // all legally playable cards (taking into account equivalences).
cardsSoln3 = [9, 7, 8]

# // Useful constants
dbitMapRank = [
    0x0000, 0x0000, 0x0001, 0x0002, 0x0004, 0x0008, 0x0010, 0x0020,
    0x0040, 0x0080, 0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000
]

dcardRank = [
    'x', 'x', '2', '3', '4', '5', '6', '7',
    '8', '9', 'T', 'J', 'Q', 'K', 'A'
]

dcardSuit = ["S", "H", "D", "C", "N"]
dcardHand = ['N' 'E', 'S', 'W']
