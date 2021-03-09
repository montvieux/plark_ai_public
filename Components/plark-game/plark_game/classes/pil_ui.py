from PIL import Image, ImageDraw, ImageFont
import json
import jsonpickle
import os
import io
import numpy as np
from datetime import datetime
import logging
import math
from .map import Map
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HexagonalGrid():
    """ A grid whose each cell is hexagonal """

    def __init__(self, scale, rows, cols, *args, **kwargs):
        self.scale = scale
        self.rows = rows
        self.cols = cols
        self.width = int(((self.scale +1) * self.cols) -
                         ((self.scale/4) * self.cols) + scale)
        self.height = int((self.scale * self.rows) +
                          ((self.scale / 2) + self.scale))


        self.setHexaSize(self.scale)
        self.sonobuoy_display_range = kwargs.get('sonobuoy_display_range', True)


    def setCell(self, idraw, xCell, yCell, items, *args, **kwargs):
        """ Create a content in the cell of coordinates x and y. Could specify options throught keywords :fill and outline"""
        self.margin = self.hexaSize

        pix_x = ((self.hexaSize - (self.hexaSize/4) + 1) * xCell) + self.margin # the +1 in this line adds horizontal  spacing between the cells
        pix_y = (self.hexaSize * yCell) + self.margin

        # Add Y offset to odd cells
        if (xCell % 2) != 0:
            pix_y = pix_y + self.hexaSize*0.5

        self.create_hexagone(idraw, pix_x, pix_y, items, *args, **kwargs)

    # Sets the size of the hexes bsed on the scale.
    def setHexaSize(self, number):
        self.hexaSize = number

    # Creates a triangle to represent the Pellican in the top center of a hex
    def createPelican(self, x, y):
        size = self.hexaSize
        #   X Y are the ceter of the triangle
        #       1
        #      /\
        #   3 /__\ 2
        #
        point1 = (x, y - (size/8))
        point2 = (x + (size/8), y + ((size/8)*2))
        point3 = (x - (size/8), y + ((size/8)*2))

        self.idraw.polygon([point1, point2, point3], fill=(
            255, 255, 255), outline=(255, 255, 255))

    # Creates a oval to represent the Plark in the bottom center of the hex
    def createPanther(self, x, y):
        size = self.hexaSize
        point1 = (x - ((size/8)*1.5), y - (size/8))
        point2 = (x + ((size/8)*1.5), y + (size/8))

        # self.create_oval(point1, point2, fill=(255,255,0))
        self.idraw.ellipse([point1, point2], fill=(255, 255, 0))

    def create_torpedo(self, x, y):
        size = self.hexaSize
        point1 = (x, y)
        point2 = (x + size/8, y + size/4)

        self.idraw.rectangle(
            [point1, point2], outline=(0, 0, 0), fill=(0, 0, 0))

    # Creates a sonobuoy at location x,y with state(hot/cold)
    #
    def create_sonobuoy(self, x, y, state):
        size = self.hexaSize
        point1 = (x, y)
        point2 = (x + size/4, y + size/4)
        fill = (0, 255, 0)  # COLD fill

        if state == "HOT":
            fill = (255, 0, 0)  # HOT fill

        self.idraw.ellipse([point1, point2], fill=fill, outline=fill)

    def create_explosion(self, x, y):
        half = self.hexaSize/2
        quarter = self.hexaSize/4

        # generate hex points based on size parameter
        # points start at
        #
        #  2    ____    3
        #      /    \
        #  1  /      \  4
        #     \      /
        #  6   \____/   5
        #
        point1 = (x - half, y)
        point2 = (x - quarter, y - half)
        point3 = (x + quarter, y - half)
        point4 = (x + half, y)
        point5 = (x + quarter, y + half)
        point6 = (x - quarter, y + half)

        self.idraw.polygon([point1, point2, point3, point4,
                            point5, point6], fill="red")


    # Creates a hex displaying the needed components within the hex based on the item list
    def create_hexagone(self, idraw, x, y, items, fill, outline=None):
        self.idraw = idraw
        half = self.hexaSize/2 - 1 # the -1 makes there a gap between the hexes 
        quarter = self.hexaSize/4

        # generate hex points based on size parameter
        # points start at
        #
        #  2    ____    3
        #      /    \
        #  1  /      \  4
        #     \      /
        #  6   \____/   5
        #
        point1 = (x - half, y)
        point2 = (x - quarter, y - half)
        point3 = (x + quarter, y - half)
        point4 = (x + half, y)
        point5 = (x + quarter, y + half)
        point6 = (x - quarter, y + half)

        if self.sonobuoy_display_range:
            if 'sonar_area' in items:
                if items['sonar_area'] == "HOT":
                    outline = "red"
                else:
                    outline = 'green'

        self.idraw.polygon([point1, point2, point3, point4,
                            point5, point6], fill=fill, outline=outline)

        if "PELICAN" in items:
            self.createPelican(x, (y - quarter))

        if "PANTHER" in items:
            self.createPanther(x, (y + quarter))

        if "SONOBUOY" in items:
            self.create_sonobuoy(x - (quarter + quarter/2),
                                 y - (quarter / 2), items['SONOBUOY'])

        if "TORPEDO" in items:
            self.create_torpedo(x + quarter, y - (quarter / 2))

        if "EXPLOSION" in items:
            self.create_explosion(x, y)

        # if items['WATER']:

    def renderUIGrid(self, gridMap, idraw):
        for col in range(self.cols):
            for row in range(self.rows):
                hexCell = gridMap[col][row]
                hexFill = ''
   
                typeValue = hexCell['HexType']

                if typeValue == 0:
                    hexFill = (102, 128, 255)
                elif typeValue == 1:
                    hexFill = 'green'
                else:
                    hexFill = 'white'

                items = hexCell['objects']
                self.setCell(idraw, col, row, items, fill=hexFill)


