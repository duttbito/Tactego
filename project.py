"""
File:    tactego.py
Author:  Timmy Nguyen
Date:    11/29/23
Section: 32
E-mail:  tnguye34@umbc.edu
Description:
  Run a simplified tactego game
	"""


import random

# function used to put the red pieces onto the board
def insert_red_player_to_the_grid(grid, h, w, player_list):
    
    red_player_grid = grid
    n = 0
    #used to enter row of 2d list
    for i in range(0, h):
        #used to enter column of 2d list
        for j in range(0, w):
            if n <= len(player_list) - 1:
                red_player_grid[i][j] = player_list[n]
                n = n + 1
    
    return red_player_grid

# function to put the blue pieces onto the board
def insert_blue_player_to_the_grid(grid, h, w, player_list):
    
    blue_player_grid = grid
    n = 0
    #used to enter row of the board
    for i in range(h - 1, -1, -1):
        #used to enter column of the board
        for j in range(0, w):
            if n <= len(player_list) - 1:
                blue_player_grid[i][j] = player_list[n]
                n = n + 1
    
    return blue_player_grid

# drawing the board with Red and Blue pieces on it
def set_up_draw_board(game_grid, h, w):
    blank_empty = "     "
    blank_after_piece = "   "
    
    game_board_grid = [["" for x in range(w)] for y in range(h)]
    
    #used to enter row of the board
    for i in range(0, h):
        #used to enter the column of the board
        for j in range(0, w):
            if game_grid[i][j] == "":
                game_board_grid[i][j] = blank_empty
            else:
                game_board_grid[i][j] = game_grid[i][j] + blank_after_piece
                
    return game_board_grid

def draw_board(game_grid, h, w):
    blank_after_column = "    "
    
    game_board_grid = [["" for x in range(w)] for y in range(h)] 
    game_board_grid = set_up_draw_board(game_grid, h, w)
    
    #Print column headers
    for n in range(0, w + 1):
        if n == 0:
            print("  ", end="")
        else:
            print(str(n - 1) + blank_after_column, end="")
    print("")
    
    #Print the rest of the board
    for i in range(0, h):
        for j in range(0, w + 1):
            if j == 0:
                print(str(i) + " ", end="")
            else:
                print(game_board_grid[i][j - 1], end="")
        print("")

# Asigning either "R" or "B" in front of the pieces list to indicate Red or Blue
def create_player_list(color, game_list):
    the_pieces_list = []
    
    for game_pieces in game_list:
        the_pieces = color + game_pieces
        the_pieces_list.append(the_pieces)

    return the_pieces_list 

def player_move(game_grid, length, width, color):
    #ask for specific piece to move by positions
    piece_selection = input("Select Piece to Move by Position >> ")
    num_list_select = piece_selection.split()
    from_y = int(num_list_select[0])
    from_x = int(num_list_select[1])
    
    #check if the piece user chooses is within the range
    if not is_within_range(from_y, from_x, length, width):
        return "Out of range"

    #check if user picks a position that is empty    
    while game_grid[from_y][from_x] == "":
        print("You must selecting a starting position with one of your pieces, not a flag.")
        piece_selection = input("Select Piece to Move by Position >> ")
        num_list_select = piece_selection.split()
        from_y = int(num_list_select[0])
        from_x = int(num_list_select[1])
    
    #used to check if the user has selected a mine piece
    while game_grid[from_y][from_x][-1] == "M":
        print("You must selecting a starting position with one of your pieces, not a flag.")
        piece_selection = input("Select Piece to Move by Position >> ")
        num_list_select = piece_selection.split()
        from_y = int(num_list_select[0])
        from_x = int(num_list_select[1])

    #check if the piece user chooses is legal/is moveable
    count_input_failure = 0
    
    #checks if the user has selected a flag piece or empty space
    while not is_piece_to_move_legal(game_grid, from_y, from_x, length, width, color):
        print("You must selecting a starting position with one of your pieces, not a flag.")
        piece_selection = input("Select Piece to Move by Position >> ")
        num_list_select = piece_selection.split()
        from_y = int(num_list_select[0])
        from_x = int(num_list_select[1])
        
        count_input_failure = count_input_failure + 1
    
    #ask for specific position the user wants to move the piece
    piece_moving_to = input("Select Position to move Piece >> ")
    num_list_move = piece_moving_to.split()
    to_y = int(num_list_move[0])
    to_x = int(num_list_move[1])

    #check if the position the piece is moved to is within the range
    if not is_within_range(to_y, to_x, length, width):
        return "Out of range"

    #to check whether the position the piece is moved to is allowed
    count_input_failure = 0
    #if the user cannot move the piece after 3 tries, it resets the turn and asks for a different piece
    while not is_position_to_move_piece_legal(game_grid, from_y, from_x, to_y, to_x, length, width, color):
        if count_input_failure >= 3:
            return "max input failure"
        else:
            print("You must select an ending position which is either empty or has an empty piece.")
            piece_moving_to = input("Select Position to move Piece >> ")
            num_list_move = piece_moving_to.split()
            to_y = int(num_list_move[0])
            to_x = int(num_list_move[1])
            
            count_input_failure = count_input_failure + 1

    #used to check if piece is moving into an empty space
    if game_grid[to_y][to_x] == "":
        game_grid[to_y][to_x] = game_grid[from_y][from_x]
        game_grid[from_y][from_x] = ''
    
    #used to check if piece is moving into a space with a opposing piece
    else:
        #check if attacker beats out the defender
        if who_win_duel(game_grid[from_y][from_x], game_grid[to_y][to_x]) == game_grid[from_y][from_x]:
            #replace defender with attacker
            game_grid[to_y][to_x] = game_grid[from_y][from_x]
            #gets rid of the original position of the attacker
            game_grid[from_y][from_x] = ''
        else:
            #checks if the defender won, if so the attacker goes away and defender stays
            game_grid[from_y][from_x] = ''

    return ''

