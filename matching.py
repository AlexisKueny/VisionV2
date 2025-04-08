import cv2
import numpy as np
from itertools import zip_longest

# Replace Edge enum with string constants
STRAIGHT = "STRAIGHT"
MALE = "MALE"
FEMALE = "FEMALE"

class puzzle_piece:
    def __init__(self, image, right_edge, bottom_edge, left_edge, top_edge, id):
        self.image = image
        self.id = id
        self.sides = {
            'top': top_edge,
            'right': right_edge,
            'bottom': bottom_edge,
            'left': left_edge
        }

        # Count how many edges are STRAIGHT
        straight_count = sum([
            edge == STRAIGHT
            for edge in self.sides.values()
        ])

        # Determine piece_type
        if straight_count == 2:
            self.piece_type = "CORNER"
        elif straight_count == 1:
            self.piece_type = "BORDER"
        elif straight_count == 0:
            self.piece_type = "MIDDLE"
        else:
            self.piece_type = "invalid"  # e.g. 3 or 4 straight edges, shouldn't happen in a normal puzzle

    def __repr__(self):
        # Symbols for each edge type per direction
        edge_symbols = {
            STRAIGHT: {'top': '─────', 'right': '|', 'bottom': '─────', 'left': '|'},
            MALE: {'top': '──^──', 'right': '▶', 'bottom': '──v──', 'left': '◀'},
            FEMALE: {'top': '──U──', 'right': '(', 'bottom': '──n──', 'left': ')'},
        }

        # Get the symbols for each side
        top = edge_symbols[self.sides['top']]['top']
        right = edge_symbols[self.sides['right']]['right']
        bottom = edge_symbols[self.sides['bottom']]['bottom']
        left = edge_symbols[self.sides['left']]['left']

        # Use a basic 3x3 block with the edge symbols
        return f"""
   {top}       ID: {self.id}
 {left}     {right} 
 {left}     {right} 
   {bottom}      Type: {self.piece_type}
"""

def print_side_by_side(piece1, piece2):
    piece1_lines = repr(piece1).splitlines()
    piece2_lines = repr(piece2).splitlines()
    for line1, line2 in zip_longest(piece1_lines, piece2_lines, fillvalue=""):
        print(f"{line1:<30} {line2}")

def rotate_piece(piece):
    return puzzle_piece(
        #image=rotate_image(piece.image),  # if needed
        right_edge=piece.sides['top'],
        bottom_edge=piece.sides['right'],
        left_edge=piece.sides['bottom'],
        top_edge=piece.sides['left'],
        id=piece.id
    )

def edges_match(edge1, edge2):
    return (edge1 == MALE and edge2 == FEMALE) or \
           (edge1 == FEMALE and edge2 == MALE)

def isMatch(piece1: puzzle_piece, piece2: puzzle_piece):
    parralels = {
        'top': ('right', 'left'),
        'right': ('top', 'bottom'),
        'bottom': ('left', 'right'),
        'left': ('bottom', 'top')
    }


    if piece1.piece_type == "CORNER" and piece2.piece_type == "CORNER":
        return False
    
    else:
        for side in piece1.sides.keys():
            if piece1.sides[side] == STRAIGHT and piece2.sides[side] == STRAIGHT:
                print("Both pieces share a straight edge on side:", side)
                # Check if the parallel sides (connectors) align
                parallel1 = piece1.sides[parralels[side][0]]
                parallel2 = piece2.sides[parralels[side][1]]

                if edges_match(parallel1, parallel2):
                    print(f"Parallel sides connect: {parallel1} (piece1) matches {parallel2} (piece2).")
                    return True
                else:
                    print(f"Parallel sides do not connect: {parallel1} (piece1) does not match {parallel2} (piece2).")
                
        return False

