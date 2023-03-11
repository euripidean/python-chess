import pygame
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn


#Checks game state
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(Square(x, y, self.tile_width, self.tile_height))
        return output
    
    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square
            
    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black'
                        )
                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
            elif self.selected_piece.move(self, clicked_square):
                self.turn = 'white' if self.turn == 'black' else 'black'
            elif clicked_square.occupying_piece is None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color, board_change=None):
        output = False
        king_pos = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pst == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [ i.occupying_piece for i in self.squares if i.occupying_piece is not None ]
        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
            if king_pos is None:
                for piece in pieces:
                    if piece.notation == 'K' and piece.color == color:
                        king_pos = piece.pos
                for piece in pieces:
                    if piece.color != color:
                        for square in piece.attacking_squares(self):
                            if square.pos == king_pos:
                                output = True
                if board_change is not None:
                    old_square.occupying_piece = changing_piece
                    new_square.occupying_piece = new_square_old_piece
                return output
            
        #checkmate checker
        def is_in_checkmate(self, color):
            output = False
            for piece in [ i.occupying_piece for i in self.squares]:
                if piece != None:
                    if piece.notation == 'K' and piece.color == color:
                        king = piece
            if king.get_valid_moves(self) == []:
                if self.is_in_check(color):
                    output = True
            return output
        
        #stalemate checker
        def is_in_stalemate(self, color):
            output = False
            for piece in [ i.occupying_piece for i in self.squares]:
                if piece != None:
                    if piece.notation == 'K' and piece.color == color:
                        king = piece
            if king.get_valid_moves(self) == []:
                if not self.is_in_check(color):
                    output = True
            return output
        
        #insufficient material checker
        def is_insufficient_material(self):
            output = False
            pieces = [ i.occupying_piece for i in self.squares if i.occupying_piece is not None ]
            if len(pieces) == 2:
                if pieces[0].notation == 'K' or pieces[1].notation == 'K':
                    if pieces[0].notation == 'N' or pieces[1].notation == 'N':
                        output = True
            elif len(pieces) == 3:
                if pieces[0].notation == 'K' or pieces[1].notation == 'K' or pieces[2].notation == 'K':
                    if pieces[0].notation == 'N' or pieces[1].notation == 'N' or pieces[2].notation == 'N':
                        if pieces[0].notation == 'B' or pieces[1].notation == 'B' or pieces[2].notation == 'B':
                            output = True
            elif len(pieces) == 4:
                if pieces[0].notation == 'K' or pieces[1].notation == 'K' or pieces[2].notation == 'K' or pieces[3].notation == 'K':
                    if pieces[0].notation == 'N' or pieces[1].notation == 'N' or pieces[2].notation == 'N' or pieces[3].notation == 'N':
                        if pieces[0].notation == 'B' or pieces[1].notation == 'B' or pieces[2].notation == 'B' or pieces[3].notation == 'B':
                            if pieces[0].notation == 'B' or pieces[1].notation == 'B' or pieces[2].notation == 'B' or pieces[3].notation == 'B':
                                output = True
            return output
        
        #threefold repetition checker
        def is_threefold_repetition(self):
            output = False
            if self.board_history.count(self.board_history[-1]) >= 3:
                output = True
            return output
        
        #fifty move rule checker
        def is_fifty_move_rule(self):
            output = False
            if self.move_counter >= 50:
                output = True
            return output
        
        #draw checker
        def is_draw(self):
            output = False
            if self.is_insufficient_material() or self.is_threefold_repetition() or self.is_fifty_move_rule():
                output = True
            return output
        
        def draw_board(self, display):
            if self.selected_piece is not None:
               self.get_square_from_pos(self.selected_piece.pos).highlight = True
               for square in self.selected_piece.get_valid_moves(self):
                   square.highlight = True
            for square in self.squares:
                square.draw(display)
