# Code by Jaime Eduardo Sttivend Velez
# Date:03/24/2019


def queens_attack(n, k, r_q, c_q, obstacles):
    """ Function to calculate te attack movements possible for a queen located in
        row r_q column r_c of a n size board with obstacles located on the
        "obstacles" tuple array.
    """

    queen = (r_q, c_q)
    size = n

    # Preparing a dictionary with all the distances to the obstacles or
    # board limits along with the unitary vector representation of all directions.
    directions = {
        # Horizontals.
        'u': {'unitary_vector': (1, 0), 'distance': -1},      # Up.
        'd': {'unitary_vector': (-1, 0), 'distance': -1},    # Down.
        # Verticals.
        'l': {'unitary_vector': (0, -1), 'distance': -1},    # Left.
        'r': {'unitary_vector': (0, 1), 'distance': -1},     # Right.
        # Diagonals.
        'ur': {'unitary_vector': (1, 1), 'distance': -1},    # Up right.
        'ul': {'unitary_vector': (1, -1), 'distance': -1},   # Up left.
        'dr': {'unitary_vector': (-1, 1), 'distance': -1},   # Down right.
        'dl': {'unitary_vector': (-1, -1), 'distance': -1},  # Down left.
    }

    # For all the obstacles check if they are within the queen's reach
    for pair in obstacles:
        diagonal = abs(pair[0] - queen[0]) - abs(pair[1] - queen[1]) == 0
        vertical = pair[0] == queen[0]
        horizontal = pair[1] == queen[1]

        if diagonal or vertical or horizontal:

            for direction in directions.values():
                substraction = vector_substraction(pair, queen)
                unit = unit_vector(substraction)
                # Check in which direction is the obstacle is
                if direction['unitary_vector'] == unit:
                    # Save the distance to the obstacle only if there is no distance is been saved (-1).
                    if direction['distance'] == -1:
                        direction['distance'] = direct_distance(queen, pair)
                        direction['pair'] = pair
                        break
                    else:
                        # Or if no lesser distance has been saved.
                        if direction['distance'] > direct_distance(queen, pair):
                            direction['distance'] = direct_distance(queen, pair)
                            direction['pair'] = pair
                            break

    distance_sumatory = 0
    for direction in directions.items():
        # For directions without recorded distance to an obstacle, the distance to the edge of the board is saved.
        if direction[1]['distance'] == -1:
            if direction[0] == "u":
                direction[1]['distance'] = direct_distance(queen, (size + 1, queen[1]))
            elif direction[0] == "d":
                direction[1]['distance'] = direct_distance(queen, (0, queen[1]))
            elif direction[0] == "r":
                direction[1]['distance'] = direct_distance(queen, (queen[0], size + 1))
            elif direction[0] == "l":
                direction[1]['distance'] = direct_distance(queen, (queen[0], 0))
            else:

                distance_up = direct_distance(queen, (size + 1, queen[1]))
                distance_down = direct_distance(queen, (0, queen[1]))
                distance_right = direct_distance(queen, (queen[0], size + 1))
                distance_left = direct_distance(queen, (queen[0], 0))

                if direction[0] == "ur":
                    direction[1]['distance'] = min(distance_up, distance_right)
                elif direction[0] == "ul":
                    direction[1]['distance'] = min(distance_up, distance_left)
                elif direction[0] == "dr":
                    direction[1]['distance'] = min(distance_down, distance_right)
                elif direction[0] == "dl":
                    direction[1]['distance'] = min(distance_down, distance_left)
        # Sum of all the distances.
        distance_sumatory += direction[1]['distance']
    steps = []
    for direction in directions.values():
        steps += get_points_in_distance(direction["unitary_vector"], direction["distance"], queen)
        print("st")
        print(steps.__str__())
    directions["steps"] = steps
    return directions


def get_board_from_text(text):
    """ Validates and returns a dictionary from an queen's attack test input text or the
        corresponding validation errors.
    """

    text = text.rstrip()
    lines = text.split("\n")
    line_board = lines[0]

    # Input format validation.
    if len(lines) < 2:
        return "Input not valid, Insufficient number of lines."
    if len(line_board.split(" ")) != 2:
        return "Wrong number of parameters for board status."

    line_queen = lines[1]

    # Queen position format validation.
    if len(line_queen.split(" ")) != 2:
        return "Wrong number of parameters for queen's position."

    size = int(line_board.split(" ")[0])
    obstacle_number = int(line_board.split(" ")[1])
    queen = (int(line_queen.split(" ")[0]), int(line_queen.split(" ")[1]))

    # Input value validation.
    if size < 1 or size > 10**5:
        return "Board's size is not valid."
    if obstacle_number < 0 or obstacle_number > 10**5:
        return "Number of obstacles is not valid."
    for dimension in queen:
        if dimension < 0 or dimension > size:
            return "Queen's location is no valid."

    obstacle_lines = lines[2:]
    obstacles_array = []

    for obstacle_line in obstacle_lines:
        obstacle = (int(obstacle_line.split(" ")[0]), int(obstacle_line.split(" ")[1]))

        # Obstacles validation.
        if obstacle == queen:
            return "Obstacles cannot be located on the same spaces as the queen"
        for dimension in obstacle:
            if dimension < 0 or dimension > size:
                return "Obstacle's location "+str(obstacle)+" is no valid."

        obstacles_array.append(obstacle)

    # Obstacles quantity validation.
    if obstacle_number != len(obstacles_array):
        return "Different number of obstacles :"+len(obstacles_array).__str__() + \
               " than specified:"+obstacle_number.__str__()+"."

    # Output dictionary.
    board = {'size': size,
             'obstacle_number': obstacle_number,
             'queen': queen,
             'obstacles': obstacles_array}


    return board


def direct_distance(a, b):
    """ Counts the number of positions between vector(board position) a and b. """

    if a[0] == b[0]:
        return abs(a[1] - b[1]) - 1
    if a[1] == b[1]:
        return abs(a[0] - b[0]) - 1
    return abs(a[0] - b[0]) - 1


def unit_vector(vector):
    """ Returns a unitary vector representation of vector."""
    return 0 if vector[0] == 0 else vector[0]/abs(vector[0]), 0 if vector[1] == 0 else vector[1]/abs(vector[1])


def vector_substraction(a, b):
    """ Subtracts 2 two dimensional vectors element by element.
    """
    return a[0] - b[0], a[1] - b[1]

def vector_sum(a, b):
    """ Subtracts 2 two dimensional vectors element by element.
    """
    return a[0] + b[0], a[1] + b[1]

def vector_multiplication(a,b):

    return a[0]* b, a[1]*b

def extract_text_from_file():
    with open('input') as fp:
        return fp.read()

def get_points_in_distance(unit_vector,distance,queen):
    if distance == 0:
        return []
    return_vector = []
    for i in range(1, distance+1):
        return_vector.append(vector_sum(queen, vector_multiplication(unit_vector, i)))
    print("fin x")
    return return_vector


def get_distance_to_wall(distance, direction, unitvector, queen):
    return 0