if __name__ == '__main__':
    # Corner piece (2 straight edges)
    piece1 = puzzle_piece(
        image=None,
        right_edge=MALE,
        bottom_edge=FEMALE,
        left_edge=STRAIGHT,
        top_edge=STRAIGHT,
        id=1
    )

    # Border piece (1 straight edge)
    piece2 = puzzle_piece(
        image=None,
        right_edge=FEMALE,
        bottom_edge=MALE,
        left_edge=STRAIGHT,
        top_edge=MALE,
        id=2
    )

    # Middle piece (0 straight edges)
    piece3 = puzzle_piece(
        image=None,
        right_edge=MALE,
        bottom_edge=FEMALE,
        left_edge=MALE,
        top_edge=FEMALE,
        id=3
    )

    # Border piece (1 straight edge)
    piece4 = puzzle_piece(
        image=None,
        right_edge=STRAIGHT,
        bottom_edge=MALE,
        left_edge=FEMALE,
        top_edge=MALE,
        id=4
    )

    # Border piece (1 straight edge)
    piece5 = puzzle_piece(
        image=None,
        right_edge=FEMALE,
        bottom_edge=MALE,
        left_edge=STRAIGHT,
        top_edge=FEMALE,
        id=5
    )

    # Test Case 1
    print("\nDoes piece1 (corner) match piece2 (border) on the right?")
    print_side_by_side(piece1, piece2)
    print("Match result:", isMatch(piece1, piece2))  # True

    # Test Case 2
    print("\nDoes piece1 (corner) match piece4 (border) on the bottom?")
    print_side_by_side(piece1, piece4)
    print("Match result:", isMatch(piece1, piece4))  # True

    # Test Case 3
    print("\nDoes piece1 (corner) match piece5 (border) on the left?")
    print_side_by_side(piece1, piece5)
    print("Match result:", isMatch(piece1, piece5))  # False

    # Test Case 4
    print("\nDoes piece1 (corner) match piece2 (border) on the top?")
    print_side_by_side(piece1, piece2)
    print("Match result:", isMatch(piece1, piece2))  # False

    # Test Case 5
    print("\nDoes piece1 (corner) match piece4 (border) on the left?")
    print_side_by_side(piece1, piece4)
    print("Match result:", isMatch(piece1, piece4))  # True

    # Test Case 6
    print("\nDoes piece2 (border) match piece4 (border) on the bottom?")
    print_side_by_side(piece2, piece4)
    print("Match result:", isMatch(piece2, piece4))  # True

    # Test Case 7
    print("\nDoes piece2 (border) match piece5 (border) on the right?")
    print_side_by_side(piece2, piece5)
    print("Match result:", isMatch(piece2, piece5))  # True

    # Test Case 8
    print("\nDoes piece4 (border) match piece5 (border) on the left?")
    print_side_by_side(piece4, piece5)
    print("Match result:", isMatch(piece4, piece5))  # True

    # Test Case 9
    print("\nDoes piece2 (border) match piece4 (border) on the top?")
    print_side_by_side(piece2, piece4)
    print("Match result:", isMatch(piece2, piece4))  # False

    # Test Case 10
    print("\nDoes piece4 (border) match piece5 (border) on the bottom?")
    print_side_by_side(piece4, piece5)
    print("Match result:", isMatch(piece4, piece5))  # False

    # Test Case 11
    print("\nDoes piece1 (corner) match piece2 (border) on the bottom?")
    print_side_by_side(piece1, piece2)
    print("Match result:", isMatch(piece1, piece2))  # True

    # Test Case 12
    print("\nDoes piece1 (corner) match piece5 (border) on the right?")
    print_side_by_side(piece1, piece5)
    print("Match result:", isMatch(piece1, piece5))  # False

    # Test Case 13
    print("\nDoes piece2 (border) match piece4 (border) on the left?")
    print_side_by_side(piece2, piece4)
    print("Match result:", isMatch(piece2, piece4))  # True

    # Test Case 14
    print("\nDoes piece4 (border) match piece5 (border) on the top?")
    print_side_by_side(piece4, piece5)
    print("Match result:", isMatch(piece4, piece5))  # True

    # Test Case 15
    print("\nDoes piece2 (border) match piece5 (border) on the bottom?")
    print_side_by_side(piece2, piece5)
    print("Match result:", isMatch(piece2, piece5))  # False

