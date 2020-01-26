import numpy as np
import random

''' ************* Configuration ************* '''
# Computer board
dimension = 5
computer_board = np.zeros((dimension, dimension), dtype=np.str)
computer_board[:] = "."
board_size = computer_board.size // dimension
rows = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

# Player board
player_board = np.zeros((dimension, dimension), dtype=np.str)
player_board[:] = "."
typed_x = []
typed_y = []

# Ships
small_ship_size = 3
number_of_small_ships = 2
number_of_ships = 4
sunked_ships = 0
hits_counter = 0

''' Vertical ships '''
# Position of 1st vertical ship
ship1_verti_X = []
ship1_verti_Y = []

# Position of 2nd vertical ship
ship2_verti_X = []
ship2_verti_Y = []

''' Horizontal ships '''
# Position of 1st horizontal ship
ship1_hori_X = []
ship1_hori_Y = []

# Position of 2nd horizontal ship
ship2_hori_X = []
ship2_hori_Y = []

# Transfered
def draw_player_board():
    columns = "\n    " + "   ".join(([str(i + 1) for i in range(board_size)]))
    print(columns)

    for i in range(int(board_size)):
        print(rows[i], player_board[i])

# Transfered
def validate_horizontally(board, x_index, y_index):
    result = True

    for i in range(small_ship_size):
        x_pos = x_index + i
        y_pos = y_index
        if board[y_pos][x_pos] != ".":
            result = False
            break
        else:
            result = True

    return result

# Transfered
def validate_pos_vert_ship(x_index, y_index):
    x_pos = []
    y_pos = []
    result = False

    for i in range(small_ship_size):
        x_pos.append(x_index)
        y_pos.append(y_index + i)

    if any(elem in x_pos for elem in ship1_verti_X) and not any(elem in y_pos for elem in ship1_verti_Y):
        result = True

    elif any(elem in y_pos for elem in ship1_verti_Y) and not any(elem in x_pos for elem in ship1_verti_X):
        result = True

    elif not any(elem in x_pos for elem in ship1_verti_X) and any(elem in y_pos for elem in ship1_verti_X):
        result = True

    else:
        result = False

    x_pos.clear()
    y_pos.clear()

    return result

# Transfered
def set_vertically_small_ships(board):
    i = 0
    located_ships = 0

    while located_ships < number_of_small_ships:

        x_index = random.randrange(board_size)
        y_index = random.randrange(board_size - 2)
        position = True

        if located_ships == 0:
            for i in range(small_ship_size):
                board[y_index + i][x_index] = "x"
                ship1_verti_Y.append(y_index + i)
                ship1_verti_X.append(x_index)
                i += 1

                if i == small_ship_size:
                    position = False
                    located_ships += 1
                    i = 0

        if located_ships == 1 and validate_pos_vert_ship(x_index, y_index):

            while position:
                board[y_index + i][x_index] = "x"
                ship2_verti_Y.append(y_index + i)
                ship2_verti_X.append(x_index)
                i += 1

                if i == small_ship_size:
                    position = False
                    located_ships += 1

    return board

# Transfered
def validate_pos_hori_ship(x_index, y_index):
    x_pos = []
    y_pos = []
    result = False

    for i in range(small_ship_size):
        x_pos.append(x_index + i)
        y_pos.append(y_index)

    if any(elem in x_pos for elem in ship1_hori_X) and not any(elem in y_pos for elem in ship1_hori_Y):
        result = True

    elif any(elem in y_pos for elem in ship1_hori_Y) and not any(elem in x_pos for elem in ship1_hori_X):
        result = True

    elif not any(elem in x_pos for elem in ship1_hori_X) and any(elem in y_pos for elem in ship1_hori_X):
        result = True

    else:
        result = False

    x_pos.clear()
    y_pos.clear()

    return result

