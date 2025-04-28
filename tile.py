"""
This file contains the class Tile. 
A tile should contain the label of the tiles biome, the amount of crowns, 
and the its grid coordinates.

The purpose of this class is to be the objects inside the grid class. 
"""

class Tile:
    def __init__(self,x,y): 
        #Coordinates
        self.x_pos = x
        self.y_pos = y
        self.counted = False
        
        #tile image:
        self.tile_image = []
        
        #Tile features
        self.biome = None
        self.crowns = 0

        self.labels = {
            0: "Bord",
            1: "Castle",
            2: "Fields",
            3: "Forest",
            4: "Grasslands",
            5: "Lakes",
            6: "Mine",
            7: "Swamp",
        }

    def set_biome(self, biome_predicted):
        """Sets the biome of the tile based on HOG/HSV model prediction"""
        assert type(biome_predicted) == int 
        self.biome=self.labels[biome_predicted]

    def set_crowns(self, crowns_predicted):
        """Sets the amount of crowns on the tile based on SIFT model prediction"""
        assert type(crowns_predicted) == int
        self.crowns=crowns_predicted

    def set_tile_image(self, chopped_image):
        """Sets image of the tile. Based on the chopped board."""
        self.tile_image=chopped_image

    def set_counted(self, boolean):
        assert type(boolean) == bool
        self.counted = boolean

    def get_biome(self):
        """Returns the biome of the tile"""
        return self.biome

    def get_crowns(self):
        """Returns the amount of crowns on the tile"""
        return self.crowns
    
    def get_image(self):
        """Returns the amount of crowns on the tile"""
        return self.tile_image
    
    def get_counted(self):
        return self.counted
    
    def get_coord(self):
        """Returns the tiles position in the grid"""
        return (self.x_pos, self.y_pos)