class Loadout():
    def __init__(self, loadout, location, font, scale, sonobuoy_range, torp_hunt, torp_speeds):
        self.font = font
        self.location = location
        self.loadout_cols = 5
        self.scale = scale
        self.loadout = Loadout
        self.width = (self.loadout_cols * self.scale) + self.scale
        self.height = 0
        self.sonobuoy_range = sonobuoy_range
        self.torp_hunt = torp_hunt
        self.torp_speeds = torp_speeds
        self.sonobuoy_count = len(list(filter(lambda item: (item.type == 'SONOBUOY'), loadout)))
        self.torp_count = len(list(filter(lambda item: (item.type == 'TORPEDO'), loadout))) 
        self.madman_loadout_location = [
            self.location[0],
            self.location[1] 
        ]

        if self.font.size > 16 :
            self.scale += font.size
            self.madman_loadout_location[1] += font.size

        self.torpedo_loadout_location = [
             self.location[0],
             self.madman_loadout_location[1] + self.scale * 1.25
        ] 
        self.sonobuoy_loadout_location = [
            self.location[0],
            # This is the combination of all the spacing calculations in the ideal world this would all be refactored so each section had an overall height that could be called by the following section.
            self.torpedo_loadout_location[1] + (self.scale * math.ceil(self.torp_count / self.loadout_cols)) + (self.scale * 0.5) + self.scale  + (self.scale * len(self.torp_speeds)+1)
        ]



    def render(self, loadout, madman, idraw):
        self.torpedo_list = list(
            filter(lambda item: (item.type == 'TORPEDO'), loadout))
        self.sonobuoy_list = list(
            filter(lambda item: (item.type == 'SONOBUOY'), loadout))
        self.madman = madman

        self.render_madman_loadout(self.madman_loadout_location,idraw)
        self.render_torpedo_loadout(self.torpedo_loadout_location, idraw)
        self.render_sonobuoy_loadout(self.sonobuoy_loadout_location, idraw)

    def render_madman_loadout(self, location, idraw):

        madman_text_location = [
            location[0],
            location[1]
        ]

        madman_location_point1 = (
            location[0] + self.scale/2,
            madman_text_location[1] + self.scale/2
        )
        
        madman_location_point2 = (
            madman_location_point1[0] + self.scale, 
            madman_location_point1[1] + self.scale/2
        )
        
        idraw.text(madman_text_location, 'Madman status:', fill='black', font=self.font)
        if self.madman:
            fill = (255, 0, 0)
        else:
            fill = (0, 255, 0)

        idraw.rectangle([madman_location_point1, madman_location_point2], outline=fill, fill=fill)

    def render_sonobuoy_loadout(self, location, idraw):
        sonobuoy_bay = [
            location[0] + self.scale/2,
            location[1] ,
        ]

        sonobuoy_range_location = [
            location[0] ,
            location[1] + ((self.scale * self.sonobuoy_count) / self.loadout_cols) + (self.scale * 0.5)
        ]

        sonobuoy_string = 'Sonobuoy: ' + str(len(self.sonobuoy_list))
        idraw.text(location, sonobuoy_string, fill='black', font=self.font)

        sonobuoy_range_string = 'Sonobuoy range: '+ str(self.sonobuoy_range)
        idraw.text(sonobuoy_range_location, sonobuoy_range_string, fill='black', font=self.font)

        for i in range(len(self.sonobuoy_list)):
            if (i % self.loadout_cols) == 0:
                sonobuoy_bay = (sonobuoy_bay[0], sonobuoy_bay[1] + self.scale/1.5) 
                bayCount = 0

            sb_location = (sonobuoy_bay[0] + (bayCount * self.scale/1.5), sonobuoy_bay[1])
            self.render_sonobuoy(sb_location, idraw)
            bayCount += 1

        for i in range(0, self.sonobuoy_range):
            hex_size = self.scale / 2
            pix_x = ((hex_size - (hex_size/4)) * i)+ hex_size/2 + sonobuoy_range_location[0]
            pix_y = (hex_size) + (hex_size/2) + sonobuoy_range_location[1]

            # Add Y offset to odd cells
            if (i % 2) != 0:
                pix_y = pix_y + (hex_size * 0.5)
            
            self.render_hex(pix_x, pix_y, hex_size , idraw,(0, 255, 0),'white')
 
    def render_torpedo_loadout(self, location, idraw):

        torpedo_bay_location = [
            location[0] + self.scale/2,
            location[1] + self.scale/1.5,
        ]
        hunt_text_location = [
            location[0] ,
            location[1] + (self.scale * math.ceil(self.torp_count / self.loadout_cols)) + (self.scale * 0.5)
        ]
        speed_text_location = [
            location[0] ,
            hunt_text_location[1] + self.scale * 0.5,
        ]
        

        hunt_string = "Torpedos hunt: "
        text_w, text_h = idraw.textsize(hunt_string)
        hunt_icon_location = (
            hunt_text_location[0] + text_w + self.scale/2,
            hunt_text_location[1]
        )

        if self.font.size > 16 :
            hunt_icon_location = (
                hunt_text_location[0] + text_w + self.scale,
                hunt_text_location[1]
            )

        torp_colour = (255,0,0)
        if self.torp_hunt:
            torp_colour = (0,255,0)

        # render text 
        torpedo_string = 'Torpedos: ' + str(len(self.torpedo_list))
        idraw.text(location, torpedo_string, fill='black', font=self.font)
        idraw.text(hunt_text_location, hunt_string, fill='black', font=self.font)
        idraw.text(speed_text_location, 'Torpedo speed:', fill='black', font=self.font)

        # torp hunt icon
        self.render_torpedo(hunt_icon_location,idraw, torp_colour, torp_colour) # sets both fill and outline to torp colour

        # render torps
        bayCount = 0
        torpedo_bay = (torpedo_bay_location[0], torpedo_bay_location[1])
        for i in range(len(self.torpedo_list)):
            if (i % self.loadout_cols) == 0 and i != 0:
                torpedo_bay = (torpedo_bay[0], torpedo_bay[1] + (self.scale * 0.7))
                bayCount = 0

            location = (torpedo_bay[0] + (bayCount * self.scale/2), torpedo_bay[1])
            self.render_torpedo(location, idraw)
            bayCount += 1

        # render torp turns 
        for t, s in enumerate(self.torp_speeds):
            turn_string = 'T' + str(t+1) + ':'
            text_w, text_h = idraw.textsize(turn_string)
            speed_text_location = (
                speed_text_location[0] ,
                speed_text_location[1] + ((self.scale *0.5) * (t+1)) 
            )
            idraw.text(speed_text_location , turn_string, fill='black', font=self.font)

            for i in range(0, s ):
                hex_size = self.scale / 2
                pix_x = ((hex_size - (hex_size/4)) * i) + hex_size + speed_text_location[0] + text_w  
                pix_y = hex_size/2 +  speed_text_location[1] 

                # Add Y offset to odd cells
                if (i % 2) != 0:
                    pix_y = pix_y + (hex_size * 0.5)
                
                self.render_hex(pix_x, pix_y, hex_size , idraw,(0, 255, 0),'white')

    def render_torpedo(self, location, idraw, fill=(0, 0, 0), outline=(0, 0, 0)):
        point1 = location
        point2 = (location[0] + self.scale/4, location[1] + self.scale/2)

        idraw.rectangle([point1, point2], outline=outline, fill=fill)

    def render_sonobuoy(self, location, idraw):
        point1 = location
        point2 = (location[0] + self.scale/2, location[1] + self.scale/2)
        fill = (0, 255, 0)  # COLD fill

        idraw.ellipse([point1, point2], fill=fill, outline=fill)

    def render_hex(self, pix_x, pix_y , hex_size, idraw, fill, outline):
        half = hex_size/2  
        quarter = hex_size/4

        point1 = (pix_x - half, pix_y)
        point2 = (pix_x - quarter, pix_y - half)
        point3 = (pix_x + quarter, pix_y - half)
        point4 = (pix_x + half, pix_y)
        point5 = (pix_x + quarter, pix_y + half)
        point6 = (pix_x - quarter, pix_y + half)

        idraw.polygon([point1, point2, point3, point4, point5, point6], fill, outline)

