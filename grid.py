"""
This file contains the class Grid. 
The grid is 5x5 in height and width. Matching the board size in KingDomino

Every point in the grid contains a tile object. 
The grid class has access to diffrenc functions such as get_neighbours etc. 
It is based on this grid that the program should calculate the final sum of points 
gain during the Kongdomino game.
"""

import tile
from models import crown_analyser
from models import tile_detector
from models import tile_detector as td
from models import crown_analyser as ca

class Grid:
    def __init__(self, size=5): 
        # dimentions
        self.size = size
            
        # the grid
        self.grid = self.create_grid()

        # the models
        self.tile_detector=td.TileDetector()
        self.crown_analyser=ca.CrownAnalyser()


    def create_grid(self):
        """Create a grid of tile objects"""
        grid = []
        for i in range(self.size):
            grid.append([tile.Tile(x=i,y=j) for j in range(self.size)])
        return grid

    def get_neighbors(self, coord):
        """Returns the neighbors of the input coordinate"""
        assert type(coord) == tuple
        neighbors = [(coord[0]+1,coord[1]),
                    (coord[0]-1,coord[1]),
                    (coord[0],coord[1]+1),
                    (coord[0],coord[1]-1)]
            
        #removes out of bounds neighbors
        neighbors = [(x,y) for x, y in neighbors 
                    if 0 <= x < self.size 
                    and 0 <= y < self.size]
        return neighbors
        
    def count_points(self):
        """Finds lines of the same biome and count their total value. It also marks them as visited.""" 
        pass

    def find_connected_tiles(self, start):
        """Finds all connected fields starting from 'start'"""
        if self.grid[start[0]][start[1]].get_counted() == False:
            tile_biome = self.grid[start[0]][start[1]].get_biome()
            visited = set()  # To keep track of visited tiles
            stack = [start]  # Using DFS, stack stores the current path
        
            connected_biomes = set()  # To store the path of connected fields
        
            while stack:
                current = stack.pop()  # Pop from the stack
                if current in visited:
                    continue  # Skip if the tile has already been visited
                visited.add(current)
                connected_biomes.add(self.grid[current[0]][current[1]])
            
                # Check neighbors and add them to the stack if they are a field
                for neighbor in sorted(self.get_neighbors(current)):
                    x, y = neighbor
                    if self.grid[x][y].get_biome() == tile_biome and neighbor not in visited:
                        stack.append(neighbor)

            # Changes the counted variable for all tiles to True, so they wont be counted again.
            for tile in list(connected_biomes):
                tile.set_counted(True)   
            return connected_biomes



    def all_connected_tiles(self):
        tile_connections = []
        for row in self.grid:
            for tile in row:
                if tile.get_counted()==False:
                    connection = self.find_connected_tiles(tile.get_coord())
                    tile_connections.append(connection)
        return tile_connections


    def calc_connected_tiles_total_sum(self):
        
        sum_total = 0
        connected_tiles = self.all_connected_tiles()

        # find the crowns and ammount of tiles in the connection and multiplies them for each connection. 
        # And adds the sum_connection to the sum_total
        for connection in connected_tiles: 
            sum_connection = 0
            crowns = 0
            tiles = 0 
            for tile in list(connection):
                tiles += 1
                crowns += tile.get_crowns() 
            sum_connection = tiles*crowns
            sum_total += sum_connection

        return sum_total
        
    def run_models(self):
        """Run the models on the grid."""
        for row in self.grid:
            for tile in row:
                tile.biome = self.tile_detector.predict(tile.tile_image)
                tile.crowns = self.crown_analyser.predict_image_label(tile.tile_image)