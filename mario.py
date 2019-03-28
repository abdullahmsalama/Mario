import copy
from operator import itemgetter

def find_index(matrix, var_to_search_for):
    if var_to_search_for == '-':
        raise Exception('Cannot search for empty chars')
    found = 0
    for index1 in range(len(matrix)):
        if found == 1:
            index1 -= 1
            break
        if var_to_search_for in matrix[index1]:
            index2 = matrix[index1].index(var_to_search_for)
            found = 1
            break
    if found == 0:
        raise Exception('Element is not found')
    return index1, index2


def convert_rowgrid_to_2Dgrid(N, grid):
    # convert to N*N matrix, returns error if not a square grid or if the grid contains any char except 'm', 'p' or '-'
    grid_matrix = []
    # to count marios, princess, obstacles and empty cells count to ensure a proper grid
    mario_count = 0
    princess_count = 0
    obstacle_count = 0
    empty_count = 0
    for i in range(len(grid)):
        # append the row to create a two dimensional matrix
        grid_matrix.append(list(grid[i]))
        # this if condition to check that the grid matrix is N*N, if not it returns an empty grid
        if N != len(grid) or N != len(grid[i]):
            grid_matrix = []
            return grid_matrix
        # count obstacles, mario, princess occurences to ensure that only one mario and princess exist,
        # and the rest are obstacles or empty cells
        for j in range(len(grid[i])):
            if 'm' == grid[i][j]:
                mario_count += 1
            elif 'p' == grid[i][j]:
                princess_count += 1
            elif 'x' == grid[i][j]:
                obstacle_count += 1
            elif '-' == grid[i][j]:
                empty_count += 1
            else:
                grid_matrix = []
                return grid_matrix

    # returns an empty grid if there is more than one mario or princess, or other elements except empty blocks or obstacles
    if mario_count != 1 or princess_count != 1 or empty_count != N ** 2 - obstacle_count - 2:
        grid_matrix = []
        return grid_matrix
    return grid_matrix

# A search function inside the grid to find the shortest paths
def search(grid, x, y, path=[], direction=[]):
    #if the princess is found, mark as visited and append the path that reaches her
    if grid[x][y] == 'p':
        path.append(direction)
        grid[x][y] = 'v'
        global shortest_paths
        #append the path in case it is as short as the shortest path, otherwise if shorter, add the path as the only shortest path.
        if shortest_paths:
            if len(path) == len(shortest_paths[0]):
                shortest_paths.append(path)
                shortest_paths_lengths.append(len(path))
            elif len(path) < len(shortest_paths[0]):
                shortest_paths = []
                shortest_paths.append(path)
                shortest_paths_lengths.append(len(path))
        else:
            shortest_paths.append(path)
            shortest_paths_lengths.append(len(path))
        return shortest_paths
    # if an obstacle found, return and don't append path
    elif grid[x][y] == 'x':
        return
    # if a visited node found, that means the recursive path finder went on circle, hence return and don't append
    elif grid[x][y] == 'v':
        return
    # mark as visited
    grid[x][y] = 'v'

    # append if not the first time it enters the function (direction is not empty)
    if direction:
        path.append(direction)

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid) - 1)):
        search(copy.deepcopy(grid), x + 1, y, copy.copy(path), 'DOWN')
    if (y > 0):
        search(copy.deepcopy(grid), x, y - 1, copy.copy(path), 'LEFT')
    if (x > 0):
        search(copy.deepcopy(grid), x - 1, y, copy.copy(path), 'UP')
    if (y < len(grid) - 1):
        search(copy.deepcopy(grid), x, y + 1, copy.copy(path), 'RIGHT')


def play(N, grid):
    global shortest_paths
    global shortest_paths_lengths
    shortest_paths = []
    shortest_paths_lengths = []

    grid_matrix = convert_rowgrid_to_2Dgrid(N, grid)
    # if the grid_matrix is retreived as not empty, that means it passes the input checks and shortest_paths sould be retreived and error_flag
    # should be False
    if grid_matrix:
        index1_mario, index2_mario = find_index(grid_matrix, 'm')
        grid = copy.deepcopy(grid_matrix)
        search(grid, index1_mario, index2_mario)
        error_flag = False
    else:
        error_flag = True

    print("\nShortest paths are:", shortest_paths, "\nError Status is", error_flag)
    return shortest_paths, error_flag

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='calls the mario play')
    parser.add_argument("N", type=int,
                        help='Grid size (N*N)')
    parser.add_argument("grid", type=str,
                        help='The grid including mario, the princess, obstacles and empty blocks, example: \"[\'---\',\'-x-\',\'--p\']\"')
    args = parser.parse_args()
    play(args.N, eval(args.grid))