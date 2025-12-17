from game_board import Marker

GAME_STATES = {
    "1": {
        "name": "AI wins in 5 turns",
        "moves": [
            (7, 4, Marker.AI), (5, 5, Marker.AI), (6, 5, Marker.AI),
            (7, 5, Marker.AI), (8, 6, Marker.AI), (8, 7, Marker.AI),
            (5, 8, Marker.AI), (6, 8, Marker.AI), (7, 8, Marker.AI),
            (9, 8, Marker.PLAYER), (4, 5, Marker.PLAYER), (5, 6, Marker.PLAYER),
            (6, 6, Marker.PLAYER), (7, 6, Marker.PLAYER), (4, 7, Marker.PLAYER),
            (8, 10, Marker.PLAYER), (7, 7, Marker.PLAYER), (3, 8, Marker.PLAYER),
            (8, 4, Marker.PLAYER)
        ],
        "turn": Marker.AI
    },
    "2": {
        "name": "Double open three",
        "moves": [
            (10, 8, Marker.AI), (10, 9, Marker.AI),
            (8, 10, Marker.AI), (9, 10, Marker.AI),
            (5, 5, Marker.PLAYER), (5, 6, Marker.PLAYER), (15, 15, Marker.PLAYER)
        ],
        "turn": Marker.AI
    },
    "3": {
        "name": "Ignore Threat and go for win",
        "moves": [
            (4, 4, Marker.PLAYER), (5, 5, Marker.PLAYER), (6, 6, Marker.PLAYER),

            (10, 10, Marker.AI), (11, 10, Marker.AI), (12, 10, Marker.AI),
            (9, 10, Marker.PLAYER)
        ],
        "turn": Marker.AI
    },
    "4": {
        "name": "Forced Block",
        "moves": [
            (5, 5, Marker.PLAYER), (6, 5, Marker.PLAYER), (7, 5, Marker.PLAYER),
            (8, 5, Marker.PLAYER),
            (4, 5, Marker.AI)
        ],
        "turn": Marker.AI
    },
    "5": {
        "name": "AI expands open three aggressively over blocking player",
        "moves": [
            (2, 2, Marker.AI), (3, 2, Marker.AI),
            (10, 8, Marker.PLAYER), (10, 9, Marker.PLAYER),
            (8, 10, Marker.PLAYER), (9, 10, Marker.PLAYER)
      ],
        "turn": Marker.AI
    },
    "6": {
        "name": "AI blocks left side not right",
        "moves": [
            (6, 6, Marker.PLAYER), (7, 6, Marker.PLAYER), (8, 6, Marker.PLAYER),
            (5, 5, Marker.PLAYER), (5, 7, Marker.PLAYER),
            (15, 15, Marker.AI)
        ],
        "turn": Marker.AI
    },
    "7": {
        "name": "Difficult to defend against AI",
        "moves": [
            (5, 5, Marker.AI), (7, 5, Marker.AI), (8, 6, Marker.AI),
            (6, 6, Marker.AI),

            (6, 5, Marker.PLAYER), (9, 7, Marker.PLAYER),
            (8, 8, Marker.PLAYER), (7, 6, Marker.PLAYER)
        ],
        "turn": Marker.AI
    },
    "8": {
        "name": "Late game win 1",
        "moves": [(9, 9, Marker.PLAYER), (8, 8, Marker.AI), (8, 10, Marker.PLAYER),
                  (10, 8, Marker.AI), (7, 9, Marker.PLAYER), (9, 8, Marker.AI),
                  (7, 8, Marker.PLAYER), (11, 8, Marker.AI), (12, 8, Marker.PLAYER),
                  (10, 9, Marker.AI), (10, 10, Marker.PLAYER), (11, 10, Marker.AI),
                  (12, 11, Marker.PLAYER), (11, 9, Marker.AI), (11, 11, Marker.PLAYER),
                  (12, 7, Marker.AI), (12, 12, Marker.PLAYER), (13, 13, Marker.AI),
                  (12, 10, Marker.PLAYER), (12, 9, Marker.AI), (12, 13, Marker.PLAYER),
                  (12, 14, Marker.AI), (9, 10, Marker.PLAYER)],
        "turn": Marker.AI
    },
    "9": {
        "name": "Late game win 2",
        "moves": [(9, 9, Marker.PLAYER), (8, 8, Marker.AI), (8, 10, Marker.PLAYER),
                  (10, 8, Marker.AI), (7, 9, Marker.PLAYER), (9, 8, Marker.AI),
                  (7, 8, Marker.PLAYER), (11, 8, Marker.AI), (12, 8, Marker.PLAYER),
                  (10, 9, Marker.AI), (10, 10, Marker.PLAYER), (11, 10, Marker.AI),
                  (12, 11, Marker.PLAYER), (11, 9, Marker.AI), (11, 11, Marker.PLAYER),
                  (12, 7, Marker.AI), (12, 12, Marker.PLAYER), (13, 13, Marker.AI),
                  (12, 10, Marker.PLAYER), (12, 9, Marker.AI), (12, 13, Marker.PLAYER),
                  (12, 14, Marker.AI), (9, 10, Marker.PLAYER), (11, 6, Marker.AI),
                  (11, 7, Marker.PLAYER), (14, 9, Marker.AI)],
        "turn": Marker.PLAYER
    },
    "0": {
        "name": "Late game black AI win 1",
        "moves": [(10, 10, Marker.PLAYER), (9, 11, Marker.AI), (8, 10, Marker.PLAYER),
                  (9, 10, Marker.AI), (9, 9, Marker.PLAYER), (11, 11, Marker.AI),
                  (8, 9, Marker.PLAYER), (13, 11, Marker.AI), (10, 11, Marker.PLAYER),
                  (10, 8, Marker.AI), (7, 9, Marker.PLAYER), (10, 9, Marker.AI),
                  (8, 11, Marker.PLAYER), (8, 12, Marker.AI), (7, 10, Marker.PLAYER),
                  (9, 12, Marker.AI)],
        "turn": Marker.PLAYER
    },
    "+": {
        "name": "Late game black AI win 2",
        "moves": [(14, 3, Marker.PLAYER), (13, 4, Marker.AI), (14, 5, Marker.PLAYER),
                  (14, 4, Marker.AI), (15, 4, Marker.PLAYER), (13, 2, Marker.AI),
                  (15, 5, Marker.PLAYER), (13, 5, Marker.AI), (13, 6, Marker.PLAYER),
                  (16, 3, Marker.AI), (15, 3, Marker.PLAYER), (15, 2, Marker.AI),
                  (14, 6, Marker.PLAYER), (15, 7, Marker.AI), (16, 4, Marker.PLAYER),
                  (13, 7, Marker.AI), (12, 6, Marker.PLAYER), (11, 6, Marker.AI),
                  (16, 6, Marker.PLAYER), (15, 6, Marker.AI), (17, 6, Marker.PLAYER),
                  (13, 3, Marker.AI), (13, 1, Marker.PLAYER)],
        "turn": Marker.AI
    }
}