class Counters():
    def __init__(self, maxturn, location, font):
        self.font = font
        self.location = location
        self.max_turn = maxturn

        self.turn_location = [
            self.location[0],
            self.location[1]
        ]
        self.move_location = [
            self.location[0],
            self.location[1] + self.font.size
        ]
        self.game_state_location = [
            self.location[0],
            self.location[1] + self.font.size * 2
        ]

    def renderCounters(self, turn, move, max_moves, state, idraw):
        # Generates the turn and move counters

        turn_string = 'Turn: ' + str(turn) + '/' + str(self.max_turn)
        move_string = 'Move: ' + str(move) + '/' + str(max_moves)
        game_state_string = 'Game state: ' + state

        idraw.text(self.turn_location, turn_string,
                   fill='black', font=self.font)
        idraw.text(self.move_location, move_string,
                   fill='black', font=self.font)
        idraw.text(self.game_state_location, game_state_string,
                   fill='black', font=self.font)


class Status_Bar():
    def __init__(self, location, width, font, scale=20):
        self.font = font
        self.height = scale
        self.width = width - scale*2
        self.point1 = location
        self.point2 = (location[0] + self.width, location[1] + self.height)
        self.status_bar_text_location = ()

    def render_status_bar(self, status_Bar, idraw):
        message = status_Bar['message']
        if message != '':
            fill = status_Bar['fill']
            # Calculates the width and height of the status message to centeralise in box
            text_w, text_h = idraw.textsize(message)
            self.status_bar_text_location = [
                self.point1[0] + ((self.width - text_w)/2),
                self.point1[1] + ((self.height - text_h)/8)
            ]

            idraw.rectangle([self.point1, self.point2],
                            outline=fill, fill=fill)
            idraw.text(self.status_bar_text_location, message,
                       fill='white', font=self.font)


