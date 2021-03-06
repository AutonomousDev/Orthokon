# Author: Cameron Bowers
# Date: 05/29/2021
# Description: The class called OrthokonBoard  represents the board for a two-player game that is played on a
# 4x4 grid. This class does not do everything needed to play a game - it's just responsible for handling the rules
# concerning the game board. Things like asking the user for moves, printing results for the user, keeping track of
# whose turn it is, and running the game loop would be the responsibility of one or more other classes.

class OrthokonBoard:
    """Doc string goes here"""

    def __init__(self):
        """initialize variables
        """
        # The board is configured as [X][Y] for coordinates
        self._board = [["Red", "", "", "Yellow"], ["Red", "", "", "Yellow"], ["Red", "", "", "Yellow"],
                       ["Red", "", "", "Yellow"]]

        self._current_state = "UNFINISHED"  # One of the three following values: "RED_WON", "YELLOW_WON",
        # or "UNFINISHED"

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

    def make_move(self, y1, x1, y2, x2):
        """ Method named make_move that takes four parameters - the row and column (in that order) of the piece being
        moved, and the row and column (in that order) of the square it's being moved to. If the game has already been
        won, or if the move is not valid, make_move should just return False. Otherwise, it should record the move,
        update the board and the current state, and return True. To update the current state, you need to detect if
        this move causes a win for either player.

        The rest of the class uses x y coordinates in the traditional order instead of Row Column.
        """
        if self.get_current_state() != "UNFINISHED":
            return False  # Game is over

        if not self._check_move(x1, y1, x2, y2):
            return False  # The move isn't valid

        self._record_move(x1, y1, x2, y2)  # After passing the Valid test the board is updated with new piece positions
        self._update_current_state()  # The game checks to see if anyone won
        return True

    def _check_move(self, x1, y1, x2, y2):
        """ This Method Checks if moves are valid. x1, y1 is the starting position. x2, y2 is the ending position"""
        # Check if a piece is at x1,y1
        if self.get_board(x1, y1) == "":
            return False  # "No piece to move"

        # Check if the move is on the board
        if x2 > 3 or x2 < 0 or y2 > 3 or y2 < 0:
            return False  # Destinations can't leave the board

        # Check if a move really happened
        if x1 == x2 and y1 == y2:
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

        # Check for Horizontal moves
        if delta_y == 0:
            # Passed Horizontal move check

            # Check for clear path to destination
            for x in range(x1 + direction_x, x2 + direction_x, direction_x):  # +direction_x ensures the starting
                # position isn't included while the ending position is. Direction_x should be 1 or -1 in this IF tree.

                if self.get_board(x, y1) != "":  # If another piece is in the way, Return False
                    return False  # Horizontal move path blocked

        # Check for Vertical moves
        elif delta_x == 0:
            # Passed Vertical check

            # Check for clear path to destination
            for y in range(y1 + direction_y, y2 + direction_y, direction_y):  # +direction_y ensures the starting
                # position isn't included while the ending position is. Direction_y should be 1 or -1 in this IF tree.

                if self.get_board(x1, y) != "":  # If another piece is in the way, Return False
                    return False  # Vertical move path blocked

        # Check for diagonal moves
        elif abs(delta_x) == abs(delta_y):
            # Passed diagonal check

            # Check for clear path to destination
            for delta in range(1, abs(delta_x) + 1):
                x = (direction_x * delta) + x1
                y = (direction_y * delta) + y1

                if self.get_board(x, y) != "":  # If another piece is in the way, Return False
                    return False  # Diagonal move path blocked

        else:
            # Illegal move, isn't horizontal, vertical or diagonal.
            return False  # Illegal move, isn't horizontal, vertical or diagonal.

        if not self._stop_check(direction_x, direction_y, x2, y2):
            return False  # Next space is open. Illegal move

        return True  # Passed all _check_move tests

    def _stop_check(self, direction_x, direction_y, x2, y2):
        """Checks to make sure the piece hit an edge or other piece"""

        if x2 + direction_x > 3 or x2 + direction_x < 0 or y2 + direction_y > 3 or y2 + direction_x < 0:
            return True  # Next space is off board. Legal stop
        if self.get_board(x2 + direction_x, y2 + direction_y) == "":
            return False  # Next space is open. Illegal move.
        return True  # Passes both stop tests

    def _record_move(self, x1, y1, x2, y2):
        """Record the move on the board"""

        piece_moving = self.get_board(x1, y1)

        # Update the board with the new piece positions
        self._set_board(x2, y2, piece_moving)
        self._set_board(x1, y1, "")

        # Surrounding pieces are turned to the moving pieces color if they aren't blank.
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
        """Checks victory conditions. If one player has no pieces or moves they lose."""

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
        """Check if Red and Yellow have have moves. Updates current state if one of the players lost"""

        # Initialize variables to track if a possible move is found
        red_has_moves = False
        yellow_has_moves = False

        # Loop through every space on the board
        for x in range(4):
            for y in range(4):
                if self.get_board(x, y) != "":  # Blank spaces can't move
                    player = self.get_board(x, y)  # Store the player on the space for this loop cycle

                    # checking in Clockwise order every direction is checked for possible moves for this space.
                    if self._check_move(x, y, x, y + 1):
                        # Theres probably a Better way to do this with less copy paste.
                        # If a move is found the appropriate tracking variable is updated.
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

        # If red or yellow have no possible moves they lose
        if not red_has_moves:
            self._set_current_state("YELLOW_WON")
        if not yellow_has_moves:
            self._set_current_state("RED_WON")
