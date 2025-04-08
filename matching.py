import cv2
import numpy as np
from itertools import zip_longest

# Replace Edge enum with string constants
STRAIGHT = "STRAIGHT"
MALE = "MALE"
FEMALE = "FEMALE"

class PuzzlePiece:  # Renamed class to follow PascalCase convention
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
    return PuzzlePiece(  # Updated class name
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

def isMatch(piece1: PuzzlePiece, piece2: PuzzlePiece):
    perpendiculars = {  # Map each side to its perpendicular sides
        'top': ('left', 'right'),
        'right': ('top', 'bottom'),
        'bottom': ('left', 'right'),
        'left': ('top', 'bottom')
    }

    if piece1.piece_type == "CORNER" and piece2.piece_type == "CORNER":
        return False

    for side in piece1.sides.keys():
        if piece1.sides[side] == STRAIGHT and piece2.sides[side] == STRAIGHT:
            print("Both pieces share a straight edge on side:", side)

            # Check if either of the perpendicular sides match
            perp1_a = piece1.sides[perpendiculars[side][0]]
            perp2_a = piece2.sides[perpendiculars[side][0]]
            perp1_b = piece1.sides[perpendiculars[side][1]]
            perp2_b = piece2.sides[perpendiculars[side][1]]

            if edges_match(perp1_a, perp2_a) or edges_match(perp1_b, perp2_a):
                print(f"Perpendicular sides connect: {perpendiculars[side][0]} ({perp1_a} on piece1) matches {perpendiculars[side][0]} ({perp2_a} on piece2) or {perpendiculars[side][1]} ({perp1_b} on piece1) matches {perpendiculars[side][1]} ({perp2_b} on piece2).")
                return True
            else:
                print(f"Perpendicular sides do not connect: {perp1_a} (piece1) does not match {perp2_a} (piece2) and {perp1_b} (piece1) does not match {perp2_b} (piece2).")

    return False

if __name__ == '__main__':
    piece1 = PuzzlePiece(
        image=None,
        right_edge=FEMALE,
        bottom_edge=STRAIGHT,
        left_edge=STRAIGHT,
        top_edge=MALE,
        id=1
    )
    piece2 = PuzzlePiece(
        image=None,
        right_edge=MALE,
        bottom_edge=STRAIGHT,
        left_edge=MALE,
        top_edge=MALE,
        id=2
    )
    piece3= PuzzlePiece(
        image=None,
        right_edge=MALE,
        left_edge=FEMALE,
        top_edge=MALE,
        bottom_edge=STRAIGHT,
        id=3
    )

    print("Matching piece1 and piece2 => TRUE")
    print_side_by_side(piece1, piece2)
    print(isMatch(piece1, piece2))

    print("Matching piece2 and piece3 => TRUE")
    print_side_by_side(piece2, piece3)
    print(isMatch(piece2, piece3))

    print("Matching piece1 and piece3 => FALSE")
    print_side_by_side(piece1, piece3) 
    print(isMatch(piece1, piece3))