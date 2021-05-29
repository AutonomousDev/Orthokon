# Author: Cameron Bowers
# Date: 05/29/2021
# Description: *******************************TODO****************************************

class OrthokonBoard:
    """Doc string goes here"""

    def __init__(self):
        """initialize variables
        """
        # The board is configured as [X][Y] for coordinates
        self._board = [["Red", "", "", "Yellow"], ["Red", "", "", "Yellow"], ["Red", "", "", "Yellow"],
                       ["Red", "", "", "Yellow"]]

        self._current_state = "UNFINISHED"  # one of the three following values: "RED_WON", "YELLOW_WON", or "UNFINISHED"
        self._debug = False

    def _debug_board(self):
        """debugging tool to print the board"""
        print(self._board)

    def get_current_state(self):
        """returns the current state"""
        return self._current_state

    def _set_current_state(self, state):
        """Update _current_state value"""
        self._current_state = state

    def get_board(self, x, y):
        """return board space values"""
        return self._board[x][y]

    def _set_board(self, x, y, player):
        """Sets a space on the board value"""
        self._board[x][y] = player

    def get_debug(self):
        # Return debug mode status
        return self._debug

    def make_move(self, x1, y1, x2, y2):
        """ Method named make_move that takes four parameters - the row and column (in that order) of the piece being
        moved, and the row and column (in that order) of the square it's being moved to. If the game has already been
        won, or if the move is not valid, make_move should just return False. Otherwise, it should record the move,
        update the board and the current state, and return True. To update the current state, you need to detect if
        this move causes a win for either player. """

        if not self._check_move(x1, y1, x2, y2):
            if self.get_debug(): print("_check move returned false")
            return False  # The move isn't valid

        self._record_move(x1, y1, x2, y2)  # After passing the Valid test the board is updated with new piece positions

        self._update_current_state()  # The game checks to see if anyone won

        # Debug print the board
        if self.get_debug(): self._debug_board()

    def _check_move(self, x1, y1, x2, y2):
        """ This Method Checks if moves are valid. x1, y1 is the starting position. x2, y2 is the ending position"""

        # Check if a piece is at x1,y1
        if self.get_board(x1, y1) == "":
            if self.get_debug(): print("No piece to move")
            return False  # "No piece to move"

        # Check if the move is on the board
        if x2 > 3 or x2 < 0 or y2 > 3 or y2 < 0:
            if self.get_debug(): print("Move off board")
            return False  # Destinations can't leave the board

        # Check if a move really happened
        if x1 == x2 and y1 == y2:
            if self.get_debug(): print("Did not move")
            return False  # Destination can't be the starting point

        # Calculate change in x and y
        delta_y = y2 - y1
        delta_x = x2 - x1

        # Get the direction of X movement as -1, 0 or 1
        if delta_x != 0:
            direction_x = int(delta_x / abs(delta_x))
        else:  # Dividing by zero isn't allowed
            direction_x = int(0)

        # Get the direction of Y movement a -1, 0 or 1
        if delta_y != 0:
            direction_y = int(delta_y / abs(delta_y))
        else:  # Dividing by zero isn't allowed
            direction_y = int(0)

        if self.get_debug():  # Narrate whats happening for debugging
            print("Moving from: ", x1, y1, "to: ", x2, y2)
            print("delta_x: ", delta_x, "delta_y: ", delta_y, "direction_x: ", direction_x, "direction_y: ",
                  direction_y)

        # Check for Horizontal moves
        if delta_y == 0:
            # Passed Horizontal move check

            # Check for clear path to destination
            for x in range(x1 + direction_x, x2 + direction_x, direction_x):  # +direction_x ensures the starting
                # position isn't included while the ending position is. Direction_x should be 1 or -1 in this IF tree.
                if self.get_debug(): print(x, y1, "is", self.get_board(x, y1))

                if self.get_board(x, y1) != "":  # If another piece is in the way, Return False
                    if self.get_debug(): print("Horizontal move path blocked")
                    return False  # Horizontal move path blocked

        # Check for Vertical moves
        elif delta_x == 0:
            # Passed Vertical check

            # Check for clear path to destination
            for y in range(y1 + direction_y, y2 + direction_y, direction_y):  # +direction_y ensures the starting
                # position isn't included while the ending position is. Direction_y should be 1 or -1 in this IF tree.
                if self.get_debug(): print(x1, y, "is", self.get_board(x1, y))

                if self.get_board(x1, y) != "":  # If another piece is in the way, Return False
                    if self.get_debug(): print("Vertical move path blocked")
                    return False  # Vertical move path blocked

        # Check for diagonal moves
        elif abs(delta_x) == abs(delta_y):
            # Passed diagonal check

            # Check for clear path to destination
            for x in range(x1 + direction_x, x2 + direction_x, direction_x):
                for y in range(y1 + direction_y, y2 + direction_y, direction_y):
                    if self.get_debug(): print(x, y, "is", self.get_board(x, y))

                    if self.get_board(x, y) != "":  # If another piece is in the way, Return False
                        if self.get_debug(): print("Diagonal move path blocked")
                        return False # Diagonal move path blocked
        else:
            # Illegal move, isn't horizontal, vertical or diagonal.
            if self.get_debug(): print("Illegal move, isn't horizontal, vertical or diagonal.")
            return False # Illegal move, isn't horizontal, vertical or diagonal.

        if self.get_debug(): print("Passed all _check_move tests")
        return True  # Passed all _check_move tests

    def _record_move(self, x1, y1, x2, y2):
        """Record the move on the board"""
        if self.get_debug(): print(self.get_board(x1, y1))

        piece_moving = self.get_board(x1, y1)
        if self.get_debug(): print("142 Piece moving is: ", piece_moving)
        self._set_board(x2, y2, piece_moving)
        self._set_board(x1, y1, "")

        # Surrounding pieces are turned to the moving pieces color.
        if x2 - 1 >= 0:
            if self.get_board(x2 - 1, y2) != "":
                self._set_board(x2 - 1, y2, piece_moving)
        if x2 + 1 <= 3:
            if self.get_board(x2 + 1, y2) != "":
                self._set_board(x2 + 1, y2, piece_moving)
        if y2 - 1 >= 0:
            if self.get_board(x2, y2 - 1) != "":
                self._set_board(x2, y2 - 1, piece_moving)
        if y2 + 1 <= 3:
            if self.get_board(x2, y2 + 1) != "":
                self._set_board(x2, y2 + 1, piece_moving)

    def _update_current_state(self):
        """Checks victory conditions. if one player has no pieces or moves they lose."""

        # Initialize variable for counting remaining pieces.
        red = 0
        yellow = 0

        # loop through every space on the board and add to the count of remaining pieces.
        for x in range(4):
            for y in range(4):
                if self.get_board(x, y) == "Red":
                    red += 1
                elif self.get_board(x, y) == "Yellow":
                    yellow += 1

        # If all 8 pieces are red or yellow game over.
        if red == 8 and yellow == 0:
            self._set_current_state("RED_WON")
        if yellow == 8 and red == 0:
            self._set_current_state("YELLOW_WON")

        self._moves_possible()  # If either player has no possible moves they lose.

        # If more than 8 pieces are on the board the game is bugged :(
        if 8 > red + yellow > 8:
            print("Something went wrong, Too many pieces on the board")

    def _moves_possible(self):
        red_has_moves = False
        yellow_has_moves = False
        for x in range(4):
            for y in range(4):
                if self.get_board(x, y) != "":
                    player = self.get_board(x, y)
                    if self._check_move(x, y, x, y + 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x + 1, y + 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x + 1, y + 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x + 1, y - 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x, y - 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x - 1, y - 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x - 1, y):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
                    if self._check_move(x, y, x - 1, y + 1):
                        if player == "Red":
                            red_has_moves = True
                        if player == "Yellow":
                            yellow_has_moves = True
        if not red_has_moves:
            self._set_current_state("YELLOW_WON")
        if not yellow_has_moves:
            self._set_current_state("RED_WON")


game = OrthokonBoard()

print(game.make_move(1, 1, 1, 2))
print(game.get_current_state())
print(game._debug_board())
