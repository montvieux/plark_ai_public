import json
import jsonpickle
import copy


class HexCell():
    def __init__(self, col, row):
        self.coordinate = {
            'row': row,
            'col': col
        }
        self.HexType = 0  # this will be used for water depth and land later on
        self.objects = []
        # Storage of items in the hex cell

    # Returns the objects in the cell
    def getCellObjects(self):
        return self.objects

class Map():
    # constructor
    def __init__(self, cols, rows):
        self.rows = rows
        self.cols = cols
        self._grid = [[0 for x in range(self.rows)] for y in range(self.cols)]

        for row in range(self.rows):
            for col in range(self.cols):
                self._grid[col][row] = HexCell(col, row)

    def toJson(self):
        return jsonpickle.encode(self._grid)

    def getGrid(self,view,panther_col,panther_row):
        if view not in ['PELICAN','PANTHER','ALL']:
            raise ValueError('Incorrect view must be "PELICAN","PANTHER" or "ALL"  ')
        #Remove the panther if the view is pelican.
        if view == "PELICAN":
            grid = copy.deepcopy(self._grid)
            hexCell = grid[panther_col][panther_row] 
            objects = [] 
            panther_found = False
            for item in hexCell.objects:
                if item.type == "PANTHER":
                    panther_found = True
                else:
                    objects.append(item)
            if panther_found is False:
                print('Did not find panther in grid as expected')
            hexCell.objects = objects   
            grid[panther_col][panther_row] = hexCell
            return grid
        else:
            return self._grid

    # def UIOutput(self, view ):
    #     if view not in ['PELICAN','PANTHER','ALL']:
    #         raise ValueError('Incorrect view must be "PELICAN","PANTHER" or "ALL"  ')

    #     uiOutput = [[0 for x in range(self.rows)] for y in range(self.cols)]

    #     for col in range(self.cols):
    #         for row in range(self.rows):
    #             uiOutput[col][row] = {
    #                 "HexType": 0,
    #                 "coordinate": [
    #                     col,
    #                     row
    #                 ],
    #                 "objects": {}
    #             }                      

    #     for col in range(self.cols):
    #         for row in range(self.rows):
       
    #             hexCell = self._grid[col][row]
    #             if view in ["PANTHER","ALL"]:
    #                 for item in hexCell.getCellObjects():
    #                     if item.type == 'SONOBUOY':
    #                         uiOutput[col][row]['objects'][item.type] = item.state

    #                         # add marker to all in radius 
    #                         sonar_area = self.getRadius(item.col, item.row, item.range)
    #                         for cell in sonar_area:
    #                             cell_col = cell['col']
    #                             cell_row = cell['row']
    #                             uiOutput[cell_col][cell_row]['objects']['sonar_area'] = item.state
                        
    #                     else:
    #                         uiOutput[col][row]['objects'][item.type] = True

    #             elif view == "PELICAN":
    #                 for item in hexCell.getCellObjects():
    #                     if item.type == 'SONOBUOY':
    #                         uiOutput[col][row]['objects'][item.type] = item.state

    #                         # add marker to all in radius 
    #                         sonar_area = self.getRadius(item.col, item.row, item.range)
    #                         for cell in sonar_area:

    #                             cell_col = cell['col']
    #                             cell_row = cell['row']
    #                             uiOutput[cell_col][cell_row]['objects']['sonar_area'] = item.state
    #                     elif item.type == "PANTHER":
    #                         pass

    #                     else:
    #                         uiOutput[col][row]['objects'][item.type] = True

    #     return jsonpickle.encode(uiOutput) 

    def is_item_type_in_cell(self, item_type, col, row): 
        cell = self.getCell(col, row)
        found = False
        for item in cell.objects:
            if item.type == item_type:
                found = True
                break
        return found

    # Returns a set HexCell object
    def getCell(self, col, row):
        return self._grid[col][row]

    # Add a new item to the board this also set the items current location to match that of the location provided
    def addItem(self, col, row, item):
        item.col = col
        item.row = row
        self._grid[col][row].objects.append(item)

    # Remove an item from the board
    def removeItem(self, item):
        col = item.col
        row = item.row
        self._grid[col][row].objects.remove(item)

    # Utility function for moving an item around the board items are removed then re-added to the board in the new location
    def moveItem(self, item, new_col, new_row):
        self.removeItem(item)
        self.addItem(new_col, new_row, item)

    # Returns a list of every object of 'searchType' within a radius 'r' of a startlocation
    #  current implementation requires the search type to be of a class e.g.
    def searchRadius(self, start_col, start_row, r, searchType):
        searchList = self.getRadius(start_col, start_row, r)
        returnList = []
        for cell in searchList:
            if self.withinMap(cell['col'], cell['row']):
                cellObj = self.getCell(cell['col'], cell['row'])
                for item in cellObj.getCellObjects():
                    if item.type in searchType:
                        returnList.append(item)
        return returnList

    def withinMap(self, col, row):
        return (0 <= col < self.cols) and (0 <= row < self.rows)

    # Returns every cell coordinate in a set range around a set point
    # Input :
    #           Startlocation [col,row]
    #           r int
    def getRadius(self, start_col, start_row, r):

        startCube = self.oddq_to_cube(start_col, start_row)
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
                    col, row = self.cube_to_oddq(cube)
                    if self.withinMap(col, row):
                        results.append({
                            'col': col,
                            'row': row
                        })

        return results

    def getNeighbours(self, direction, currentCol, currentRow):

        cube = self.oddq_to_cube(currentCol, currentRow)
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

        newCol, newRow = self.cube_to_oddq(cube)
        return newCol, newRow

    # Gets the distance between two point on the map
    # Points 1 and 2 are provided in oddq format[col,row]
    # returns an integer of distance.
    def distance(self, point1_col, point1_row, point2_col, point2_row):
        point1Cube = self.oddq_to_cube(point1_col, point1_row)
        point2Cube = self.oddq_to_cube(point2_col, point2_row)

        return max(abs(point1Cube['x'] - point2Cube['x']), abs(point1Cube['y'] - point2Cube['y']), abs(point1Cube['z'] - point2Cube['z']))

    # Returns a list of all edge hexes on the map
    def get_edges(self):
        edges = []
        for col in range(self.cols):
            for row in range(self.rows):
                if ((col == 0) or (col == (self.cols - 1))) or ((row == 0) or (row == (self.rows - 1))):
                    edges.append({'col': col, 'row': row})
        return edges

    def get_path(self, start_location_col,  start_location_row, end_locataion_col, end_locataion_row):

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
                
        start_node = Node(start_location_col, start_location_row , 0, self.distance(start_location_col, start_location_row ,end_locataion_col, end_locataion_row))

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
                neighbours = self.getRadius(currentNode.col, currentNode.row,1)

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
                            open_list.append(Node(n['col'], n['row'], new_g, self.distance(n['col'], n['row'], end_locataion_col, end_locataion_row), parent_node))
      
        # make the path.
        return(make_path(closed_list[-1]))
        

    # converts the cubed cooordinate back in to 'oddq' method
    def cube_to_oddq(self, cube):
        col = int(cube['x'])
        row = int(cube['z'] + (cube['x'] - (cube['x'] & 1)) / 2)
        return col, row

    # converts the grid based 'oddq' method of storing map into the cubed
    # coordinate system this makes it easiser to run search algorthems (apparently)
    def oddq_to_cube(self, col, row):
        x = col
        z = row - (col - (col & 1)) / 2
        y = -x-z
        cube = {
            'x': x,
            'y': y,
            'z': z
        }
        return (cube)
