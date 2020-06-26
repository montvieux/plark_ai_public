# converts the grid based 'oddq' method of storing map into the cubed
# coordinate system this makes it easiser to run search algorthems (apparently)
def oddq_to_cube(col, row):
    x = col
    z = row - (col - (col & 1)) / 2
    y = -x-z
    cube = {
        'x': x,
        'y': y,
        'z': z
    }
    return (cube)

# converts the cubed cooordinate back in to 'oddq' method
def cube_to_oddq(cube):
    col = int(cube['x'])
    row = int(cube['z'] + (cube['x'] - (cube['x'] & 1)) / 2)
    return col, row

def getNeighbours(direction, currentCol, currentRow):
    cube = oddq_to_cube(currentCol, currentRow)
    # https://www.redblobgames.com/grids/hexagons/
    if direction == 1:
        # UP.
        cube['z'] = cube['z'] - 1
        cube['y'] = cube['y'] + 1

    if direction == 2:
        # UP right
        cube['x'] = cube['x'] + 1
        cube['z'] = cube['z'] - 1

    if direction == 3:
        # Down right
        cube['x'] = cube['x'] + 1
        cube['y'] = cube['y'] - 1

    if direction == 4:
        # down
        cube['z'] = cube['z'] + 1
        cube['y'] = cube['y'] - 1

    if direction == 5:
        # down left
        cube['x'] = cube['x'] - 1
        cube['z'] = cube['z'] + 1

    if direction == 6:
        # up left
        cube['x'] = cube['x'] - 1
        cube['y'] = cube['y'] + 1

    newCol, newRow = cube_to_oddq(cube)
    return newCol, newRow

def withinMap(col, row, num_cols, num_rows):
    return (0 <= col < num_cols) and (0 <= row < num_rows)

# Gets the distance between two point on the map
# Points 1 and 2 are provided in oddq format[col,row]
# returns an integer of distance.
def distance(point1_col, point1_row, point2_col, point2_row):
    point1Cube = oddq_to_cube(point1_col, point1_row)
    point2Cube = oddq_to_cube(point2_col, point2_row)

    return max(abs(point1Cube['x'] - point2Cube['x']), abs(point1Cube['y'] - point2Cube['y']), abs(point1Cube['z'] - point2Cube['z']))

# Returns every cell coordinate in a set range around a set point
# Input :
#           Startlocation [col,row]
#           r int
def getRadius(start_col, start_row, r, num_cols, num_rows):

    startCube = oddq_to_cube(start_col, start_row)
    results = []

    # Start and end points for searching range, end ranges need extra +1
    # due to python range(start,end) not being inclusing of the end value
    xStart = int(startCube['x']-r)
    xEnd = int(startCube['x'] + r) + 1
    yStart = int(startCube['y']-r)
    yEnd = int(startCube['y']+r) + 1

    for nx in range(xStart, xEnd):
        for ny in range(yStart, yEnd):
            nz = -nx-ny
            if (nz <= startCube['z']+r) and (nz >= startCube['z']-r):
                cube = {
                    'x': nx,
                    'y': ny,
                    'z': nz
                }
                col, row = cube_to_oddq(cube)
                if withinMap(col, row, num_cols, num_rows):
                    results.append({
                        'col': col,
                        'row': row
                    })

    return results

def get_path(start_location_col,  start_location_row, end_locataion_col, end_locataion_row, num_cols, num_rows):

    class Node():
        def __init__(self, col, row, g, h, parent=None):
            self.col = col
            self.row = row
            self.parent = parent
            self.g = g # graphical score, the amount of moves from the starting location 
            self.h = h # heuristic score, the distance from current node to end location
            self.f = g + h # final score, the sum of the above.

    def make_path(node, path=[]):
        # recursive function to add the locationof each nodes parent node untill the starting node is found.
        # This starts at the end_location, and travels backwards along the shortest generated route. 
        if node.parent != None:
            path.insert(0, {"col": node.col, "row": node.row})
            return (make_path(node.parent, path)) 
        else:
            return path
            
    start_node = Node(start_location_col, start_location_row , 0, distance(start_location_col, start_location_row ,end_locataion_col, end_locataion_row))

    # this list is used to store all locations that hve not been processed yet 
    open_list = [start_node]

    # this list containes all locations that have been processed
    closed_list = []
    goal_reached = False
    
    while not goal_reached:

        # get the node(hex location) from the open list that has the lowest f score (the node with the best change of being a viable step)
        currentNode = min(open_list, key=lambda n: n.f)

        if (currentNode.col == end_locataion_col) and (currentNode.row == end_locataion_row):
            goal_reached = True
            closed_list.append(currentNode)

        else:
            # get all the neighbours for the current node
            neighbours = getRadius(currentNode.col, currentNode.row,1, num_cols, num_rows)

            # move current node to the closed list it is considered processed
            closed_list.append(currentNode)
            open_list.remove(currentNode)
            parent_node = currentNode

            for n in neighbours:
                # n = list(n) # this is needed due to an issue in the map functions returing a tupil
                if (n['col'] != parent_node.col) or (n['row'] != parent_node.row): # test if the neighbour is the parent. the get radius function includes the starting location in its results but we dont want it here.
                    new_g = parent_node.g + 1

                    # the n value is just a cordinate if they are already recorded in the open/closed lists we need the node object to modify 
                    # normally you wouldn't have to do this but due to the way we get neighbours this was the simplest option.
                    current_node_closed = next((x for x in closed_list if (x.col == n['col']) and (x.row == n['row'])), None)
                    current_node_open = next((x for x in open_list if (x.col == n['col']) and (x.row == n['row'])), None)

                    # test if the node is in the list if the amount of steps taken to get there is better than what is already recorded
                    # update the node for the new parent 
                    if current_node_closed in closed_list and new_g < current_node_closed.g:
                        current_node_closed.g = new_g
                        current_node_closed.parent = parent_node

                    elif current_node_open in open_list and new_g < current_node_open.g:
                        current_node_open.g = new_g
                        current_node_open.parent = parent_node

                    # If the node has not been added to any list create a node and add it to the open list
                    elif current_node_open not in open_list and current_node_closed not in closed_list:
                        open_list.append(Node(n['col'], n['row'], new_g, distance(n['col'], n['row'], end_locataion_col, end_locataion_row), parent_node))
  
    # make the path.
    return(make_path(closed_list[-1]))

# Returns a list of every object of 'searchType' within a radius 'r' of a startlocation
#  current implementation requires the search type to be of a class e.g.
#
def searchRadius(grid, start_col, start_row, r, searchType):
    num_cols = len(grid)
    num_rows = len(grid[0])
    searchList = getRadius(start_col, start_row, r, num_cols, num_rows)
    returnList = []
    for cell in searchList:
        if withinMap(cell['col'], cell['row'], num_cols, num_rows):
            cell = grid[cell['col']][cell['row']]
            for item_type, item_state in cell['objects'].items():
                if item_type in searchType:
                    returnList.append({"type": item_type, "state": item_state})
    return returnList