def tactego(pieces_file, length, width, test_seed):  

    game_list = []
    #open the file and read it
    the_file = open(pieces_file, "r")
    line_split = []
    for line in the_file:
        line_split = line.split()
    

        for i in range(0, int(line_split[1])):
            game_list.append(line_split[0])
    
    #player red 
    random.seed(test_seed)
    random.shuffle(game_list)
    #put the shuffled red pieces into a list
    red_pieces_list = []
    red_pieces_list = create_player_list("R", game_list)

    #player blue
    random.seed(test_seed)
    random.shuffle(game_list)
    #put the shuffled blue pieces into a list
    blue_pieces_list = []
    blue_pieces_list = create_player_list("B", game_list)

    game_grid = [["" for x in range(width)] for y in range(length)]

    game_grid = insert_red_player_to_the_grid(game_grid, length, width, red_pieces_list)
    game_grid = insert_blue_player_to_the_grid(game_grid, length, width, blue_pieces_list)

    #draw initial board based on randomized seed
    draw_board(game_grid, length, width) 

    #if no one has won the game, enter this while loop
    while who_win_whole_game(game_grid) == "no one":
        #Red player goes first
        player_move_result = player_move(game_grid, length, width, "R") 
        
        if player_move_result == "Out of range":
            return "Out of range"
        elif player_move_result == "max input failure":
            print("Starting again, did not select a valid end move after 3 tries.")
        
        #if red has not won the game yet, it goes to blue
        else:
            draw_board(game_grid, length, width)
            if who_win_whole_game(game_grid) == "no one":
                player_move_result = player_move(game_grid, length, width, "B")
                if player_move_result == "Out of range":
                    return "Out of range"
                elif player_move_result == "max input failure":
                    print("Starting again, did not select a valid end move after 3 tries.")
                    
                    #boolean flag to check if the player is still failing
                    is_max_input_failure = True
                    while is_max_input_failure:
                        player_move_result = player_move(game_grid, length, width, "B")
                        if player_move_result == "Out of range":
                            return "Out of range"
                        elif player_move_result == "max input failure":
                            print("Starting again, did not select a valid end move after 3 tries.")
                        #if the position the piece moves to is legal, it goes out of the while loop
                        else:
                            draw_board(game_grid, length, width)
                            is_max_input_failure = False                       
                else:    
                    draw_board(game_grid, length, width)

    return who_win_whole_game(game_grid)
    
# to check if a red/blue piece beats the other red/blue piece
def who_win_duel(attacker, defender):
    #if the defender is the flag, the attacker wins
    if defender[-1] == "F":
        return attacker
    #if the defender is the assassin, the attacker wins
    elif defender[-1] == "A":
        return attacker
    #if the attacker is an assassin, the assassin wins
    elif attacker[-1] == "A":
        return attacker
    #if the defender is the sapper, the attaacker wins
    elif defender[-1] == "S":
        return attacker
    #checks if attacker is a sapper
    elif attacker[-1] == "S":
        #if a sapper attacks another sapper, the attacking sapper wins
        if defender[-1] == "S":
            return attacker
        #if a sapper attacks a mine, it defeats the mine 
        elif defender[-1] == "M":
            return attacker
        #if a sapper attacks a normal piece, it loses automatically
        else:
            return defender
    #if the anyone attacks a mine, the mine wins
    elif defender[-1] == "M":
        return defender 
    #if the attacker strength is the same or higher than defender, the attcker wins
    else:
        if int(attacker[-1]) >= int(defender[-1]):
            return attacker
        #if attacker attacks a defender with a higher strength, the attacker loses
        else:
            return defender

def who_win_whole_game(grid):
    #red and blue flag count to see if it still exists in grid
    red_flag_count = 0
    blue_flag_count = 0
    
    #loop to enter inside of a 2d list
    for i in range(0, length):
        for j in range(0, width):
            if grid[i][j] == 'RF':
                red_flag_count += 1
            elif grid[i][j] == 'BF':
                blue_flag_count += 1
    
    #check whether blue, red, or neither have won the game
    if blue_flag_count == 0:
        return 'R has won the game'
    elif red_flag_count == 0:
        return 'B has won the game'
    else:
        return 'no one'

#check if a selected piece is within the grid/board length
def is_within_range(y, x, length, width):
    if (0 <= y < length) and (0 <= x < width): #cannot be out of range
        return True
    else:
        return False
    
def is_piece_to_move_legal(grid, y, x, length, width, color):
    if grid[y][x] != "": #cannot select an empty piece
        if grid[y][x][0] == color: #must select your own piece (color)
            if grid[y][x][-1] != 'F':
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def is_position_to_move_piece_legal(grid, from_y, from_x, to_y, to_x, length, width, color):
    if (from_y -1 <= to_y <= from_y + 1) and (from_x -1 <= to_x <= from_x + 1):
        if grid[to_y][to_x] == "": #If moves to empty slot
            return True
        else:
            if grid[to_y][to_x][0] != color: #Cannot move into own piece (color)
                return True
            else:
                return False
    else:
        return False

if __name__ == '__main__':
    pick_seed = input("What is the seed? ")
    random.seed(pick_seed)
    file_name = input('What is the filename for the pieces? ')
    length = int(input('What is the length? '))
    width = int(input('What is the width? '))
    
    tactego_result = tactego(file_name, length, width, pick_seed)
    
    if tactego_result == "Out of range":
        print("Error, terminating...")
    else:
        print(tactego_result)



