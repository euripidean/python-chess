import pygame
from data.classes.pieces.Queen import Queen

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False

    def get_moves(self, board): # adjusted this to refactor so double check it is working
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)
                    break
                output.append(square)
        return output
    
    def get_valid_moves(self, board):
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)
        return output
    
    def move(self, board, square, force=False):
       for i in board.squares:
           i.hightlight = False
       if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True
            # Pawn Promotion handling
            if self.notation == '': # See if there is a way to enable choosing the piece to promote to
                if self.y == 0 or self.y == 7:
                    square.occupying_piece = Queen(self.x, self.y, self.color, board)
           # Castling handling
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            return True
       else:
           board.selected_piece = None
           return False
       
    def attacking_squares(self, board):
        return self.get_moves(board)
               


    
       