class PIL_UI():
    def __init__(self, gameFile, scale, render_all, sonobuoy_display_range, render_width,render_height, sonobuoy_range, torp_hunt, torp_speeds):
        # Initilise pil UI.
        self.scale = scale
        self.render_all = render_all
        self.sonobuoy_display_range = sonobuoy_display_range
        self.sonobuoy_range = sonobuoy_range
        self.torp_hunt = torp_hunt
        self.torp_speeds = torp_speeds
        self.render_width = render_width
        self.render_height = render_height
        self.map = None
        
        #self.loadMapFromJson(gameFile['mapFile'])
        
        self.process_game_board(gameFile['gameBoard'])
        self.loadFont(self.rows)
        # Initilise Grid components
        self.grid = HexagonalGrid(self.scale, self.rows, self.cols, sonobuoy_display_range=self.sonobuoy_display_range)

        # Set locations of counters and loadout.
        self.counters_location = (self.grid.width, self.scale * 0.5)
        self.loadout_location = (self.grid.width, self.counters_location[1] + (self.scale * 1.5))
        self.status_bar_location = (scale, self.grid.height)

        # Initilise Counters and loadout components based on grid position
        self.counters = Counters(gameFile["maxTurns"], self.counters_location, self.font)
        self.loadout = Loadout(gameFile['pelican_loadout'], self.loadout_location, self.font, self.scale, self.sonobuoy_range, self.torp_hunt, self.torp_speeds)

        # Calculate width of image size based on components.
        self._width = self.grid.width + self.loadout.width + self.scale

        # Initilises the status bar
        self.status_bar = Status_Bar(self.status_bar_location, self._width, self.font, self.scale)

        # Calculate height of image size based on components.
        self._height = self.grid.height + self.status_bar.height

        # Calls the update function to render the initial game.
        self.update(gameFile)

    def update(self, gameFile,render_width=None,render_height=None):
        # Creates a clean canvas and draw interface
        self.ui_img = Image.new('RGB', (self._width, self._height), 'white')
        self.idraw = ImageDraw.Draw(self.ui_img)

        # Update the UI map from recieved JSON file
        #self.loadMapFromJson(gameFile['mapFile'])
        self.process_game_board(gameFile['gameBoard'])

        # Updates the display components with updates information
        self.grid.renderUIGrid(self.gridMap, self.idraw)

        # Set the move count and limit based on driving agent 
        if gameFile['driving_agent'] == 'pelican':
            move_in_turn = gameFile['pelican_move_in_turn']
            max_moves = gameFile['pelican_max_moves']
        elif gameFile['driving_agent'] == 'panther':
            move_in_turn = gameFile['panther_move_in_turn']
            max_moves = gameFile['panther_max_moves'] 

        # Render counters and loadouts based on driving agent
        if gameFile['driving_agent'] == 'pelican' or self.render_all:
            self.counters.renderCounters(gameFile['turn_count'], move_in_turn, max_moves, gameFile['game_state'], self.idraw)
            self.loadout.render(gameFile['pelican_loadout'], gameFile['madman'], self.idraw)
        elif gameFile['driving_agent'] == 'panther':
            self.counters.renderCounters(gameFile['turn_count'], move_in_turn, max_moves, gameFile['game_state'], self.idraw)

        self.status_bar.render_status_bar(gameFile['status_bar'], self.idraw)

        if render_height is not None and render_width is not None:
            return self.ui_img.resize([render_width,render_height], Image.LANCZOS)
        else:
            return self.ui_img.resize([self.render_width,self.render_height], Image.LANCZOS)
      
    # def loadMapFromJson(self, mapfile):
    #     # Loads map from file adjusting rows and cols for rendering.
    #     self.gridMap = json.loads(mapfile)
    #     self.rows = len(self.gridMap[0])
    #     self.cols = len(self.gridMap)


    def process_game_board(self, gameBoard):
        self.rows = len(gameBoard[0])
        self.cols = len(gameBoard)
        if self.map is None:
            self.map = Map(self.cols,self.rows)

        uiOutput = [[0 for x in range(self.rows)] for y in range(self.cols)]

        for col in range(self.cols):
            for row in range(self.rows):
                uiOutput[col][row] = {
                    "HexType": 0,
                    "coordinate": [
                        col,
                        row
                    ],
                    "objects": {}
                }                      

        for col in range(self.cols):
            for row in range(self.rows):
       
                hexCell = gameBoard[col][row]
             
                for item in hexCell.objects:
                    if item.type == 'SONOBUOY':
                        uiOutput[col][row]['objects'][item.type] = item.state

                        # add marker to all in radius 
                        sonar_area = self.map.getRadius(item.col, item.row, item.range)
                        for cell in sonar_area:
                            cell_col = cell['col']
                            cell_row = cell['row']
                            uiOutput[cell_col][cell_row]['objects']['sonar_area'] = item.state
                    
                    else:
                        uiOutput[col][row]['objects'][item.type] = True

        self.gridMap = uiOutput

        

    def loadFont(self, font_size = 16):
        # Load font file
        if font_size < 16:
            font_size = 16
        try:
            font_path = os.path.join(os.path.dirname(__file__), 'resources/font.ttf')
            font_path = os.path.normpath(font_path)
            self.font = ImageFont.truetype(font_path, font_size)
        except:
            # default font
            self.font = ImageFont.load_default()
            logger.info('Failed to load font, default font used')
