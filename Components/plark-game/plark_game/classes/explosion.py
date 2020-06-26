class Explosion():

    def __init__(self):
        self.id = ""
        self.type = "EXPLOSION"
        self.col = None
        self.row = None
        
    def setLocation(self, col, row):
        self.col = col
        self.row = row