# Transfered
def set_horizontally_small_ships(board):
    should_break1 = True
    should_break2 = True
    located_ships = 0

    while located_ships < number_of_small_ships:

        if located_ships == 0:

            # Generating 1st ship
            while should_break1:
                x_index = random.randrange(board_size - 2)
                y_index = random.randrange(board_size)

                position_one = validate_horizontally(board, x_index, y_index)

                if position_one:
                    should_break1 = False
                    for i in range(small_ship_size):
                        ship1_hori_Y.append(y_index)
                        ship1_hori_X.append(x_index + i)
                        board[y_index][x_index + i] = "x"
                        continue

        located_ships += 1

        if located_ships == 1:

            # Generating 2nd ship
            while should_break2:
                x_index = random.randrange(board_size - 2)
                y_index = random.randrange(board_size)

                position_two = validate_horizontally(board, x_index, y_index)

                if position_two:
                    should_break2 = False
                    for i in range(small_ship_size):
                        ship2_hori_Y.append(y_index)
                        ship2_hori_X.append(x_index + i)
                        board[y_index][x_index + i] = "x"
                        continue

        located_ships += 1


def validate_coordinates(x, y):

    if not x.isdigit() or not y.isalpha():
        print("\nIncorrect type!")
        return False

    else:
        x = int(x)
        if x >= 10 or x <= 0 or y not in rows:
            print("Wrong coordinates!")
            return False

        else:
            return True


def hit(x, y, player_board):
    global sunked_ships
    global hits_counter
    should_break = True

    y = rows.index(y)

    for i in range(len(typed_x)):
        x_typed = typed_x[i]
        y_typed = typed_y[i]
        if (typed_x is None and typed_y is None) or (x == x_typed and y == y_typed):
            print("\nYou have shot here already, please choose another position.")
    else:
        #TODO skalibrowac counter
        hits_counter += 1
        typed_x.append(x)
        typed_y.append(y)
        # Checking 1st vertical ship
        if x in ship1_verti_X and y in ship1_verti_Y:
            ship1_verti_Y.remove(y)
            ship1_verti_X.remove(x)
            player_board[y][x] = "x"
            print("\nHit!")

            if ship1_verti_X == [] and ship1_verti_Y == []:
                print("Sunked!")
                sunked_ships += 1

        # Checking 2nd vertical ship
        elif x in ship2_verti_X and y in ship2_verti_Y:
            ship2_verti_Y.remove(y)
            ship2_verti_X.remove(x)
            player_board[y][x] = "x"
            print("\nHit!")

            if ship2_verti_X == [] and ship2_verti_Y == []:
                print("Sunked!")
                sunked_ships += 1

        # Checking 1st horizontal ship
        elif x in ship1_hori_X and y in ship1_hori_Y:
            ship1_hori_Y.remove(y)
            ship1_hori_X.remove(x)
            player_board[y][x] = "x"
            print("\nHit!")

            if ship1_hori_X == [] and ship1_hori_Y == []:
                print("Sunked!")
                sunked_ships += 1

        # Checking 2nd horizontal ship
        elif x in ship2_hori_X and y in ship2_hori_Y:
            ship2_hori_Y.remove(y)
            ship2_hori_X.remove(x)
            player_board[y][x] = "x"
            print("\nHit!")

            if ship2_hori_X == [] and ship2_hori_Y == []:
                print("Sunked!")
                sunked_ships += 1
        else:
            print("\nMiss!")
            player_board[y][x] = "o"

        if sunked_ships == number_of_ships:
            print("\nAll ships are sunked!")
            print("It took you ", hits_counter, " moves.")
            draw_player_board()
            should_break = False

        return should_break, player_board


set_vertically_small_ships(computer_board)
set_horizontally_small_ships(computer_board)

should_break = True
while should_break:
    draw_player_board()

    hit_x = input("\nSelect a column: ")
    hit_y = input("Select a row: ")

    valid = validate_coordinates(hit_x, hit_y)

    if valid:
        hit_x = int(hit_x)
        should_break, player_board = hit(hit_x - 1, hit_y, player_board)

    else:
        continue